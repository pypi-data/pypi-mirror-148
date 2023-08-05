import toori
import argparse


def main():
    parser = argparse.ArgumentParser(description="Connect to an Iro server")

    parser.add_argument(
        "-a", "--addr", help="address of server to connect to", type=str, required=True
    )
    parser.add_argument("-p", "--port", help="server port to connect to", type=int)
    parser.add_argument("-f", "--filter", help="sniffing filter to use", type=str)
    parser.add_argument(
        "-t",
        "--transports",
        help="socketIO transport method",
        type=str,
        choices=["websocket", "polling"],
    )
    args = parser.parse_args()

    cli = toori.TooriClient(args.addr, args.port, args.filter, args.transports)
    cli.start()
