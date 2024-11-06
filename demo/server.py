import socket
import time
import pandas as pd


host = 'localhost'
port = 8888

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5)  # become a server socket, maximum 5 connections

# Only accept the connection ONCE
connection, address = serversocket.accept()
array = []
while True:
    buf = connection.recv(1024)
    t = time.time()
    connection.send(buf + f' recv: {t}'.encode())
    print(buf)

    if len(buf) > 0:
        if buf == b'quit':
            break

        t0 = float(buf.decode().split(' ')[-1])
        delay = t - t0
        array.append(dict(delay=delay*1000, content=buf))
        print(f'Recv: {buf} | {delay}')
    else:
        print('Received empty message.')
        break

df = pd.DataFrame(array)
print(df)
print('Std(ms): {}, Avg(ms): {}'.format(df['delay'].std(), df['delay'].mean()))
print('Max(ms): {}, Min(ms): {}'.format(df['delay'].max(), df['delay'].min()))
