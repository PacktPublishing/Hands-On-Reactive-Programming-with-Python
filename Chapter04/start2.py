import rx
from rx.scheduler.eventloop import AsyncIOScheduler
import threading
import asyncio


def foo():
    print("foo from {}".format(threading.get_ident()))
    return 2


loop = asyncio.get_event_loop()
done = loop.create_future()
scheduler = AsyncIOScheduler(loop=loop)

number = rx.start(foo, scheduler=scheduler)
print("subscribing...")
number.subscribe(
    lambda i: print("on_next: {} from {}".format(i, threading.get_ident())),
    lambda e: print("on_error: {}".format(e)),
    lambda: done.set_result(0)
)

print("staring mainloop from {}".format(threading.get_ident()))
loop.run_until_complete(done)
loop.close()
