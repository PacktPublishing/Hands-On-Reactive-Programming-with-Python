from rx import Observable


def create_numbers_observable(*args):
    return Observable.of(*args)

create_numbers_observable(1, 2, 3, 4).subscribe(
    on_next=lambda i: print("item: {}".format(i)),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)
