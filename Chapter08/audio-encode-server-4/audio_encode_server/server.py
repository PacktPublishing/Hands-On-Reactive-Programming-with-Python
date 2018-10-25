import json
import threading
import asyncio
import datetime
from collections import namedtuple
from rx import Observable
from rx.concurrency import ThreadPoolScheduler, AsyncIOScheduler
from cyclotron import Component
from cyclotron_aio.runner import run

import cyclotron_std.sys.argv as argv
import cyclotron_std.argparse as argparse
import cyclotron_aio.httpd as httpd
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
aio_scheduler = AsyncIOScheduler()

def parse_config(file_data):
    config = (
        file_data
        .filter(lambda i: i.id == "config")
        .flat_map(lambda i: i.data)
        .map(lambda i: json.loads(
            i,
            object_hook=lambda d: namedtuple('x', d.keys())(*d.values())))
    )

    return config.share()


def audio_encoder(sources):
    # Parse configuration
    parsed_argv = (
        sources.argv.argv.skip(1)
        .let(argparse.argparse,
            parser=Observable.just(
                argparse.Parser(description="audio encode server")),
            arguments=Observable.from_([
                argparse.ArgumentDef(
                    name='--config', help="Path of the server configuration file")
            ]))
        .filter(lambda i: i.key == 'config')
        .subscribe_on(aio_scheduler)
        .share()
    )

    # monitor and parse config file
    monitor_init = (
        parsed_argv
        .flat_map(lambda i : Observable.from_([
            inotify.AddWatch(id='config', path=i.value, flags=aionotify.Flags.MODIFY),
            inotify.Start(),
        ]))
    )

    config_update = (
        sources.inotify.response
        .debounce(5000)
        .map(lambda i: True)
        .start_with(True)
    )

    read_config_file = (
        Observable.combine_latest(parsed_argv, config_update,
            lambda config, _: file.Read(id='config', path=config.value))
    )
    config = sources.file.response.let(parse_config)

    # Transcode request handling
    encode_init = (
        config
        .map(lambda i: i.encode)
        .distinct_until_changed()
        .map(lambda i: encoder.Configure(
            samplerate=i.samplerate,
            bitdepth=i.bitdepth))
    )

    encode_request = (
        sources.httpd.route
        .filter(lambda i: i.id == 'flac_transcode')
        .flat_map(lambda i: i.request)
        .flat_map(lambda i: Observable.just(i, encode_scheduler))
        .map(lambda i: encoder.EncodeMp3(
            id=i.context,
            data=i.data,
            key=i.match_info['key']))
    )
    encoder_request = Observable.merge(encode_init, encode_request)

    # store encoded file
    store_requests = (
        sources.encoder.response
        .observe_on(s3_scheduler)
        .map(lambda i: s3.UploadObject(
            key=i.key + '.flac',
            data=i.data,
            id=i.id,
        ))
    )

    # acknowledge http request
    http_response = (
        sources.s3.response
        .map(lambda i: httpd.Response(
            data='ok'.encode('utf-8'),
            context=i.id,
        ))
    )

    # http server
    http_init = (
        config.take(1)
        .flat_map(lambda i: Observable.from_([
            httpd.Initialize(request_max_size=0),
            httpd.AddRoute(
                methods=['POST'],
                path='/api/transcode/v1/flac/{key:[a-zA-Z0-9-\._]*}',
                id='flac_transcode',
            ),
            httpd.StartServer(
                host=i.server.http.host,
                port=i.server.http.port),
        ]))
    )
    http = Observable.merge(http_init, http_response)

    # s3 database
    s3_init = (
        config.take(1)
        .map(lambda i: s3.Configure(
            access_key=i.s3.access_key,
            secret_key=i.s3.secret_key,
            bucket=i.s3.bucket,
            endpoint_url=i.s3.endpoint_url,
            region_name=i.s3.region_name,
        ))
    )

    # merge sink requests
    file_requests = read_config_file
    s3_requests = Observable.merge(s3_init, store_requests)

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
