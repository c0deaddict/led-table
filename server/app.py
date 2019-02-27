import asyncio

from . import opc, web


def main():
    try:
        web.app.on_startup.extend([
            opc.start,
        ])

        web.app.on_shutdown.extend([
            opc.stop,
        ])

        web.start()
    except Exception as ex:
        logger.exception(ex)
    finally:
        # teardown
        pass
