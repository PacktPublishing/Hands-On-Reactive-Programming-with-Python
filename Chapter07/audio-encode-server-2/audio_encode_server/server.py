import json
from collections import namedtuple
import reactivex as rx
import reactivex.operators as ops
from cyclotron import Component
from cyclotron.asyncio.runner import run

import cyclotron_std.sys.argv as argv
import cyclotron_std.argparse as argparse
import cyclotron_aiohttp.httpd as httpd
import cyclotron_std.io.file as file

import audio_encode_server.encoder as encoder
import audio_encode_server.s3 as s3

Drivers = namedtuple('Drivers', ['encoder', 'httpd', 's3', 'file', 'argv'])
Source = namedtuple('Source', ['encoder', 'httpd', 's3', 'file', 'argv'])
Sink = namedtuple('Sink', ['encoder', 'httpd', 's3', 'file'])


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

    read_request, read_response = sources.argv.argv.pipe(
        ops.skip(1),
        argparse.parse(parser),
        ops.filter(lambda i: i.key == 'config'),
        ops.map(lambda i: file.Read(id='config', path=i.value)),
        file.read(sources.file.response),
    )
    config = read_response.pipe(
        ops.filter(lambda i: i.id == "config"),
        ops.flat_map(lambda i: i.data),
        parse_config,
    )

    # Transcode request handling
    encode_init = config.pipe(
        ops.map(lambda i: encoder.Initialize(storage_path=i.encode.storage_path))
    )

    encode_request = sources.httpd.route.pipe(
        ops.filter(lambda i: i.id == 'flac_transcode'),
        ops.flat_map(lambda i: i.request),
        ops.map(lambda i: encoder.EncodeMp3(
            id=i.context,
            data=i.data,
            key=i.match_info['key'])),
    )
    encoder_request = rx.merge(encode_init, encode_request)

    # store encoded file
    store_requests = sources.encoder.response.pipe(
        ops.map(lambda i: s3.UploadObject(
            key=i.key + '.flac',
            data=i.data,
            id=i.id,
        ))
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
        ]))
    )
    http = rx.merge(http_init, http_response)

    # s3 database
    s3_init = config.pipe(
        ops.map(lambda i: s3.Configure(
            access_key=i.s3.access_key,
            secret_key=i.s3.secret_key,
            bucket=i.s3.bucket,
            endpoint_url=i.s3.endpoint_url,
            region_name=i.s3.region_name,
        ))
    )

    # merge sink requests
    file_requests = read_request
    s3_requests = rx.merge(s3_init, store_requests)

    return Sink(
        encoder=encoder.Sink(request=encoder_request),
        s3=s3.Sink(request=s3_requests),
        file=file.Sink(request=file_requests),
        httpd=httpd.Sink(control=http),
    )


def main():
    dispose = run(
        entry_point=Component(call=audio_encoder, input=Source),
        drivers=Drivers(
            encoder=encoder.make_driver(),
            httpd=httpd.make_driver(),
            s3=s3.make_driver(),
            file=file.make_driver(),
            argv=argv.make_driver(),
        )
    )
    dispose()
