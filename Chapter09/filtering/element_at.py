import reactivex as rx
import reactivex.operators as ops

numbers = rx.from_([1, 2, 3, 4, 5, 6])
numbers.pipe(ops.element_at(3)).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
