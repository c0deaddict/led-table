import json

from aiohttp import web, WSCloseCode
import os

from aiohttp.web_fileresponse import FileResponse

from . import settings
from .log import logger
from .request_logger import request_logger


async def get_index(request):
    return web.HTTPFound(location='/static/index.html')


async def get_photo(request):
    filepath = os.path.join(settings.PHOTOS_ROOT,
                            request.match_info['album'],
                            request.match_info['name'])
    return FileResponse(filepath)


async def trigger_event(request):
    event = request.match_info['event']
    request.app['event_queue'].put_nowait(event)
    return web.Response(status=200, body='thank you come again')


async def ws_handler(request):
    ws = web.WebSocketResponse(protocols=('neon.display',))
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

app.on_response_prepare.append(hide_server_header)
app.on_shutdown.append(close_websockets)

app.router.add_get('/', get_index)
app.router.add_get('/photo/{album}/{name}', get_photo)
app.router.add_get('/event/{event}', trigger_event)
app.router.add_get('/ws', ws_handler)
app.router.add_static('/static', '../web/')


def start(event_queue):
    app['event_queue'] = event_queue
    web.run_app(app, host='0.0.0.0', port=8080)


async def broadcast(event):
    for ws in app['clients']:
        await ws.send_str(json.dumps(event))
