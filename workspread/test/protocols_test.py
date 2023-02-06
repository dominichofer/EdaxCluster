import unittest
from workspread.protocols import HeaderPresentation


class HeaderPresentationTest(unittest.TestCase):

    def test_None(self):
        original = None
        data = HeaderPresentation.encode(original)
        msg = HeaderPresentation.decode(data)
        self.assertEqual(original, msg)

    def test_bytes(self):
        original = b'\x12\x34\x56\x78'
        data = HeaderPresentation.encode(original)
        msg = HeaderPresentation.decode(data)
        self.assertEqual(original, msg)
        
    def test_int(self):
        original = 13
        data = HeaderPresentation.encode(original)
        msg = HeaderPresentation.decode(data)
        self.assertEqual(original, msg)

    def test_str(self):
        original = 'string'
        data = HeaderPresentation.encode(original)
        msg = HeaderPresentation.decode(data)
        self.assertEqual(original, msg)

    def test_list(self):
        original = [1, 2, 3]
        data = HeaderPresentation.encode(original)
        msg = HeaderPresentation.decode(data)
        self.assertEqual(original, msg)

    def test_tuple(self):
        original = (1, 2, 3)
        data = HeaderPresentation.encode(original)
        msg = HeaderPresentation.decode(data)
        self.assertEqual(original, msg)

        
if __name__ == '__main__':
    unittest.main(verbosity=2)
