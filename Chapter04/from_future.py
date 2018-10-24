from rx import Observable
import asyncio


async def foo(future):
    await asyncio.sleep(1)
    future.set_result(2)


loop = asyncio.get_event_loop()
done = loop.create_future()
asyncio.ensure_future(foo(done))

number = Observable.from_future(done)
print("subscribing...")
number.subscribe(
    lambda i: print("on_next: {}".format(i)),
    lambda e: print("on_error: {}".format(e)),
    lambda: print("on_completed")
)

print("staring mainloop")
loop.run_until_complete(done)
loop.close()
