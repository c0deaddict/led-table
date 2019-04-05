import json
import asyncio

from aiohttp import web, WSCloseCode
import os

from aiohttp.web_fileresponse import FileResponse

from . import settings, leds
from .log import logger
from .request_logger import request_logger
from .scheduler import scheduler
from .screensaver import Screensaver, programs


async def _start_screensaver(app, prog):
    s = app['active_screensaver']
    if s is not None:
        logger.info('Stopping current screensaver program')
        await s.stop()
    s = Screensaver(prog)
    app['active_screensaver'] = s
    await s.start()


async def get_index(request):
    return web.HTTPMovedPermanently(location='/static/index.html')


async def run_screensaver_program(request):
    prog_name = request.match_info['program']
    Prog = programs.get(prog_name)
    if Prog is None:
        return web.Response(status=404, body='program not found')

    client_id = 'http://{0}'.format(request.remote)
    # TODO claim without a timeout.
    # ... or: subscribe to the timeout and stop the screensaver.
    if not await scheduler.claim(client_id):
        return web.Response(status=400, body='could not claim display')

    await _start_screensaver(request.app, Prog())
    return web.Response(status=200, body='thank you come again')


async def request_shutdown(request):
    return web.Response(status=200, body='initiating shutdown')


async def ws_handler(request):
    ws = web.WebSocketResponse(protocols=('led-table',))
    await ws.prepare(request)

    request.app['clients'].append(ws)

    try:
        async for msg in ws:
            logger.info('Message received: {}'.format(msg))
            if msg.data == 'ping':
                await ws.send_str(json.dumps('pong'))
    finally:
        request.app['clients'].remove(ws)

    return ws


async def close_websockets(app):
    for ws in app['clients']:
        await ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')


app = web.Application(middlewares=[
    request_logger(logger),
])

app['clients'] = []
app['active_screensaver'] = None

app.on_shutdown.append(close_websockets)

app.router.add_get('/', get_index)
app.router.add_static('/static', 'static/')

# TODO make this POST when final!
app.router.add_get('/screensaver/run/{program}', run_screensaver_program)
app.router.add_get('/shutdown', request_shutdown)

app.router.add_get('/ws', ws_handler)


def start():
    web.run_app(app, host=settings.HOST, port=settings.WEB_PORT)


async def broadcast(event):
    for ws in app['clients']:
        await ws.send_str(json.dumps(event))
