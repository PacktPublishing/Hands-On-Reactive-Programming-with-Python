import reactivex as rx
import reactivex.operators as ops

numbers = rx.from_([11, 12, 13, 14])

numbers.pipe(ops.all(lambda i: i > 10)).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
