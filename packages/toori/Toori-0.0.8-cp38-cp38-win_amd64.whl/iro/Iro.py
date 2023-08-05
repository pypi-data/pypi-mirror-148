import iro
import argparse


def main():
    parser = argparse.ArgumentParser(description="Host an Iro server")

    parser.add_argument(
        "-a", "--addr", help="address to host on", type=str, required=False
    )
    parser.add_argument("-p", "--port", help="port to listen on", type=int)
    parser.add_argument("-f", "--filter", help="sniffing filter to use", type=str)
    parser.add_argument("-c", "--cert", help="SSL cert path", type=str)
    parser.add_argument("-k", "--key", help="SSL key path", type=str)
    args = parser.parse_args()

    iro.start(args.addr, args.port, args.filter, args.cert, args.key)
