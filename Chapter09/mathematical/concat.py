from rx import Observable

numbers1 = Observable.from_([1, 2, 3, 4])
numbers2 = Observable.from_([11, 12])

numbers1.concat(numbers2).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
