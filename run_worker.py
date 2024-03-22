import logging
import multiprocessing
import threading
from rte import RemoteServer
from edax_cluster import EdaxWorker

logging.basicConfig(level=logging.DEBUG)

def work(ip, edax_path):
    server = RemoteServer(f"{ip}:50051")
    worker = EdaxWorker(server, refresh_time=5, exe_path=edax_path)
    worker.run()


def main():
    edax_path = r"G:\edax-ms-windows\edax-4.4"
    ip = "localhost"

    threads = []
    for _ in range(multiprocessing.cpu_count()):
        threads.append(threading.Thread(target=work, args=(ip, edax_path)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
