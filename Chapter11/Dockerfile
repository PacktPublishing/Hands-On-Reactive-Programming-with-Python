FROM python:3.6

RUN apt-get update && apt-get install -y sox libsox-fmt-mp3

ENV config /opt/audio-encoder/config.json
WORKDIR /tmp/audio-encode-server

COPY ./ /tmp/audio-encode-server
RUN python setup.py install

CMD ["sh", "-c", "/usr/local/bin/audio-encode-server --config ${config}"]