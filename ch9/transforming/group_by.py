from rx import Observable
from rx.subjects import Subject


def wrap_items(i):
    return i.map(lambda j: 'obs {}: {}'.format(i, j))

numbers = Observable.from_([1, 2, 3, 4, 5, 6])
numbers.group_by(lambda i: i % 2 == 0).flat_map(wrap_items).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
