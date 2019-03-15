# Open Pixel Control
import asyncio

from .log import logger
from .utils import chunks
from .settings import HOST, OPC_PORT, WIDTH
from .scheduler import scheduler
from .leds import display


async def do_paint(client_id, frame):
    if await scheduler.claim(client_id):
        if await display.paint(frame):
            return 'painted'
        else:
            return 'dropped'
    else:
        return 'denied'


class ParseError(Exception):
    pass


def parse_frame(data):
    if len(data) < 4:
        raise ParseError('message too short')

    channel = data[0]
    command = data[1]
    length = (data[2] << 8) | data[3]
    payload = data[4:]

    if len(payload) != length:
        raise ParseError('expected {0} bytes, received {1}'.format(length, len(payload)))

    frame = dict()

    if command == 0:
        # Set 8 bit pixel colors
        for i, (r, g, b) in enumerate(chunks(payload, 3)):
            x = i % WIDTH
            y = i // WIDTH
            frame[(x,y)] = (r, g, b)

    elif command == 1:
        for x, y, r, g, b in chunks(payload, 5):
            frame[(x,y)] = (r, g, b)

    else:
        raise ParseError('unknown command: {0}'.format(command))

    return frame


class UdpServer(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        client_id = 'udp://{0}:{1}'.format(*addr)
        try:
            frame = parse_frame(data)
        except ParseError:
            logger.exception('Error parsing frame from {0}'.format(client_id))
        else:
            asyncio.ensure_future(do_paint(client_id, frame))

    def error_received(self, exc):
        pass

    async def start(self):
        loop = asyncio.get_event_loop()
        self.transport, protocol = await loop.create_datagram_endpoint(
            lambda: self, local_addr=(HOST, OPC_PORT))
        logger.info('Listening on UDP {0}:{1}'.format(HOST, OPC_PORT))

    async def stop(self):
        try:
            self.transport.close()
        finally:
            self.transport = None
            self.received = None
            logger.info('Closed UDP socket')


class TcpServer:
    def __init__(self):
        self.server = None

    async def start(self):
        self.server = await asyncio.start_server(
            self.handle_tcp_message, HOST, OPC_PORT)
        logger.info('Listening on TCP {0}:{1}'.format(HOST, OPC_PORT))

    async def stop(self):
        try:
            self.server.close()
            await self.server.wait_closed()
        finally:
            self.server = None
            logger.info('Closed TCP socket')

    async def handle_tcp_message(self, reader, writer):
        header = await reader.read(4)
        length = (header[2] << 8) | header[3]
        payload = await reader.read(length)

        addr = writer.get_extra_info('peername')
        client_id = 'tcp://{0}:{1}'.format(*addr)
        try:
            frame = parse_frame(header + payload)
        except ParseError:
            logger.exception('Error parsing frame from {0}'.format(client_id))
            resp = 'parse_error'
        else:
            resp = await do_paint(client_id, frame)

        writer.write((resp + '\n').encode())
        await writer.drain()
        writer.close()


udp_server = UdpServer()
tcp_server = TcpServer()
