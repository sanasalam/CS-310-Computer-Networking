#!/usr/bin/env python3
import ssl
import argparse
import socket
from pathlib import Path

FILE_DIR: Path = Path(__file__).parent.resolve()
HOST: str = "localhost"


def create_ssl_context() -> ssl.SSLContext:
    # TODO: Create an SSL context. Do not forget to disable security properties.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def create_client_ssl_socket(ctx: ssl.SSLContext, host_ip: str) -> ssl.SSLSocket:
    # TODO: Wrap the socket using the SSL context.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket = ctx.wrap_socket(sock, server_hostname = host_ip);

    return client_socket


def launch_client(server_port: int) -> None:
    # TODO: Create an SSL context.
    ctx = create_ssl_context()
    # TODO: Create an SSL client socket.
    client_socket = create_client_ssl_socket(ctx, HOST)
    # TODO: Connect to the server and send an encrypted SSL message.
    client_socket.connect((HOST, server_port))
    msg = b"This message is encrypted with SSL."
    client_socket.send(msg)
    # TODO: Do not forget to close the socket.
    client_socket.close()

def main(args):
    launch_client(args.server_port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--server-port",
        default="8000",
        type=int,
        help="The port the client will connect to.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
