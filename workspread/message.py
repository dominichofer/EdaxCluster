class Message:
    encoding = 'utf8'
    terminator = '\0'
    encoded_terminator = terminator.encode(encoding)

    def __init__(self, header: str, body = '') -> None:
        assert isinstance(header, str)
        assert isinstance(body, (str, list))
        assert ' ' not in header
        assert ',' not in header
        assert self.terminator not in header
        assert self.terminator not in body
        self.header = header
        self.body = body
        
    def __eq__(self, o) -> bool:
        return self.header == o.header and self.body == o.body

    def __ne__(self, o) -> bool:
        return not self == o

    def __str__(self) -> str:
        return self.header + ' ' + self.body

    def encode(self) -> bytes:
        if isinstance(self.body, list):
            body_sizes = [str(len(x)) for x in self.body]
            body = ''.join(self.body)
            s = ','.join([self.header] + body_sizes) + ' ' + body + self.terminator
        else:
            s = self.header + ' ' + self.body + self.terminator
        return s.encode(self.encoding)
    
    @classmethod
    def __decode(cls, msg: str):
        header, body = msg.split(' ', 1)
        if ',' in header:
            new_header, *body_sizes = header.split(',')
            new_body = []
            sum = 0
            for size in body_sizes:
                new_body.append(body[sum:sum + int(size)])
                sum += int(size)
            return cls(new_header, new_body)
        else:
            return cls(header, body)

    @staticmethod
    def decode(data: bytes):
        msg = data.decode(Message.encoding).rstrip(Message.terminator)
        return [Message.__decode(m) for m in msg.split(Message.terminator)]
