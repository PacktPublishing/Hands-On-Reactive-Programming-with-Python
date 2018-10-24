from rx import Observable


err = Observable.throw("error!")
err.catch_exception(lambda e: Observable.from_([1, 2, 3])) \
    .subscribe(
        on_next=lambda i: print("item: {}".format(i)),
        on_error=lambda e: print("error: {}".format(e)),
        on_completed=lambda: print("completed")
    )
