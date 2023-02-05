import reactivex as rx
import reactivex.operators as ops
from reactivex.subject import Subject
import time

numbers = Subject()

numbers.pipe(ops.timestamp()).subscribe(
    on_next=lambda i: print("on_next {}: {}".format(i.value, i.timestamp)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)

numbers.on_next(1)
time.sleep(0.1)
numbers.on_next(2)
time.sleep(0.1)
numbers.on_next(3)
time.sleep(0.1)
numbers.on_next(4)
