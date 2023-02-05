import reactivex as rx
import reactivex.operators as ops
from reactivex.subject import Subject
import time

numbers1 = Subject()
numbers2 = Subject()

numbers1.pipe(
    ops.join(
        numbers2,
        lambda i: rx.just(True).pipe(ops.delay(200)),
        lambda i: rx.just(True).pipe(ops.delay(300)),
    ),
    ops.starmap(lambda i, j: i + j),
).subscribe(
        on_next=lambda i: print("on_next {}".format(i)),
        on_error=lambda e: print("on_error: {}".format(e)),
        on_completed=lambda: print("on_completed")
)

numbers1.on_next(0)
numbers2.on_next(2)
numbers1.on_next(1)
time.sleep(0.4)
numbers1.on_next(2)
numbers2.on_next(5)
time.sleep(0.25)
numbers1.on_next(3)
numbers2.on_next(3)
