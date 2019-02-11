import sys
import colorsys

from base import *

OFF = Color(0, 0, 0)
GREEN = Color(0, 255, 0)
YELLOW = Color(255, 255, 0)
RED = Color(255, 0, 0)
DARK_GREEN = Color(0, 128, 0)
DARK_YELLOW = Color(128, 128, 0)
DARK_RED = Color(128, 0, 0)

MAX_LEVEL = 1000
BAR_HEIGHT = HEIGHT
NUM_BARS = WIDTH
BAR_COLORS = [GREEN] * 7 + [YELLOW] * 5 + [RED] * 3


def hsv2rgb(h, s, v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def hsv2color(h, s, v):
    return Color(*hsv2rgb(h, s, v))


def striped_bar_color(bar, strength):
    if bar % 2 == 0:
        if strength < 6:
            return GREEN
        elif strength < 12:
            return YELLOW
        else:
            return RED
    else:
        if strength < 7:
            return DARK_GREEN
        elif strength < 12:
            return DARK_YELLOW
        else:
            return DARK_RED


def gradient_bar_color(bar, strength):
    if strength < 6:
        return Color(0, 64 + strength * 31, 0)
    elif strength < 12:
        value = 64 + (strength - 6) * 31
        return Color(value, value, 0)
    else:
        value = 64 + (strength - 12) * 63
        return Color(value, 0, 0)


def fancy_bar_color(bar, strength):
    return hsv2color(
        (strength + 1) / 15.0,
        1.0 - ((bar + 1) / 60.0),
        0.5 + ((bar + 1) / 30.0))


bar_color_fn = striped_bar_color  # fancy_bar_color


def clamp(value):
    if value < 0:
        return 0
    elif value > MAX_LEVEL:
        return MAX_LEVEL
    else:
        return value


def to_bar(value):
    return int(round((value / float(MAX_LEVEL)) * BAR_HEIGHT))


current_bars = [0] * 15


def draw_bar(bar, height):
    global current_bars
    current_height = current_bars[bar]
    if height < current_height:
        for i in range(height, current_height):
            yield (bar, i), OFF
    elif height > current_height:
        for i in range(current_height, height):
            yield (bar, i), bar_color_fn(bar, i)
    current_bars[bar] = height


def main():
    send_reset()
    for line in iter(sys.stdin.readline, ''):
        try:
            values = [to_bar(clamp(int(val))) for val in line.split(';')[0:-1]]
            if len(values) > NUM_BARS:
                print('Too much values received: ', len(values))
            else:
                updates = []
                for bar, height in enumerate(values):
                    updates.extend(draw_bar(bar, height))
                send_updates(updates)
        except ValueError as e:
            print(e)
            pass


if __name__ == '__main__':
    main()

