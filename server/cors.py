import aiohttp_cors

CORS_CONFIG = aiohttp_cors.ResourceOptions(
    allow_credentials=True,
    allow_methods='*',
    allow_headers='*',
)
