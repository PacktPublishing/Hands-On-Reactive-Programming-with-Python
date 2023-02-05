import reactivex as rx
import threading


def foo():
    print("foo from {}".format(threading.get_ident()))
    return 1

number = rx.start(foo)
print("subscribing...")
number.subscribe(
        on_next=lambda i: print("on_next: {} from {}".format(
            i, threading.get_ident())),
        on_error=lambda e: print("error: {}".format(e)),
        on_completed=lambda: print("completed")
    )
