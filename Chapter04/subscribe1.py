import rx
from rx.core import Observer


class MyObserver(Observer):
    def on_next(self, item):
        print("on_next {}".format(item))

    def on_completed(self):
        print("on_completed")

    def on_error(self, error):
        print("on_error: {}".format(error))

numbers = rx.from_([1, 2, 3])
numbers.subscribe(MyObserver())
