from rx import Observable, Observer


class MyObserver(Observer):
    def on_next(self, item):
        print("on_next {}".format(item))

    def on_completed(self):
        print("on_completed")

    def on_error(self, error):
        print("on_error: {}".format(error))

numbers = Observable.from_([1, 2, 3])
numbers.subscribe(MyObserver())
