import os
import threading
from collections import namedtuple
from rx import Observable
import sox

from cyclotron import Component


def mp3_to_flac(data, samplerate, bitdepth):
    tid = threading.get_ident()
    tmp_filename = os.path.join('/tmp/transcode-{}.mp3'.format(tid))
    tmp2_filename = os.path.join('/tmp/transcode-{}.flac'.format(tid))
    with open(tmp_filename, 'wb') as content_file:
        size = content_file.write(data)
        status = 0 if size == len(data) else -1
    transformer = sox.Transformer()
    transformer.convert(samplerate=samplerate, n_channels=2, bitdepth=bitdepth)
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
Configure = namedtuple('Configure', ['samplerate', 'bitdepth'])
EncodeMp3 = namedtuple('Encode', ['id', 'data', 'key'])

# Source events
EncodeResult = namedtuple('EncodeResult', ['id', 'data', 'key'])


def make_driver():
    def encoder(sink):
        def on_subscribe(observer):
            samplerate = None
            bitdepth = None

            def on_next(item):
                nonlocal samplerate
                nonlocal bitdepth
                if type(item) is Configure:
                    print("configure: {}".format(item))
                    samplerate = item.samplerate
                    bitdepth = item.bitdepth
                elif type(item) is EncodeMp3:
                    encoded_data = mp3_to_flac(
                        item.data, samplerate, bitdepth)
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
