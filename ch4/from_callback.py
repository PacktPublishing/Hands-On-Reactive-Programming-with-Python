from rx import Observable


def foo(what, handler):
    print("foo: {}".format(what))
    handler("hello " + what)

callback = Observable.from_callback(foo)
cbk_obs = callback("world")
print("subscribing...")
cbk_obs.subscribe(
    on_next=lambda i: print("item: {}".format(i)),
    on_error=lambda e: print("error: {}".format(e)),
    on_completed=lambda: print("completed")
)
