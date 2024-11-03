#!/usr/bin/env python3
import ssl
import argparse
from pathlib import Path
import socket

FILE_DIR: Path = Path(__file__).parent.resolve()
HOST: str = "localhost"


def create_ssl_context(cert_file: str) -> ssl.SSLContext:
    # TODO: Create an SSL context for the server side. You need to load your certificate.
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain(cert_file)
    return ctx


def create_server_socket(host_ip: str, host_port: int) -> socket.socket:
    # TODO: Create a TCP server socket that is configured correctly.
    bindsocket = socket.socket()
    bindsocket.bind((host_ip, host_port))
    return bindsocket


def wait_for_ssl_connection(ssl_context: ssl.SSLContext, server_socket: socket.socket) -> ssl.SSLSocket:
    # TODO: Wait for an SSL connection and wrap the new socket in an SSL context.
    # Hint: You should call accept here.
    server_socket.listen()
    newsocket, addr_newsocket = server_socket.accept()
    conn_stream = ssl_context.wrap_socket(newsocket, server_side=True)
    newsocket.close()
    return conn_stream


def launch_server(server_port: int, cert_file: str) -> bytes:
    # TODO: Use the helper functions to create an SSL server.
    ctx = create_ssl_context(cert_file)
    server_socket = create_server_socket(HOST, args.server_port)
    data = wait_for_ssl_connection(ctx, server_socket)
    print("Received client SSL message %s", data)
    # TODO: Do not forget to close the socket.
    server_socket.close()
    return data


def main(args):
    launch_server(args.server_port, args.cert_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--server-port",
        default="8000",
        type=int,
        help="The port the server will listen on.",
    )
    parser.add_argument(
        "-c",
        "--cert-file",
        default="cert.pem",
        type=str,
        help="The certificate file the server will use for SSL.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
