from rx import Observable


def sum_even(source):
    def on_subscribe(observer):
        accumulator = 0

        def on_next(i):
            nonlocal accumulator
            if i % 2 == 0:
                accumulator += i
            else:
                observer.on_next(accumulator)
                accumulator = i

        def on_error(e):
            observer.on_error()

        def on_completed():
            nonlocal accumulator
            observer.on_next(accumulator)
            observer.on_completed()

        source.subscribe(on_next, on_error, on_completed)

    return Observable.create(on_subscribe)


numbers = Observable.from_([2, 2, 4, 5, 2])
sum_even(numbers).subscribe(
    on_next=lambda i: print("item: {}".format(i)),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)
