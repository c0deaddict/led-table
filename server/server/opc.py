# Open Pixel Control
import asyncio

from .log import logger
from .settings import HOST, OPC_PORT
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


class UdpServer(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None
        self.received = asyncio.Queue(10)

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        asyncio.ensure_future(do_paint(client_id, frame))
        # self.transport.sendto(data, addr)

        try:
            # TODO schedule a call to do_paint, don't return anything.
            self.received.put_nowait((data, addr))
        except asyncio.QueueFull:
            print(f'dropped packet size {len(data)} from {addr}')

    def error_received(self, exc):
        pass

    async def start(self):
        if self.transport is None:
            loop = asyncio.get_running_loop()
            self.transport, protocol = await loop.create_datagram_endpoint(
                lambda: self, local_addr=(HOST, OPC_PORT))
            logger.info(f'Listening on UDP {HOST}:{OPC_PORT}')

    async def stop(self):
        if self.transport:
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
        if self.server is None:
            self.server = await asyncio.start_server(
                self.handle_tcp_message, HOST, OPC_PORT)
            logger.info(f'Listening on TCP {HOST}:{OPC_PORT}')

    async def stop(self):
        if self.server:
            try:
                self.server.close()
                await self.server.wait_closed()
            finally:
                self.server = None
                logger.info('Closed TCP socket')

    async def handle_tcp_message(self, reader, writer):
        data = await reader.read(100)
        addr = writer.get_extra_info('peername')
        client_id = ('tcp', addr)
        frame = dict()
        resp = await do_paint(client_id, frame)
        writer.write(resp)
        await writer.drain()
        writer.close()


udp_server = UdpServer()
tcp_server = TcpServer()
