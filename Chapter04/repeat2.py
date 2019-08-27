import rx
import rx.operators as ops

numbers = rx.from_([1, 2, 3])
numbers.pipe(
    ops.repeat(3)
).subscribe(
    on_next=lambda i: print("item: {}".format(i)),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)
