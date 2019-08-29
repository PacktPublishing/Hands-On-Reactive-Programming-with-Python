import rx
import rx.operators as ops
from rx.core.notification import OnNext, OnCompleted

numbers = rx.from_([
    OnNext(1), OnNext(2),
    OnNext(3), OnNext(4),
    OnCompleted()])

numbers.pipe(ops.dematerialize()).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
