import unittest
from reversi import EdaxLine
from edax_cluster import EdaxWorker


class TestEdaxWorker(unittest.TestCase):
    def test_execute_task(self):
        worker = EdaxWorker(server=None, refresh_time=1)
        task = b"--XXXXX--OOOXX-O-OOOXXOX-OXOXOXXOXXXOXXX--XOXOXX-XXXOOO--OOOOO-- X<"

        result = worker.execute_task(task)

        r = EdaxLine.from_bytes(result)
        self.assertEqual(r.intensity.depth, 14)
        self.assertEqual(r.intensity.confidence_level, float("inf"))
        self.assertEqual(r.score, 18)
