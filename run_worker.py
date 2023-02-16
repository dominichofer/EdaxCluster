import datetime
import multiprocessing
import subprocess
import sys
import threading
import edax
from core import Position
from workspread import TaskDispatchClient

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

        engine = edax.Engine(edax_exe, depth)
        line = engine.solve(pos)[0]

        result = f'{line.depth} {line.confidence} {line.score} {line.time} {line.nodes}'
        client.report_result((index, result))
        log(f'Sent result: {result}')


if __name__ == '__main__':
    edax_exe = sys.argv[1]
    ip = sys.argv[2]

    threads = []
    for _ in range(multiprocessing.cpu_count()):
        threads.append(threading.Thread(target=work, args=(ip, edax_exe)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    subprocess.run(['shutdown', 'now'])
