#! /bin/sh

transcode_url="http://localhost:8080/api/transcode/v1/flac"
date
echo "encoding file 0"
curl -X POST --data-binary @banjo0.mp3 $transcode_url/banjo0 &
echo "encoding file 1"
curl -X POST --data-binary @banjo1.mp3 $transcode_url/banjo1 &
echo "encoding file 2"
curl -X POST --data-binary @banjo2.mp3 $transcode_url/banjo2 &
echo "encoding file 3"
curl -X POST --data-binary @banjo3.mp3 $transcode_url/banjo3 &
echo "encoding file 4"
curl -X POST --data-binary @banjo4.mp3 $transcode_url/banjo4 &
echo "encoding file 5"
curl -X POST --data-binary @banjo5.mp3 $transcode_url/banjo5 &
echo "encoding file 6"
curl -X POST --data-binary @banjo6.mp3 $transcode_url/banjo6 &
echo "encoding file 7"
curl -X POST --data-binary @banjo7.mp3 $transcode_url/banjo7 &
echo "encoding file 8"
curl -X POST --data-binary @banjo8.mp3 $transcode_url/banjo8 &
echo "encoding file 9"
curl -X POST --data-binary @banjo9.mp3 $transcode_url/banjo9 &

wait
date
echo "completed"
