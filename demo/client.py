import socket
import random
import time
import pandas as pd


host = 'localhost'
port = 8888


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))
array = []

for j in range(20):
    t_send = time.time()
    clientsocket.send(f'{j}: hello: {t_send}'.encode())
    buf = clientsocket.recv(1024)
    t_recv = time.time()
    delay = t_recv - t_send
    array.append(dict(delay=delay*1000, content=buf))
    print(f'Recv: {j} | {buf} | {delay}')
    time.sleep(random.random()*1)

clientsocket.send(b'quit')

df = pd.DataFrame(array)
print(df)
print('Std(ms): {}, Avg(ms): {}'.format(df['delay'].std(), df['delay'].mean()))
print('Max(ms): {}, Min(ms): {}'.format(df['delay'].max(), df['delay'].min()))
