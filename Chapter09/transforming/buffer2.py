from rx import Observable
from rx.subjects import Subject
import time
import threading

window_selector = None


def closing_selector():
    print("closing_selector")
    global window_selector
    window_selector = Subject()
    return window_selector


numbers = Subject()
numbers.buffer(closing_selector).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)

numbers.on_next(1)
numbers.on_next(2)
numbers.on_next(3)
window_selector.on_completed()
numbers.on_next(4)
numbers.on_next(5)
window_selector.on_completed()
