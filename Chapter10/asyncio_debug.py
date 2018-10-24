import asyncio
import time


async def do_something():    
    print("I do something")
    time.sleep(0.5)
    #await asyncio.sleep(0.5)
    print("Done")


loop = asyncio.get_event_loop()
#loop.set_debug(True)
loop.run_until_complete(do_something())
loop.stop()
loop.close()