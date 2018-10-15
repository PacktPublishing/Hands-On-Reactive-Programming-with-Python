from rx import Observable
from rx.subjects import Subject

first = Subject()
second = Subject()

first.amb(second).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)

first.on_next(1)
second.on_next(2)
first.on_completed()
