from rx import Observable

numbers = Observable.from_([1, 2, 3, 4])

numbers.materialize().subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
