from collections import namedtuple
from rx import Observable
from cyclotron import Component
import asyncio

Sink = namedtuple('Sink', ['request'])
Source = namedtuple('Source', ['response'])

# Sink items
Connect = namedtuple('Connect', ['host', 'port'])
Write = namedtuple('Write', ['id', 'data'])

# Source items
Connection = namedtuple('Connection', ['id', 'observable'])
Data = namedtuple('Data', ['data'])


def make_driver(loop=None):
    loop = loop or asyncio.get_event_loop()

    def driver(sink):        
        def on_subscribe(observer):
            async def tcp_client(host, port):
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

                try:
                    reader, writer = await asyncio.open_connection(
                        host, port, loop=loop)
                    connection = Observable.create(lambda o: on_connection_subscribe(o, reader, writer))
                    observer.on_next(Connection(
                        id=writer, 
                        observable=connection))                        
                except Exception as e:
                    loop.call_soon(observer.on_error(e))
                                

            async def write(writer, data):
                writer.write(data)

            def on_next(i):
                if type(i) is Connect:
                    asyncio.ensure_future(tcp_client(i.host, i.port))
                elif type(i) is Write:
                    asyncio.ensure_future(write(i.id, i.data))                    

            sink.request.subscribe(
                on_next=on_next,
                on_completed=observer.on_completed,
                on_error=observer.on_error
            )

        return Source(response=Observable.create(on_subscribe))

    return Component(call=driver, input=Sink)
