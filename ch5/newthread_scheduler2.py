from rx import Observable
from rx.concurrency import NewThreadScheduler
import threading
import time

new_thread_scheduler = NewThreadScheduler()
numbers = Observable.from_([1, 2, 3, 4])

subscription = numbers \
    .map(lambda i: i*2) \
    .observe_on(new_thread_scheduler) \
    .map(lambda i: "number is: {}".format(i)) \
    .subscribe(
        on_next=lambda i: print("on_next({}) {}"
            .format(threading.get_ident(), i)),
        on_error=lambda e: print("on_error({}): {}"
            .format(threading.get_ident(), e)),
        on_completed=lambda: print("on_completed({})"
            .format(threading.get_ident()))
    )

print("main({})".format(threading.get_ident()))
time.sleep(1.0)
