import unittest
from random import randbytes
from workspread.protocols import HeaderPresentation, HeaderSizeTransport


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


class SocketMock:

    def sendall(self, data: bytes) -> None:
        self.stream = data

    def recv(self, buffer_size: int) -> bytes:
        data = self.stream[:buffer_size]
        self.stream = self.stream[buffer_size:]
        return data


class HeaderSizeTransportTest(unittest.TestCase):

    def test_send_receive_1_chunk(self):
        original = b'\x12\x34\x56\x78'
        socket = SocketMock()
        tp = HeaderSizeTransport(socket)

        tp.send(original)
        recv = tp.receive()

        self.assertEqual(original, recv)

    def test_send_receive_multichunk(self):
        original = randbytes(int(12.5 * HeaderSizeTransport.buffer_size))
        socket = SocketMock()
        tp = HeaderSizeTransport(socket)

        tp.send(original)
        recv = tp.receive()

        self.assertEqual(original, recv)

        
if __name__ == '__main__':
    unittest.main(verbosity=2)
