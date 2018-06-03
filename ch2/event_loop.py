import datetime
import asyncio

async def wait(delay):
    now = datetime.datetime.now()
    print("wait for {} seconds at {}:{}:{}".format(delay, now.hour, now.minute, now.second))
    await asyncio.sleep(delay)
    now = datetime.datetime.now()
    print("waited for {} seconds at {}:{}:{}".format(delay, now.hour, now.minute, now.second))
    return True

loop = asyncio.get_event_loop()
loop.run_until_complete(wait(2))
