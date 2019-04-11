import json
import asyncio

from aiohttp import web, WSCloseCode, WSMsgType
import os

from aiohttp.web_fileresponse import FileResponse

from . import settings, opc
from .log import logger
from .request_logger import request_logger
from .scheduler import scheduler
from .screensaver import Screensaver, programs
from .leds import display


async def _stop_screensaver(app):
    s = app['active_screensaver']
    if s is not None:
        logger.info('Stopping current screensaver program')
        await s.stop()
        app['active_screensaver'] = None


async def _start_screensaver(app, prog):
    await _stop_screensaver(app)
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


async def stop_screensaver(request):
    await _stop_screensaver(request.app)
    await display.reset()
    return web.Response(status=200, body='roger')


async def reset_display(request):
    await display.reset()
    return web.Response(status=200, body='ack')


async def request_shutdown(request):
    os.system('systemctl poweroff')
    return web.Response(status=200, body='initiating shutdown')


async def ws_handler(request):
    ws = web.WebSocketResponse(protocols=('led-table',))
    await ws.prepare(request)

    client_id = 'http://{0}'.format(request.remote)
    request.app['clients'].append(ws)

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                logger.info('Text message received: {}'.format(msg))
                if msg.data == 'ping':
                    await ws.send_str('pong')
            elif msg.type == WSMsgType.BINARY:
                # logger.info('Binary message received: {}'.format(msg))
                try:
                    frame = opc.parse_frame(msg.data)
                    result = await opc.do_paint(client_id, frame)
                except opc.ParseError:
                    logger.exception('WebSocket OPC parse error')
                    result = 'parse_error'
                await ws.send_str(result)
            elif msg.type == WSMsgType.ERROR:
                logger.error('WebSocket connection closed with exception:', ws.exception())
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

app.router.add_post('/screensaver/run/{program}', run_screensaver_program)
app.router.add_post('/screensaver/stop', stop_screensaver)
app.router.add_post('/display/reset', reset_display)
app.router.add_post('/shutdown', request_shutdown)

app.router.add_get('/ws', ws_handler)


def start():
    web.run_app(app, host=settings.HOST, port=settings.WEB_PORT)


async def broadcast(event):
    for ws in app['clients']:
        await ws.send_str(json.dumps(event))
