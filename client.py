"""
File: client.py
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
import random
import socket
import pandas as pd
from threading import Thread

from rich import print

from util import config, logger, MyPackage


# %% ---- 2024-10-30 ------------------------
# Function and class
class MyClient(object):
    host = config.IP.host
    port = config.IP.port
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bufsize = 1024

    def __init__(self):
        self.socket.connect((self.host, self.port))

    def send_package(self):
        mp = MyPackage()
        mp.update_content({'client': {'send': time.time()}})

        # Add header and send
        b, n = mp.encode()
        head = '0x{0:0{1}X}'.format(
            n, config.TCP.codeLengthOfBodyLength).encode(config.TCP.encoding)
        self.socket.send(head+b)

        # Wait until receive
        recv, t_recv = self._receive()
        dct = {'client': {'recv': t_recv}}
        mp = MyPackage(buf=recv)
        mp.update_content(dct)
        logger.debug(f'Received package: {mp.package}')

        return mp

    def send_echo(self):
        t_send = time.time()
        ts = str(t_send).encode(config.TCP.encoding)
        n = len(ts)
        head = '0e{0:0{1}X}'.format(
            n, config.TCP.codeLengthOfBodyLength).encode(config.TCP.encoding)
        self.socket.send(head+ts)

        h = self.socket.recv(config.TCP.codeLengthOfBodyLength+2)
        t_recv = time.time()
        if not h.startswith(b'0e'):
            raise ValueError(f'Invalid received data: {h}')

        n = int(b'0x'+h[2:], 16)
        tsr = self.socket.recv(n)
        offset = float(tsr.split(b',')[1]) - float(tsr.split(b',')[0])
        return t_recv - t_send, tsr, offset

    def _receive(self):
        # Receive header for buf remain length
        # It will also break if empty message is received
        h = self.socket.recv(config.TCP.codeLengthOfBodyLength+2)
        t_recv = time.time()
        try:
            body_length = int(h, 16)
        except Exception as e:
            logger.error(
                f'Received wrong number of bytes: {h}, expect like "0x12345678"')
            raise

        # Receive body
        array = []
        while body_length > 0:
            buf = self.socket.recv(min(body_length, self.bufsize))
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


# %% ---- 2024-10-30 ------------------------
# Play ground
if __name__ == '__main__':
    client = MyClient()
    # Thread(target=client.recv_loop, daemon=True).start()

    buffer = []

    for _ in range(20):
        mp = client.send_package()
        df = mp.to_df()
        buffer.append(df)

    delays = []
    for _ in range(20):
        delay = client.send_echo()
        delays.append(delay)

    # Interacting
    while False:
        inp = input('Enter q to escape, s to send >> ')
        if inp == 'q':
            break

        if inp == 's':
            mp = client.send_package()
            df = mp.to_df()
            buffer.append(df)
            print(df)

    df = pd.concat(buffer)
    df.index = range(len(df))
    df[('summary', 'recvDelay')] = df[('client', 'recv')] - df[('client', 'send')]
    df[('summary', 'sentOffset')] = df[(
        'server', 'recv')] - df[('client', 'send')]
    df[('summary', 'recvOffset')] = df[(
        'client', 'recv')] - df[('server', 'send')]
    print(df)
    print(df['summary'].sort_values('recvDelay'))

    print(delays)

    # Safely close the app
    sys.exit()

# %%

# %%
# %%


# %% ---- 2024-10-30 ------------------------
# Pending


# %% ---- 2024-10-30 ------------------------
# Pending
