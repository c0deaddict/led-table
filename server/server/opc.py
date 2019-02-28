# Open Pixel Control
import asyncio

from .settings import HOST, OPC_PORT
from .log import logger


class UdpServer(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None
        self.received = asyncio.Queue(10)

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)

        try:
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

    async def handle_tcp_message(self, reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        print("Send: %r" % message)
        writer.write(data)
        await writer.drain()

        print("Close the client socket")
        writer.close()

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


udp_server = UdpServer()
tcp_server = TcpServer()
