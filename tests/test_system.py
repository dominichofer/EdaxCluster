import unittest
from threading import Thread
from rte import Server
from edax_cluster import EdaxTask, EdaxBatchClient, EdaxWorker


class TestSystem(unittest.TestCase):
    def setUp(self) -> None:
        self.server = Server(task_timeout=1)
        worker = EdaxWorker(self.server, refresh_time=0.5)
        self.worker_thread = Thread(target=worker.run)
        self.worker_thread.start()

    def tearDown(self) -> None:
        self.server.release_waiting_workers()
        self.server.stop()
        self.worker_thread.join()

    def test_system(self):
        client = EdaxBatchClient(self.server, refresh_time=0.5)
        tasks = [EdaxTask(pos="--XXXXX--OOOXX-O-OOOXXOX-OXOXOXXOXXXOXXX--XOXOXX-XXXOOO--OOOOO-- X", level=60)] * 3
        results = client.solve(tasks)

        self.assertEqual(len(results), 3)
        for r in results:
            self.assertIsNotNone(r)
            self.assertEqual(r.score, +18)
