"""File Load"""

from datetime import datetime
import os


class Istream:
    def __init__(self, path: str):
        with open(os.path.normpath(path), 'rb') as file:
            self.data = file.read()
        self.index = 0

    def back(self, how: int):
        self.index = max(0, self.index - how)

    def next(self, how: int):
        self.index = min(len(self.data), self.index + how)

    def get_char(self) -> int:
        self.index += 1
        return self.data[self.index - 1]

    def eof(self) -> bool:
        return self.index == len(self.data)

    def get_int(self, count: int) -> int:
        if self.eof(): return 0
        ans = 0
        for i in range(count):
            ans = ans + self.get_char() * 256 ** i
        return ans

    def get_str_len(self, len: int) -> str:
        ans = ''
        for i in range(len): ans += chr(self.get_int(4))
        return ans

    def get_str(self, stop: int) -> str:
        if self.eof(): return ''
        ans = ''
        q = self.get_int(4)
        while q != stop and not self.eof():
            ans += chr(q)
            q = self.get_int(4)
        if q != stop: ans += chr(q)
        return ans

    def get_bool(self, count: int = 8) -> list[bool]:
        if self.eof(): return [False] * count
        ans = [False] * count
        q = self.get_char()
        i = 0
        while q != 0 and count != i:
            ans[count - 1 - i] = bool(q & 1)
            i += 1
            q >>= 1
        return ans

    def get_str_to_end(self) -> str:
        ans = self.data[self.index:].decode('utf-8')
        self.index = len(self.data)
        return ans


class Ostream:
    def __init__(self, path: str):
        self.file = open(os.path.normpath(path), 'wb')

    def write_char(self, char: int):
        self.file.write(bytes([char]))

    def write_int(self, num: int, count: int):
        for i in range(count):
            self.write_char(num % 256)
            num //= 256

    def write_str_len(self, string: str):
        for i in string:
            self.write_int(ord(i), 4)

    def write_str(self, string: str, stop: int):
        if not 0 <= stop <= 255: raise ValueError('0-255!')
        self.write_str_len(string)
        self.write_int(stop, 4)

    def write_bool(self, bools: list[bool]):
        if len(bools) > 8: raise ValueError('Слишком много')
        q = 0
        for i in bools:
            q <<= 1
            q |= i
        self.write_char(q)

    def write_str_to_end(self, string: str):
        self.file.write(string.encode('utf-8'))

    def close(self):
        self.file.close()


class FileType:
    def save(self, path: str, type_file: str):
        file = Ostream(path)
        date = datetime.now()
        file.write_int(date.day, 1)
        file.write_int(date.month, 1)
        file.write_int(date.year - 2000, 1)
        file.write_str(type_file, 1)
        self.save_(file)
        file.close()

    def save_(self, file: Ostream):
        pass

    def load(self, file: Istream):
        pass

