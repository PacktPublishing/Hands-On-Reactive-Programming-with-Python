from collections import namedtuple
from rx import Observable
from cyclotron import Component
import asyncio

Sink = namedtuple('Sink', ['request'])
Source = namedtuple('Source', ['response'])

# Sink items
Listen = namedtuple('Listen', ['host', 'port'])
Write = namedtuple('Write', ['id', 'data'])

# Source items
Connection = namedtuple('Connection', ['id', 'observable'])
Data = namedtuple('Data', ['data'])


def make_driver(loop=None):
    loop = loop or asyncio.get_event_loop()

    def driver(sink):
        def on_subscribe(observer):
            async def client_connected(reader, writer):
                def on_connection_subscribe(observer, reader, writer):
                    async def handle_connection(observer, reader, writer):
                        while True:
                            try:
                                data = await reader.read(100)
                                if data == b'':
                                    break
                                loop.call_soon(observer.on_next, Data(data=data))
                            except Exception as e:
                                loop.call_soon(observer.on_error(e))
                                break

                        loop.call_soon(observer.on_completed)
                        writer.close()

                    asyncio.ensure_future(handle_connection(observer, reader, writer))

                connection = Observable.create(lambda o: on_connection_subscribe(o, reader, writer))
                observer.on_next(Connection(
                    id=writer,
                    observable=connection))

            async def listen(host, port, handler):
                try:
                    await asyncio.start_server(handler, host, port, loop=loop)
                except Exception as e:
                    loop.call_soon(observer.on_error(e))

            async def write(writer, data):
                writer.write(data)

            def on_next(i):
                if type(i) is Listen:
                    asyncio.ensure_future(listen(i.host, i.port, client_connected))
                elif type(i) is Write:
                    asyncio.ensure_future(write(i.id, i.data))

            sink.request.subscribe(
                on_next=on_next,
                on_completed=observer.on_completed,
                on_error=observer.on_error
            )



        return Source(response=Observable.create(on_subscribe))

    return Component(call=driver, input=Sink)
