#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple

FILE_DIR: Path = Path(__file__).parent.resolve()
HOST: str = "localhost"


# TODO: Choose a P value that is shared with the client.
P: int = 7


def calculate_shared_secret(x: int, y: int, z: int) -> int:
    # TODO: Calculate the shared secret and return it
    calculation = (x**y)%z
    return calculation


def exchange_base_number(sock: socket.socket) -> int:
    # TODO: Wait for a client message that sends a base number.
    proposal = int.from_bytes(sock.recv(4), 'big')
    # TODO: Return a message that the base number has been received.
    sock.send("Base number has been received".encode())
    return proposal


def launch_server(server_port: int) -> Tuple[int, int, int]:
    # TODO: Create a server socket. can be UDP or TCP.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, server_port))
    server.listen()
    newsock, addr_newsock = server.accept()
    # TODO: Wait for the client to propose a base for the key exchange.
    x = exchange_base_number(newsock)
    print("Base int is %s" % x)
    # TODO: Wait for the nonce computed by the client.
    # TODO: Also reply to the client.
    #*with newsock:
        #while True:
    rx_int = int.from_bytes(newsock.recv(4), 'big')
            #if not rx_int:
                #break
    print("Int received from peer is %s" % rx_int)
    b = random.randint(1,100)
    y = (x**b)%P
    newsock.send(y.to_bytes(4, 'big'))
    print("Y is %s" % y)
    # TODO: Compute the shared secret using the secret number.
    secret = calculate_shared_secret(rx_int, b, P)
    print("Shared secret is %s" % secret)
    # TODO: Do not forget to close the socket.
    newsock.close()
    server.close()
    # TODO: Return the base number, the secret integer, and the shared secret
    return x, b, secret


def main(args):
    launch_server(args.server_port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--server-port",
        default="8000",
        type=int,
        help="The port the server will listen on.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
