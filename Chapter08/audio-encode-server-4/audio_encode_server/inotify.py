from collections import namedtuple
import asyncio
import aionotify
from rx import Observable
from cyclotron import Component
import threading

Source = namedtuple('Source', ['response'])
Sink = namedtuple('Sink', ['request'])

# Sink objects
AddWatch = namedtuple('AddWatch', ['id', 'path', 'flags'])
Start = namedtuple('Start', [])

# Source objects
Event = namedtuple('Event', ['id', 'path'])

def make_driver(loop = None):
    loop = asyncio.get_event_loop() if loop is None else loop

    def driver(sink):

        def on_subscribe(observer):
            watcher = aionotify.Watcher()

            async def read_events():
                nonlocal observer
                await watcher.setup(loop)
                while True:                    
                    event = await watcher.get_event()
                    loop.call_soon(observer.on_next, Event(id=event.alias, path=event.name))
                watcher.close()

            def on_next(item):
                if type(item) is AddWatch:
                    watcher.watch(alias=item.id, path=item.path, flags=item.flags)
                        
                elif type(item) is Start:
                    asyncio.ensure_future(read_events())

                else:
                    observer.on_error("unknown item: {}".format(type(item)))

            sink.request.subscribe(
                on_next=on_next,
                on_error=lambda e: observer.on_error(e))

        return Source(
            response=Observable.create(on_subscribe)
        )


    return Component(call=driver, input=Sink)
