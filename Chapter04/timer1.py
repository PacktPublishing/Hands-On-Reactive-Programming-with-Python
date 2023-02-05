import reactivex as rx
import datetime
import time

print("starting at {}".format(datetime.datetime.now()))
one_shot = rx.timer(1.0)
one_shot.subscribe(
        on_next=lambda i: print("tick {} at {}".format(
            i, datetime.datetime.now())),
        on_error=lambda e: print("error: {}".format(e)),
        on_completed=lambda: print("completed")
)

# wait to let some time for the timer to expire
time.sleep(2.0)
