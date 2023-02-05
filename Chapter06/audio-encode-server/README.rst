======================================
The Reactive Audio Transcoding Server
======================================

This is a reactive implementation of an audio transcoding HTTP server.


..code:: console
    pip install --editable .

..code:: console
    audio-encode-server --config ./config.sample.json

..code:: console
    curl -X POST --data-binary @audio-dataset/banjo0.mp3  http://localhost:8080/api/transcode/v1/flac/banjo

transcoded file is in /tmp/banjo.flac
