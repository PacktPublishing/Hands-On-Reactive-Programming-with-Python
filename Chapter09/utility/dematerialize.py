from rx import Observable
from rx.core.notification import OnNext, OnCompleted

numbers = Observable.from_([
    OnNext(1), OnNext(2),
    OnNext(3), OnNext(4),
    OnCompleted()])

numbers.dematerialize().subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
