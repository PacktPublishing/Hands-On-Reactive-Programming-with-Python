import asyncio
import aionotify

# Setup the watcher
watcher = aionotify.Watcher()
watcher.watch(alias='test', path='/tmp/foo.txt', flags=
    aionotify.Flags.ACCESS | aionotify.Flags.MODIFY | aionotify.Flags.OPEN | aionotify.Flags.CLOSE_WRITE)

# Prepare the loop
loop = asyncio.get_event_loop()

async def work():
    await watcher.setup(loop)
    for _ in range(10):
        event = await watcher.get_event()
        print(event)
    watcher.close()

loop.run_until_complete(work())
loop.stop()
loop.close()
watcher.unwatch('/tmp/foo.txt')
