import reactivex as rx
import reactivex.operators as ops
from reactivex.subject import Subject


def wrap_items(i):
    return i.pipe(ops.map(lambda j: 'obs {}: {}'.format(i, j)))

numbers = Subject()
windows = Subject()
numbers.pipe(
    ops.window(windows),
    ops.flat_map(wrap_items)
).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)

numbers.on_next(1)
numbers.on_next(2)

windows.on_next(True)
numbers.on_next(3)
numbers.on_next(4)
numbers.on_next(5)
windows.on_next(True)
