from rx import Observable
from rx.subjects import Subject

numbers = Subject()
trigger = Subject()

numbers.take_until(trigger).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)

numbers.on_next(1)
numbers.on_next(2)
trigger.on_next(True)
numbers.on_next(3)
numbers.on_next(4)
numbers.on_completed()
