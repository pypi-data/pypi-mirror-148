"""
色
"""

from engineio.payload import Payload
import socketio
from aiohttp import web
import asyncio
import ssl
from scapy.all import (
    IP,
    TCP,
    AsyncSniffer,
    conf,
    get_if_addr,
    UDP,
)

# Can be generic because most packets are filtered on the client side
sniff_filter = "tcp and (src port 80 or src port 443)"

# Prevents crashing when overloaded
Payload.max_decode_packets = 250000

# Local IP of the server
LOCAL_IP = get_if_addr(conf.iface)

# Set to whitelist dst IPs initiated by client
dest_whitelist = set()

# L3 socket object for Scapy to reuse
scapy_l3_socket = conf.L3socket()

# Ping timeout prevents client from disconnecting when there is a delay
sio = socketio.AsyncServer(
    async_mode="aiohttp", ping_timeout=9999, serializer="default"
)

app = web.Application()
sio.attach(app)


async def handleInboundPacket(pkt):
    try:
        # Get packet from IP layer onwards and send to client
        packet_inbound = pkt[IP]
    except IndexError:
        return

    # Skip packet if it is not a reply to the client
    if packet_inbound[IP].src not in dest_whitelist:
        return

    # packet_inbound.show()

    # Send packet to client
    await sio.emit(
        "ret",
        bytes(packet_inbound),
    )


# Sniff for returning inbound packets in the background
async def background_task():
    sniffer = AsyncSniffer(
        filter=sniff_filter,
        store=False,
        prn=lambda pkt: asyncio.run(handleInboundPacket(pkt)),
    )
    print(f"Sniffing with filter ({sniff_filter})")
    sniffer.start()


# Listen for messages on "out" event
@sio.on("out")
async def handleOutboundPacket(sid, data):
    packet_outbound = IP(data)
    # packet_outbound.show()

    # Change packet source IP to server's local IP
    packet_outbound[IP].src = LOCAL_IP

    # Whitelist st IP to allow returning packet
    dest_whitelist.add(packet_outbound[IP].dst)

    # Force recalculaton of layer checksums
    if packet_outbound.haslayer(IP):
        del packet_outbound[IP].chksum
    if packet_outbound.haslayer(TCP):
        del packet_outbound[TCP].chksum
    if packet_outbound.haslayer(UDP):
        del packet_outbound[UDP].chksum

    scapy_l3_socket.send(packet_outbound)


# On client connect
@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")

    # Clear whitelist
    global dest_whitelist
    dest_whitelist.clear()


# On client disconnect
@sio.event
def disconnect(sid):
    print(f"Client {sid} disconnected")

    # Clear whitelist
    global dest_whitelist
    dest_whitelist.clear()


# Start background task and initialize
async def init_app():
    sio.start_background_task(background_task)
    return app


def start(host, port, filter=None, ssl_cert_path=None, ssl_key_path=None):
    ssl_context = None

    # "/etc/letsencrypt/live//fullchain.pem"
    # "/etc/letsencrypt/live//privkey.pem"
    if ssl_cert_path and ssl_key_path:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(ssl_cert_path, ssl_key_path)

    if not host:
        host = "0.0.0.0"
    if not port:
        port = 443

    if filter:
        global sniff_filter
        sniff_filter = filter

    web.run_app(init_app(), host=host, port=port, ssl_context=ssl_context)


if __name__ == "__main__":
    # Debug
    start("localhost", 8080)
