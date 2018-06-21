import asyncio
from aiohttp import web
from rx import Observable, AnonymousObservable
from rx.subjects import Subject

def http_driver(sink, loop):
    app = None
    runner = None

    def on_subscribe(observer):
        def add_route(app, methods, path):
            async def on_request_data(request, path):
                data = await request.read()
                response_future = asyncio.Future()
                request_item = {
                    'method': request.method,
                    'path': path,
                    'match_info': request.match_info,
                    'data': data,
                    'context': response_future,
                }
                observer.on_next(request_item)
                await response_future
                data, status = response_future.result()

                response = web.StreamResponse(status=status, reason=None)
                await response.prepare(request)
                if data is not None:
                    await response.write(data)
                return response

            for method in methods:
                app.router.add_route(method, path, lambda r: on_request_data(r, path))

        def start_server(host, port, app):
            runner = web.AppRunner(app)

            async def _start_server(runner):
                await runner.setup()
                site = web.TCPSite(runner, host, port)
                await site.start()

            loop.create_task(_start_server(runner))
            return runner

        def stop_server(runner):
            async def _stop_server():
                await runner.cleanup()

            loop.create_task(_stop_server())

        def on_sink_item(i):
            nonlocal runner
            if i['what'] == 'response':
                response_future = i['context']
                response_future.set_result((i['data'], i['status']))
            elif i['what'] == 'add_route':
                add_route(app, i['methods'], i['path'])
            elif i['what'] == 'start_server':
                runner = start_server(i['host'], i['port'], app)
            elif i['what'] == 'stop_server':
                stop_server(runner)

        def on_sink_error(e):
            observer.on_error(e)

        def on_sink_completed():
            observer.on_completed()

        app = web.Application()
        sink.subscribe(
            on_next=on_sink_item,
            on_error=on_sink_error,
            on_completed=on_sink_completed)

    return AnonymousObservable(on_subscribe)


def echo_server(source):
    init = Observable.from_([
        {
            'what': 'add_route',
            'methods': ['GET'],
            'path': '/echo/{what}',
        }, {
            'what': 'start_server',
            'host': 'localhost',
            'port': 8080
        }
    ])

    echo = source['http'] \
        .map(lambda i: {
            'what': 'response',
            'status': 200,
            'context': i['context'],
            'data': i['match_info']['what'].encode('utf-8'),
        })

    return {
        'http': Observable.merge(init, echo),
    }


def main():
    loop = asyncio.get_event_loop()
    http_proxy = Subject()
    sources = {
        'http': http_driver(http_proxy, loop),
    }

    sinks = echo_server(sources)
    sinks["http"].subscribe(http_proxy)

    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()
