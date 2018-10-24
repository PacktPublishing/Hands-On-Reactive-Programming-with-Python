from rx import Observable

numbers = Observable.from_([1, 2, 3])
numbers.repeat(3).subscribe(
    on_next=lambda i: print("item: {}".format(i)),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)
