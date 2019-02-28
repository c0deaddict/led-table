import asyncio

from . import opc, web, leds
from .log import logger


services = [
    opc.udp_server,
    opc.tcp_server,
    leds,
]


def run():
    try:
        def invoke(fn):
            return lambda _: fn()

        web.app.on_startup.extend([invoke(s.start) for s in services])
        web.app.on_shutdown.extend(reversed([invoke(s.stop) for s in services]))

        web.start()
    except Exception as ex:
        logger.exception(ex)
    finally:
        # teardown
        pass
