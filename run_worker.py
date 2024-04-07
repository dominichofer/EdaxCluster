import logging
import multiprocessing
import sys
import threading
from rte import RemoteServer
from edax_cluster import EdaxWorker

logging.basicConfig(level=logging.INFO)


def work(target):
    server = RemoteServer(target)
    worker = EdaxWorker(server, refresh_time=1)
    worker.run()


if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"

    threads = []
    for _ in range(multiprocessing.cpu_count()):
        threads.append(threading.Thread(target=work, args=(f"{ip}:50051",)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()
