import subprocess
import secrets
import numpy as np
import multiprocessing
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import Iterable
from core import write_position_file
from .output import Line, parse


class Engine:
    def __init__(self, exe_path, level: int, tasks: int = None, thread_pool: bool = False):
        self.exe: Path = Path(exe_path)
        self.level: int = level
        self.tasks: int = tasks
        self.thread_pool: bool = thread_pool

    def name(self):
        return f'Edax4.4 level {self.level}'

    def __solve(self, pos) -> list[Line]:
        token = secrets.token_hex(16)
        tmp_file = self.exe.parent / f'tmp_{token}.script'

        write_position_file(pos, tmp_file) # create tmp file
        
        cmd = [self.exe, '-l', str(self.level), '-solve', tmp_file]
        if self.tasks:
            cmd += ['-n', str(self.tasks)]
        if self.level < 2:
            cmd += ['-h', '10']

        result = subprocess.run(
            cmd,
            cwd = self.exe.parent,
            capture_output = True,
            text = True)

        tmp_file.unlink() # remove tmp file

        return parse(result.stdout)
            
    def solve(self, pos) -> list[Line]:
        if not isinstance(pos, Iterable):
            pos = [pos]
        
        if self.thread_pool:
            pool = ThreadPool()
            results = pool.map(
                self.__solve, 
                np.array_split(pos, multiprocessing.cpu_count() * 4)
                )
            pool.close()
            return [r for result in results for r in result]
        else:
            return self.__solve(pos)

    def choose_move(self, pos) -> list[int]:
        result = self.solve(pos)
        return [(r.pv[0] if r.pv else 64) for r in result]
