import unittest
from reversi import Position
from edax_cluster import EdaxTask


class TestEdaxTask(unittest.TestCase):
    def test_serialize(self):
        original = EdaxTask(Position(1, 2), 3)  # arbitrary

        data = bytes(original)
        recovered = EdaxTask.from_bytes(data)

        self.assertEqual(original, recovered)
