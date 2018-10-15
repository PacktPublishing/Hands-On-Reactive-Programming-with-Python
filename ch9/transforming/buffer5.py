from rx import Observable
from rx.subjects import Subject
import time
import threading

numbers = Subject()
dispoable = numbers.buffer_with_time(200, timeshift=400).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)

numbers.on_next(1)
numbers.on_next(2)
t1 = threading.Timer(0.250, lambda: numbers.on_next(3))
t1.start()
t2 = threading.Timer(0.450, lambda: numbers.on_next(4))
t2.start()
t3 = threading.Timer(0.750, lambda: dispoable.dispose())
t3.start()
