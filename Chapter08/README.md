# Chapter 08

## Audio Encode Server

### Setup

First ensure that a minio instance is running:

```console
$ mkdir /tmp/minio
$ mkdir /tmp/minio/config
$ mkdir /tmp/minio/data
$ docker run -d -p 9000:9000 --name minio -v /tmp/minio/data:/data -v /tmp/minio/config:/root/.minio -e "MINIO_ACCESS_KEY=P0B76GIFPB6T0OD5I67U" -e "MINIO_SECRET_KEY=3+kGshnhQ7i41UabvMz8buqUKgtGsikmdL1Q+oDR"  minio/minio server /data
```

Then create a bucket named "audio" from the web UI of minio. You can access it from the "http://localhost:9000" url on a web browser.

### Execute

start the audio encoder server:

```console
(venv-rx)$ audio-encode-server --config config.sample.json
```

from another console, in the audio-dataset directory, send an encoding request:

```
curl -X POST --data-binary @banjo1.mp3 http://localhost:8080/api/transcode/v1/flac/banjo1
```