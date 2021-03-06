import rx
import rx.operators as ops


numbers = rx.from_([1, 2, 3])
pub_numbers = numbers.pipe(
    ops.publish(),
    ops.ref_count()
)

pub_numbers.subscribe(
    on_next=lambda i: print("item: {}".format(i)),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)

pub_numbers.subscribe(
    on_next=lambda i: print("item: {}".format(i)),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)
