from datetime import timedelta

BASE_URL = 'http://led-table'
HOST = '0.0.0.0'
OPC_PORT = 1337
WEB_PORT = 8080

WIDTH = 15
HEIGHT = 15

DISPLAY_IMPL = 'server.leds.fake'

CLAIM_EXPIRE = timedelta(minutes=5)

