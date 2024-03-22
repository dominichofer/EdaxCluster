from dataclasses import dataclass
from reversi import Position


@dataclass
class EdaxTask:
    pos: Position
    level: int

    @staticmethod
    def from_bytes(data: bytes) -> "EdaxTask":
        pos = Position.from_string(data[:66].decode())
        level = int.from_bytes(data[66:], "big")
        return EdaxTask(pos, level)

    def __bytes__(self) -> bytes:
        pos = str(self.pos).encode()
        level = self.level.to_bytes(1, "big")
        return pos + level
