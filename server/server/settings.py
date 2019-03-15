from datetime import time, timedelta

BASE_URL = 'http://led-table'
HOST = '0.0.0.0'
OPC_PORT = 1337
WEB_PORT = 8080

WIDTH = 15
HEIGHT = 15

DISPLAY_IMPL = 'server.leds.neo'

CLAIM_EXPIRE = timedelta(seconds=15)

# Table is powered on in this time window (from 08:00 until 18:00).
SCHEDULE_ON_TIME = [time(8, 0, 0), time(18, 0, 0)]

# Powered off during the weekends and on (Dutch) holidays.
SCHEDULE_ON_WEEKENDS = False
SCHEDULE_ON_HOLIDAYS = False

# Run each program for this amount of time.
SCREENSAVER_CHANGE = timedelta(seconds=15)

# Screensaver is enabled this percentage of the time,
# in windows of a minimum amount of time.
SCREENSAVER_ON_CHANCE = 0.1
SCREENSAVER_ON_MIN_WINDOW = timedelta(minutes=6)
