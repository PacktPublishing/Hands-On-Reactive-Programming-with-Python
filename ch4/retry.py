from rx import Observable


subscribe_count = 0


def on_subscribe(observer):
    global subscribe_count
    subscribe_count += 1
    if subscribe_count == 1:
        observer.on_next(1)
        observer.on_error("error!")
    else:
        observer.on_next(1)
        observer.on_next(2)
        observer.on_next(3)
        observer.on_completed()

err = Observable.create(on_subscribe)
err.retry(2) \
    .subscribe(
        on_next=lambda i: print("item: {}".format(i)),
        on_error=lambda e: print("error: {}".format(e)),
        on_completed=lambda: print("completed")
    )
