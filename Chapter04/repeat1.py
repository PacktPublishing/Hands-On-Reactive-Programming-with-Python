import rx
import rx.operators as ops

ones = rx.just(1).pipe(ops.repeat(5))
ones.subscribe(
    on_next=lambda i: print("item: {}".format(i)),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)
