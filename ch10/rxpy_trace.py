
from rx import Observable, Observer
import json
import traceback


class TraceObservable(Observer):
    def __init__(self, prefix):
        self.prefix = prefix

    def on_next(self, value):
        print("{} - on next: {}".format(self.prefix, value))

    def on_completed(self):
        print("{} - completed".format(self.prefix))

    def on_error(self, error):
        if isinstance(error, Exception):
            print("{} - on error: {}, {}".format(self.prefix,  error, traceback.print_tb(error.__traceback__)))
        else:
            print("{} - on error: {}".format(self.prefix,  error))


Observable.just('{ "foo": 2"}') \
    .do_action(TraceObservable("trace 1")) \
    .map(lambda i: json.loads(i)) \
    .do_action(TraceObservable("trace 2")) \
    .subscribe(
        on_next=lambda i: print("on_next: {}".format(i)),
        on_error=lambda e: print("on_error {}".format(e)),
        on_completed=lambda: print("completed")
    )
