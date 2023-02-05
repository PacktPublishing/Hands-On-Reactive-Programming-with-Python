import reactivex as rx
from reactivex import operators as ops


err = rx.throw("error!")
err.pipe(
    ops.catch(rx.from_([1, 2, 3]))
).subscribe(
    on_next=lambda i: print("item: {}".format(i)),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)
