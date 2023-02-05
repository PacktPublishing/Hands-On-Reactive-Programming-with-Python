import reactivex as rx
import reactivex.operators as ops
from reactivex.subject import Subject


def wrap_items(i):
    return i.pipe(ops.map(lambda j: 'obs {}: {}'.format(i, j)))

numbers = rx.from_([1, 2, 3, 4, 5, 6])
numbers.pipe(
    ops.group_by(lambda i: i % 2 == 0),
    ops.flat_map(wrap_items),
).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
