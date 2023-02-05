import reactivex as rx
import reactivex.operators as ops

numbers = rx.from_([1, 2, 3, 4])

numbers.pipe(ops.count(lambda i: i > 2)).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
