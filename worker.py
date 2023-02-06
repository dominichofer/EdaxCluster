import socket
import datetime
import time
import sys
import edax
import multiprocessing
import threading
from core import Position
from workspread import Client

def log(text: str = ''):
    print(f'[{datetime.datetime.now()}] {text}')


def work(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    client = Client(sock)
    while True:
        log(f'Asking for task')
        task = client.get_task()
        log(f'Received task: {task}')
        if task is None:
            break
        pos = Position.from_string(task)
        depth = int(task[66:])
        #edax = edax.Engine('../edax-reversi/bin/lEdax-x64-modern', depth)
        engine = edax.Engine(r'G:\edax-ms-windows\edax-4.4', depth)
        line = engine.solve(pos)[0]

        result = f'{line.depth} {line.confidence} {line.score} {line.time} {line.nodes}'
        client.report_result(result)
        log(f'Sent result: {result}')


if __name__ == '__main__':

    #ip = sys.argv[1]
    #port = int(sys.argv[2])
    ip = 'ec2-54-157-188-48.compute-1.amazonaws.com'
    port = 12350
    
    threads = []
    for _ in range(multiprocessing.cpu_count()):
        threads.append(threading.Thread(target=work, args=(ip, port)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()
