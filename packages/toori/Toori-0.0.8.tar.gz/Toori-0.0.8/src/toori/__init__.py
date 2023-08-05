"""
通り
"""

from _toori import *  # Import all C++ functions

import socketio
from engineio.payload import Payload
from scapy.all import IP
import socket

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# from threading import Thread
# import time


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


class TooriClient:
    # Attempts WebSocket first, else fallback to polling
    def __init__(self, addr, port, filter, transports) -> None:
        if not addr:
            addr = "http://localhost"
        if not port:
            port = 443
        if not filter:
            filter = "tcp && tcp.DstPort == 443"

        # Increase the socketIO packet buffer
        Payload.max_decode_packets = 250000

        # Filter only outbound and non loopback
        filter = "outbound && !loopback && " + filter

        # Whitelist the Iro server
        server_ip = socket.gethostbyname(addr.split("//")[-1])
        filter += f" && ip.DstAddr != {server_ip}"

        transports_string = transports if transports else "auto"

        if not addr.startswith("http://") and not addr.startswith("https://"):
            if port == 443:
                addr = "https://" + addr
            else:
                addr = "http://" + addr

        # Initialize WinDivert injector
        init_inbound(get_ip_address())  # Interface address to replace
        print(f"WinDivert injector initialized")

        # Connect to socketIO server
        print(f"Connecting to server {addr}:{port} via {transports_string} transport")
        self.sio = socketio.Client(serializer="default", ssl_verify=False)
        self.sio.connect(f"{addr}:{port}", transports=transports)
        print(f"Connected to server")

        # Initialize WinDivert sniffer
        init_outbound(filter)
        print(f"WinDivert sniffer initialized")
        print(f"Sniffing with filter ({filter})")

    def send_outbound(self, data):
        try:
            self.sio.emit("out", data)
        except socketio.exceptions.BadNamespaceError:
            # Reconnect
            return

    def inbound_handler(self):
        @self.sio.on("ret")
        def inject(data):
            inboundPacket = IP(
                bytes(data)
            )  # Might not be needed, or use for error checking
            inject_once(bytes(inboundPacket))

    def start(self):
        # Thread(target=self.handle_inbound_thread, args=()).start() # Not required

        print(f"Starting socketIO inbound handler")
        self.inbound_handler()

        print(f"Starting WinDivert outbound sniffer")
        # Outbound sniffer loop
        while True:
            # time.sleep(0.1)  # Temp fix
            self.send_outbound(recv_once())
