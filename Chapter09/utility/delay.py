import reactivex as rx
import reactivex.operators as ops
import datetime
import time

numbers = rx.just(1)

print("{}".format(datetime.datetime.now()))
numbers.pipe(ops.delay(0.2)).subscribe(
    on_next=lambda i: print("on_next {}: {}".format(
        i, datetime.datetime.now())),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
time.sleep(0.5)
