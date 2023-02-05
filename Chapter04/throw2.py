import reactivex as rx

exception = rx.throw(NotImplementedError("I do nothing"))
exception.subscribe(
    on_next=lambda i: print("item: {}".format(i)),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)
