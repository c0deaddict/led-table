import json
import asyncio

from aiohttp import web, WSCloseCode
import os

from aiohttp.web_fileresponse import FileResponse

from . import settings, leds
from .log import logger
from .request_logger import request_logger


event_queue = asyncio.Queue()


async def get_index(request):
    return web.HTTPFound(location='/static/index.html')


async def trigger_event(request):
    event = request.match_info['event']
    event_queue.put_nowait(event)
    await leds.paint(123)
    return web.Response(status=200, body='thank you come again')


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

app.on_shutdown.append(close_websockets)

app.router.add_get('/', get_index)
app.router.add_get('/event/{event}', trigger_event)
app.router.add_get('/ws', ws_handler)
# app.router.add_static('/static', '../web/')


def start():
    web.run_app(app, host=settings.HOST, port=settings.WEB_PORT)


async def broadcast(event):
    for ws in app['clients']:
        await ws.send_str(json.dumps(event))
