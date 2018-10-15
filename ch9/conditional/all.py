from rx import Observable

numbers = Observable.from_([11, 12, 13, 14])

numbers.all(lambda i: i > 10).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
