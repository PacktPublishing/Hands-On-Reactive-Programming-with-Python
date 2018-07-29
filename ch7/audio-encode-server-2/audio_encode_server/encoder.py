import os
from collections import namedtuple
from rx import Observable
import sox

from cyclotron import Component


def mp3_to_flac(data):
    tmp_filename = os.path.join('/tmp/transcode-tmp.mp3')
    tmp2_filename = os.path.join('/tmp/transcode-tmp.flac')
    with open(tmp_filename, 'wb') as content_file:
        size = content_file.write(data)
        status = 0 if size == len(data) else -1
    transformer = sox.Transformer()
    transformer.convert(samplerate=16000, n_channels=2, bitdepth=16)
    transformer.build(tmp_filename, tmp2_filename)

    # retrieve data in a buffer
    with open(tmp2_filename, mode='rb') as file:
        flac_data = file.read()

    os.remove(tmp_filename)
    os.remove(tmp2_filename)
    return flac_data


Source = namedtuple('Source', ['response'])
Sink = namedtuple('Sink', ['request'])

# Sink events
Initialize = namedtuple('Initialize', ['storage_path'])
EncodeMp3 = namedtuple('Encode', ['id', 'data', 'key'])

# Source events
EncodeResult = namedtuple('EncodeResult', ['id', 'data', 'key'])


def make_driver():
    def encoder(sink):
        def on_subscribe(observer):
            storage_path = None

            def on_next(item):
                if type(item) is Initialize:
                    nonlocal storage_path
                    storage_path = item.storage_path
                elif type(item) is EncodeMp3:
                    encoded_data = mp3_to_flac(
                        item.data)
                    observer.on_next(
                        EncodeResult(id=item.id, key=item.key, data=encoded_data))
                else:
                    observer.on_error("unknown item: {}".format(type(item)))

            sink.request.subscribe(
                on_next=on_next,
                on_error=lambda e: observer.on_error(e),
                on_completed=lambda: observer.on_completed(),
            )

        return Source(
            response=Observable.create(on_subscribe)
        )

    return Component(call=encoder, input=Sink)
