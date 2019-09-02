import rx
import rx.operators as ops
from rx.core import Observer
import json
import traceback


def trace(prefix):
    def _trace(source):
        def on_subscribe(observer, scheduler):
            def on_next(i):
                print("{} - on next: {}".format(prefix, i))
                observer.on_next(i)

            def on_error(e):
                if isinstance(e, Exception):
                    print("{} - on error: {}, {}".format(prefix,  e, traceback.print_tb(e.__traceback__)))
                else:
                    print("{} - on error: {}".format(prefix,  e))
                observer.on_error(e)

            def on_completed():
                print("{} - completed".format(prefix))
                observer.on_completed()

            source.subscribe(
                on_next=on_next,
                on_error=on_error,
                on_completed=on_completed
            )
        return rx.create(on_subscribe)

    return _trace


rx.just('{ "foo": 2"}').pipe(
    trace("trace 1"),
    ops.map(lambda i: json.loads(i)),
    trace("trace 2"),
).subscribe(
        on_next=lambda i: print("on_next: {}".format(i)),
        on_error=lambda e: print("on_error {}".format(e)),
        on_completed=lambda: print("completed")
    )
