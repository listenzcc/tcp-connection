"""
File: server.py
Author: Chuncheng Zhang
Date: 2024-10-30
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-10-30 ------------------------
# Requirements and constants
import sys
import time
import socket
import random

from threading import Thread

from util import config, logger, MyPackage


# %% ---- 2024-10-30 ------------------------
# Function and class
class MyServer(object):
    host = config.IP.host
    port = config.IP.port
    clients_limit = config.IP.clientsLimit
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bufsize = 1024

    def __init__(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.clients_limit)
        logger.info(f'Started server on {self.host}:{self.port}')

    def serve_forever(self):
        while True:
            conn, addr = self.socket.accept()
            logger.debug(f'Got connection: {conn} | {addr}')
            Thread(target=self.recv_loop(conn, addr), daemon=True).start()

    def _receive(self, conn):
        # Receive header for buf remain length
        # It will also break if empty message is received
        h = conn.recv(config.TCP.codeLengthOfBodyLength+2)
        t_recv = time.time()

        if h == b'':
            raise ConnectionResetError

        # Deal with echo package
        if h.startswith(b'0a'):
            n = int(b'0x'+h[2:], 16)
            ts = conn.recv(n)
            tsr = ts + b',' + str(t_recv).encode(config.TCP.encoding)
            n = len(tsr)
            head = '0x{0:0{1}X}'.format(
                n, config.TCP.codeLengthOfBodyLength).encode(config.TCP.encoding)
            conn.send(head+tsr)
            logger.debug(f'Received echo packet and sent back: {ts} -> {tsr}')
            return None, t_recv

        # Deal with normal package
        try:
            body_length = int(h, 16)
        except Exception as e:
            logger.error(
                f'Received wrong number of bytes: {h}, expect like "0x12345678"')
            raise

        # Receive body
        array = []
        while body_length > 0:
            buf = conn.recv(min(body_length, self.bufsize))
            body_length -= len(buf)
            array.append(buf)

        # Body should be extracted but is not actually emptied.
        if body_length != 0:
            logger.error(
                f'Received unexpected number of bytes, remain_num is not ZERO: {body_length}, {array}')
            raise

        # Concatenate the array together to make recv bytes
        recv = b''.join(array)

        logger.debug(f'Received {recv}')
        return recv, t_recv

    def recv_loop(self, conn, addr):
        """
        This function continuously receives data from a connection until an empty message is received.
        The receiving process is handled in the main loop, while the returning process is handled in a separate thread for every recv.

        Parameters:
        - conn (socket.socket): The socket connection object.
        - addr (tuple): The address of the connected client.

        Returns:
        None
        """
        while True:
            # Receive bytes from connection
            try:
                recv, t_recv = self._receive(conn)
            except ConnectionResetError:
                break

            # Update message and return
            if recv is not None:
                Thread(
                    target=self.work_with_recv, args=(conn, recv, t_recv), daemon=True).start()

        logger.debug(f'Connection stopped: {conn} | {addr}')
        return

    def work_with_recv(self, conn, recv: bytes, t_recv: float):
        # Update message and return
        mp = MyPackage(buf=recv)
        dct = {'server': {'recv': t_recv}}

        # TODO: Working with recv
        # There are chances sleeping for a while or not
        # Sleep for upper to 1 seconds simulating a loaded work.
        if random.random() < -0.1:
            time.sleep(random.random())

        # Return message
        dct['server']['send'] = time.time()
        mp.update_content(dct)

        # Add header and send
        b, n = mp.encode()
        head = '0x{0:0{1}X}'.format(
            n, config.TCP.codeLengthOfBodyLength).encode(config.TCP.encoding)

        conn.send(head+b)
        return


# %% ---- 2024-10-30 ------------------------
# Play ground
if __name__ == "__main__":
    # Start the server
    server = MyServer()

    Thread(target=server.serve_forever, daemon=True).start()

    # Interacting
    while True:
        inp = input('Enter q to escape >> ')
        if inp == 'q':
            break

    # Safely close the app
    sys.exit()

# %% ---- 2024-10-30 ------------------------
# Pending


# %% ---- 2024-10-30 ------------------------
# Pending
