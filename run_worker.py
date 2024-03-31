import logging
import multiprocessing
import threading
from rte import RemoteServer
from edax_cluster import EdaxWorker

logging.basicConfig(level=logging.INFO)


def work(target):
    server = RemoteServer(target)
    worker = EdaxWorker(server, refresh_time=1)
    worker.run()


def main():
    target = "localhost:50051"

    threads = []
    for _ in range(multiprocessing.cpu_count()):
        threads.append(threading.Thread(target=work, args=(target,)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
