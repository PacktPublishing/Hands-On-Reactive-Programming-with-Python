from rx import Observable
from rx.subjects import Subject

obs1 = Subject()
obs2 = Subject()
obs3 = Subject()
higher_order = Subject()

higher_order.switch_latest().subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)

higher_order.on_next(obs1)
obs1.on_next("1: 1")
obs1.on_next("1: 2")
higher_order.on_next(obs2)
obs1.on_next("1: 3")
obs2.on_next("2: 1")
obs2.on_next("2: 2")
higher_order.on_next(obs3)
obs2.on_next("2: 3")
obs3.on_next("3: 1")
obs3.on_next("3: 2")
