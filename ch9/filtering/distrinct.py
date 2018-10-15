from rx import Observable

numbers = Observable.from_([1, 2, 1, 3, 3, 2, 4, 5])
numbers.distinct().subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
