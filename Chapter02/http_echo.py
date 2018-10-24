import asyncio
from aiohttp import web

async def echo_handler(request):
    response = web.Response(text=request.match_info['what'])
    await response.prepare(request)
    return response

async def start_server(runner):
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

app = web.Application()
app.router.add_route('GET', '/echo/{what}', echo_handler)
runner = web.AppRunner(app)

loop = asyncio.get_event_loop()
loop.create_task(start_server(runner))

loop.run_forever()
loop.close()
