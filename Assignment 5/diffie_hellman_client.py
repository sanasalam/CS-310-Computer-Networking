#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple

FILE_DIR: Path = Path(__file__).parent.resolve()
HOST: str = "localhost"

# TODO: Choose a P value that is shared with the server.
P: int = 7

def exchange_base_number(sock: socket.socket, server_port: int) -> int:
    # TODO: Connect to the server and propose a base number.
    # TODO: This should be a random number.
    sock.connect((HOST, server_port))
    proposal = random.randint(1,100)
    sock.send(proposal.to_bytes(4, 'big'))
    sock.recv(1024)
    print("Base proposal successful.")
    return proposal


def calculate_shared_secret(x: int, y: int, z: int) -> int:
    # TODO: Calculate the shared secret and return it
    calculation = (x**y)%z
    return calculation


def generate_shared_secret(server_port: int) -> Tuple[int, int, int]:
    # TODO: Create a socket and send the proposed base number to the server.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    x = exchange_base_number(sock, server_port)
    print("Base int is %s" % x)
    # TODO: Calculate the message the client sends using the secret integer.
    a = random.randint(1,100)
    y = (x**a)%P
    print("Y is %s" % y)
    # TODO: Send it to the server.
    sock.send(y.to_bytes(4, 'big'))
    # TODO: Calculate the secret based on the server reply.
    rx_int = int.from_bytes(sock.recv(4), 'big')
    print("Int received from peer is %s" % rx_int)
    secret = calculate_shared_secret(rx_int, a, P)
    print("Shared secret is %s" % secret)
    # TODO: Do not forget to close the socket.
    sock.close()
    # TODO: Return the base number, the private key, and the shared secret
    return x, y, secret


def main(args):
    if args.seed:
        random.seed(args.seed)
    generate_shared_secret(args.server_port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--server-port",
        default="8000",
        type=int,
        help="The port the client will connect to.",
    )
    parser.add_argument(
        "--seed",
        dest="seed",
        type=int,
        help="Random seed to make the exchange deterministic.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
