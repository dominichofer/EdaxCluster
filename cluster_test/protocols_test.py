import unittest
from random import randbytes
from cluster.protocols import PascalMethod, MessageTransporter


class PascalMethodTest(unittest.TestCase):

    def roundtrip(self, msg):
        presenter = PascalMethod()
        data = presenter.encode(msg)
        ret = presenter.decode(data)
        self.assertEqual(msg, ret)

    def test_None(self):
        self.roundtrip(None)

    def test_bytes(self):
        self.roundtrip(b'\x12\x34\x56\x78')
        
    def test_bool(self):
        self.roundtrip(True)
        self.roundtrip(False)
        
    def test_int(self):
        self.roundtrip(13)
        
    def test_float(self):
        msg = 3.14
        presenter = PascalMethod()
        data = presenter.encode(msg)
        ret = presenter.decode(data)
        self.assertAlmostEqual(msg, ret)

    def test_str(self):
        self.roundtrip('string')

    def test_tuple(self):
        self.roundtrip((1, 2, 3))

    def test_list(self):
        self.roundtrip([1, 2, 3])


class SocketMock:
    """
    Mocks 'socket.socket'.
    Puts data from 'sendall' into a buffer and emits it in 'recv'.
    """

    def setblocking(self, _) -> None:
        pass

    def sendall(self, data: bytes) -> None:
        self.stream = data

    def recv(self, buffer_size: int) -> bytes:
        data = self.stream[:buffer_size]
        self.stream = self.stream[buffer_size:]
        return data


class MessageTransporterTest(unittest.TestCase):

    def test_send_receive_1_chunk(self):
        tp = MessageTransporter(SocketMock())
        msg = b'\x12\x34\x56\x78'

        tp.send(msg)
        recv = tp.receive(blocking = True)

        self.assertEqual(msg, recv)

    def test_send_receive_multichunk(self):
        tp = MessageTransporter(SocketMock())
        msg = randbytes(int(12.5 * tp.buffer_size))

        tp.send(msg)
        recv = tp.receive(blocking = True)

        self.assertEqual(msg, recv)

        
if __name__ == '__main__':
    unittest.main(verbosity=2)
