======================================
The Reactive Audio Transcoding Server
======================================

This is a reactive implementation of an audio transcoding HTTP server.

..code:: console
    docker run -d -p 9000:9000 -p 9001:9001 --name minio \
    -e "MINIO_ROOT_USER=P0B76GIFPB6T0OD5I67U" \
    -e "MINIO_ROOT_PASSWORD=3+kGshnhQ7i41UabvMz8buqUKgtGsikmdL1Q+oDR" \
    -v $HOME/minio/data:/data \
    -v $HOME/minio/config:/root/.minio \
    minio/minio server /data --console-address ":9001"

create a bucket named "audio"

..code:: console
    pip install --editable .

..code:: console
    audio-encode-server --config ./config.sample.json

..code:: console
    curl -X POST --data-binary @audio-dataset/banjo0.mp3  http://localhost:8080/api/transcode/v1/flac/banjo

transcoded file is in audio/banjo.flac
