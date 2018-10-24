from rx import Observable
import datetime
import time

numbers = Observable.just(1)

print("{}".format(datetime.datetime.now()))
numbers.delay(200).subscribe(
    on_next=lambda i: print("on_next {}: {}".format(
        i, datetime.datetime.now())),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
time.sleep(0.5)
