from rx import Observable
from rx.subjects import Subject
import datetime
import time
from rx.disposables import AnonymousDisposable


def resource():
    print("create resource at {}".format(datetime.datetime.now()))

    def dispose():
        print("dispose resource at {}".format(datetime.datetime.now()))

    return AnonymousDisposable(dispose)


Observable.using(resource,
    lambda r: Observable.just(1).delay(200)).subscribe(
        on_next = lambda i: print("on_next {}".format(i)),
        on_error = lambda e: print("on_error: {}".format(e)),
        on_completed = lambda: print("on_completed")
)
time.sleep(500)
