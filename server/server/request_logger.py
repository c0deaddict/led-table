from aiohttp import web


def request_logger(logger):
    @web.middleware
    async def logger_middleware(request, handler):
        logger.info('>> {} {}'.format(request.method, request.path))
        try:
            response = await handler(request)
            logger.info('<< {} {} {}'.format(request.method, request.path, response.status))
            return response
        except web.HTTPException as ex:
            logger.info('!! {} {} {}'.format(request.method, request.path, ex.status))
            raise ex

    return logger_middleware
