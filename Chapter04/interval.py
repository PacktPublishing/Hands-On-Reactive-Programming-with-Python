from rx import Observable
import datetime
import time

ticks = Observable.interval(1000)
ticks.subscribe(
    on_next=lambda i: print("tick {} at {}".format(
        i, datetime.datetime.now())),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)

# wait to let some time for the timer to expire
time.sleep(5.0)
