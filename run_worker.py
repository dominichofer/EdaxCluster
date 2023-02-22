import datetime
import multiprocessing
import sys
import threading
import edax
from core import Position
from cluster import TaskDispatchClient

def log(text: str = ''):
    now = datetime.datetime.now()
    print(f'[{now}] {text}')


def work(ip, edax_exe):
    client = TaskDispatchClient(ip)

    while True:
        log(f'Requesting task')
        task = client.request_task()
        if task is None:
            log('Received no task')
            break
        log(f'Received task: {task}')

        index, (pos, depth) = task

        pos = Position.from_string(pos)
        depth = int(depth)

        engine = edax.Engine(edax_exe, depth, tasks=1)
        line = engine.solve(pos)[0]
        
        client.report_result((index, (line.depth, line.score, line.time, line.nodes)))
        log(f'Sent result: {line.depth} {line.score} {line.time} {line.nodes}')


if __name__ == '__main__':
    edax_exe = sys.argv[1]
    ip = sys.argv[2]
    #edax_exe = r'G:\edax-ms-windows\edax-4.4'
    #ip = 'ec2-44-195-46-122.compute-1.amazonaws.com'
    #ip = 'localhost'

    #work(ip, edax_exe)

    threads = []
    for _ in range(multiprocessing.cpu_count()):
        threads.append(threading.Thread(target=work, args=(ip, edax_exe)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()
