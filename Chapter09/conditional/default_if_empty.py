import reactivex as rx
import reactivex.operators as ops

empty = rx.empty()

empty.pipe(ops.default_if_empty("default")).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
