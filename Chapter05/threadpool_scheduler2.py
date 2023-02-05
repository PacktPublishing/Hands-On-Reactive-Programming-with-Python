import reactivex as rx
import reactivex.operators as ops
from reactivex.scheduler import ThreadPoolScheduler
import threading
import time

threadpool_scheduler = ThreadPoolScheduler()
numbers = rx.from_([1, 2, 3, 4])

subscription = numbers.pipe(
    ops.map(lambda i: i*2),
    ops.observe_on(threadpool_scheduler),
    ops.map(lambda i: "number is: {}".format(i)),
).subscribe(
        on_next=lambda i: print("on_next({}) {}"
                                .format(threading.get_ident(), i)),
        on_error=lambda e: print("on_error({}): {}"
                                 .format(threading.get_ident(), e)),
        on_completed=lambda: print("on_completed({})"
                                   .format(threading.get_ident()))
    )

print("main({})".format(threading.get_ident()))
time.sleep(1.0)
