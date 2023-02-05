import json
import threading
import asyncio
import datetime
from collections import namedtuple
import reactivex as rx
import reactivex.operators as ops
from reactivex.scheduler import ThreadPoolScheduler
from reactivex.scheduler.eventloop import AsyncIOScheduler
from cyclotron import Component
from cyclotron.asyncio.runner import run

import cyclotron_std.sys.argv as argv
import cyclotron_std.argparse as argparse
import cyclotron_aiohttp.httpd as httpd
import cyclotron_std.io.file as file

import audio_encode_server.encoder as encoder
import audio_encode_server.s3 as s3
import audio_encode_server.inotify as inotify
import aionotify

Drivers = namedtuple('Drivers', ['encoder', 'httpd', 's3', 'file', 'inotify', 'argv'])
Source = namedtuple('Source', ['encoder', 'httpd', 's3', 'file', 'inotify', 'argv'])
Sink = namedtuple('Sink', ['encoder', 'httpd', 's3', 'file', 'inotify'])

s3_scheduler = ThreadPoolScheduler(max_workers=1)
encode_scheduler = ThreadPoolScheduler(max_workers=4)
aio_scheduler = AsyncIOScheduler(asyncio.get_event_loop())


def parse_config(file_data):
    return file_data.pipe(
        ops.map(lambda i: json.loads(
            i,
            object_hook=lambda d: namedtuple('x', d.keys())(*d.values()))),
        ops.share(),
    )


def create_arg_parser():
    parser = argparse.ArgumentParser("audio encode server")
    parser.add_argument(
        '--config', required=True,
        help="Path of the server configuration file")
    return parser


def audio_encoder(sources):
    # Parse configuration
    parser = create_arg_parser()

    parsed_argv = sources.argv.argv.pipe(
        ops.skip(1),
        argparse.parse(parser),
        ops.filter(lambda i: i.key == 'config'),
        ops.subscribe_on(aio_scheduler),
        ops.share(),
    )

    # monitor and parse config file
    monitor_init = parsed_argv.pipe(
        ops.flat_map(lambda i : rx.from_([
            inotify.AddWatch(id='config', path=i.value, flags=aionotify.Flags.MODIFY),
            inotify.Start(),
        ]))
    )

    config_update = sources.inotify.response.pipe(
        ops.debounce(5.0, scheduler=aio_scheduler),
        ops.map(lambda i: True),
        ops.start_with(True),
    )

    read_request, read_response = rx.combine_latest(
        parsed_argv, config_update
    ).pipe(
        ops.starmap(lambda config, _: file.Read(id='config', path=config.value)),
        file.read(sources.file.response),
    )

    config = read_response.pipe(
        ops.filter(lambda i: i.id == "config"),
        ops.flat_map(lambda i: i.data),
        parse_config,
    )

    # Transcode request handling
    encode_init = config.pipe(
        ops.map(lambda i: i.encode),
        ops.distinct_until_changed(),
        ops.map(lambda i: encoder.Configure(
            samplerate=i.samplerate,
            bitdepth=i.bitdepth)),
    )

    encode_request = sources.httpd.route.pipe(
        ops.filter(lambda i: i.id == 'flac_transcode'),
        ops.flat_map(lambda i: i.request),
        ops.flat_map(lambda i: rx.just(i, encode_scheduler)),
        ops.map(lambda i: encoder.EncodeMp3(
            id=i.context,
            data=i.data,
            key=i.match_info['key'])),
    )
    encoder_request = rx.merge(encode_init, encode_request)

    # store encoded file
    store_requests = sources.encoder.response.pipe(
        ops.observe_on(s3_scheduler),
        ops.map(lambda i: s3.UploadObject(
            key=i.key + '.flac',
            data=i.data,
            id=i.id,
        )),
    )

    # acknowledge http request
    http_response = sources.s3.response.pipe(
        ops.map(lambda i: httpd.Response(
            data='ok'.encode('utf-8'),
            context=i.id,
        ))
    )

    # http server
    http_init = config.pipe(
        ops.take(1),
        ops.flat_map(lambda i: rx.from_([
            httpd.Initialize(request_max_size=0),
            httpd.AddRoute(
                methods=['POST'],
                path='/api/transcode/v1/flac/{key:[a-zA-Z0-9-\._]*}',
                id='flac_transcode',
            ),
            httpd.StartServer(
                host=i.server.http.host,
                port=i.server.http.port),
        ])),
    )
    http = rx.merge(http_init, http_response)

    # s3 database
    s3_init = config.pipe(
        ops.take(1),
        ops.map(lambda i: s3.Configure(
            access_key=i.s3.access_key,
            secret_key=i.s3.secret_key,
            bucket=i.s3.bucket,
            endpoint_url=i.s3.endpoint_url,
            region_name=i.s3.region_name,
        )),
    )

    # merge sink requests
    file_requests = read_request
    s3_requests = rx.merge(s3_init, store_requests)

    return Sink(
        encoder=encoder.Sink(request=encoder_request),
        s3=s3.Sink(request=s3_requests),
        file=file.Sink(request=file_requests),
        httpd=httpd.Sink(control=http),
        inotify=inotify.Sink(request=monitor_init),
    )


def main():
    dispose = run(
        entry_point=Component(call=audio_encoder, input=Source),
        drivers=Drivers(
            encoder=encoder.make_driver(),
            httpd=httpd.make_driver(),
            s3=s3.make_driver(),
            file=file.make_driver(),
            inotify=inotify.make_driver(),
            argv=argv.make_driver(),
        )
    )
    dispose()
