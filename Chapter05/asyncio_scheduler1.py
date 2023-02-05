import reactivex as rx
import reactivex.operators as ops
from reactivex.scheduler.eventloop import AsyncIOScheduler
import threading
import asyncio
import threading

loop = asyncio.new_event_loop()
asyncio_scheduler = AsyncIOScheduler(loop=loop)
numbers = rx.from_([1, 2, 3, 4], scheduler=asyncio_scheduler)

subscription = numbers.pipe(
    ops.map(lambda i: i*2),
    ops.map(lambda i: "number is: {}".format(i)),
).subscribe(
    on_next=lambda i: print("on_next({}) {}"
                            .format(threading.get_ident(), i)),
    on_error=lambda e: print("on_error({}): {}"
                             .format(threading.get_ident(), e)),
    on_completed=lambda: print("on_completed({})"
                               .format(threading.get_ident()))
)

print("starting event loop")
loop.run_forever()
loop.close()
