# Open Pixel Control
import asyncio

from .settings import HOST, OPC_PORT


class OpcUdpProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport
        self.received = asyncio.Queue(10)

    def datagram_received(self, data, addr):
        messgae = data.decode()
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)

        try:
            self.received.put_nowait((data, addr))
        except asyncio.QueueFull:
            print(f'dropped packet size {len(data)} from {addr}')

    def error_received(self, exc):
        pass


async def handle_tcp_message(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))

    print("Send: %r" % message)
    writer.write(data)
    await writer.drain()

    print("Close the client socket")
    writer.close()


udp_server = None
tcp_server = None


async def start_udp():
    if udp_server is None:
        loop = asyncio.get_running_loop()
        udp_server, protocol = await loop.create_datagram_endpoint(
            lambda: OpcUdpProtocol(), local_addr=(HOST, OPC_PORT))

async def stop_udp():
    if udp_server:
        try:
            udp_server.close()
            await udp_server.wait_closed()
        finally:
            udp_server = None


async def start_tcp():
    if tcp_server is None:
        tcp_server = await asyncio.start_server(
            handle_message, HOST, OPC_PORT)


async def stop_tcp():
    if tcp_server:
        try:
            tcp_server.close()
            await tcp_server.wait_closed()
        finally:
            tcp_server = None


async def start():
    await start_udp()
    await start_tcp()


async def stop():
    await stop_udp()
    await stop_tcp()
