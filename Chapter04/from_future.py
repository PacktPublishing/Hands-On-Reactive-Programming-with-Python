import reactivex as rx
import asyncio


async def foo(future):
    await asyncio.sleep(1)
    future.set_result(2)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
done = loop.create_future()
t = asyncio.ensure_future(foo(done), loop=loop)

number = rx.from_future(done)
print("subscribing...")
number.subscribe(
    lambda i: print("on_next: {}".format(i)),
    lambda e: print("on_error: {}".format(e)),
    lambda: print("on_completed")
)

print("staring mainloop")
loop.run_until_complete(t)
loop.close()
