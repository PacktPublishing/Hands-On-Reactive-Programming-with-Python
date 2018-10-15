from rx import Observable


def on_subscribe(observer):
    observer.on_next(1)
    observer.on_next(2)
    observer.on_next(3)
    observer.on_completed()


numbers = Observable.create(on_subscribe)
numbers.subscribe(
    on_next=lambda i: print("item: {}".format(i)),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)
