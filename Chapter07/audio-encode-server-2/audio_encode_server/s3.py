from collections import namedtuple
from io import BytesIO
import reactivex as rx
from boto3.session import Session

from cyclotron import Component

Source = namedtuple('Source', ['response'])
Sink = namedtuple('Sink', ['request'])

# Sink objects
Configure = namedtuple('Configure', [
    'access_key', 'secret_key',
    'bucket', 'endpoint_url', 'region_name'])

UploadObject = namedtuple('UploadObject', ['key', 'data', 'id'])

# Source objects
UploadReponse = namedtuple('UploadReponse', ['key', 'id'])


def make_driver():
    def driver(sink):

        def on_subscribe(observer, scheduler):
            client = None
            bucket = None

            def on_next(item):
                nonlocal client
                nonlocal bucket

                if type(item) is Configure:
                    session = Session(aws_access_key_id=item.access_key,
                                      aws_secret_access_key=item.secret_key)
                    client = session.client(
                        's3',
                        endpoint_url=item.endpoint_url,
                        region_name=item.region_name)
                    bucket = item.bucket

                elif type(item) is UploadObject:
                    data = BytesIO(item.data)
                    client.upload_fileobj(data, bucket, item.key)
                    observer.on_next(UploadReponse(
                        key=item.key,
                        id=item.id))

                else:
                    observer.on_error("unknown item: {}".format(type(item)))

            sink.request.subscribe(
                on_next=on_next,
                on_error=lambda e: observer.on_error(e),
                on_completed=lambda: observer.on_completed())

        return Source(
            response=rx.create(on_subscribe)
        )

    return Component(call=driver, input=Sink)
