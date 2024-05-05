"""File Load"""

from datetime import datetime
import os


class Istream:
    """stream input"""

    def __init__(self, path: str):
        with open(os.path.normpath(path), 'rb') as file:
            self.data = file.read()
        self.index = 0

    def back(self, how: int):
        """back index"""

        self.index = max(0, self.index - how)

    def next(self, how: int):
        """next index"""

        self.index = min(len(self.data), self.index + how)

    def get_char(self) -> int:
        """get char"""

        self.index += 1
        return self.data[self.index - 1]

    def eof(self) -> bool:
        """is end?"""

        return self.index == len(self.data)

    def get_int(self, count: int) -> int:
        """get int"""

        if self.eof():
            return 0
        ans = 0
        for i in range(count):
            ans = ans + self.get_char() * 256 ** i
        return ans

    def get_str_len(self, lenght: int) -> str:
        """get str on len"""

        ans = ''
        for i in range(lenght):
            ans += chr(self.get_int(4))
        return ans

    def get_str(self, stop: int) -> str:
        """get str on stop char"""

        if self.eof():
            return ''
        ans = ''
        q = self.get_int(4)
        while q != stop and not self.eof():
            ans += chr(q)
            q = self.get_int(4)
        if q != stop:
            ans += chr(q)
        return ans

    def get_bool(self, count: int = 8) -> list[bool]:
        """get bool on count (on 1 bytes)"""

        if self.eof():
            return [False] * count
        ans = [False] * count
        q = self.get_char()
        i = 0
        while q != 0 and count != i:
            ans[count - 1 - i] = bool(q & 1)
            i += 1
            q >>= 1
        return ans

    def get_str_to_end(self) -> str:
        """get str from index to end"""

        ans = self.data[self.index:].decode('utf-8')
        self.index = len(self.data)
        return ans


class Ostream:
    """stream out"""

    def __init__(self, path: str):
        self.file = open(os.path.normpath(path), 'wb')

    def write_char(self, char: int):
        """put char"""

        self.file.write(bytes([char]))

    def write_int(self, num: int, count: int):
        """put int on count bytes"""

        for i in range(count):
            self.write_char(num % 256)
            num //= 256

    def write_str_len(self, string: str):
        """put str"""

        for i in string:
            self.write_int(ord(i), 4)

    def write_str(self, string: str, stop: int):
        """put str and stop-char"""

        if not 0 <= stop <= 255:
            raise ValueError('0-255!')
        self.write_str_len(string)
        self.write_int(stop, 4)

    def write_bool(self, bools: list[bool]):
        """put bool (1-8)"""

        if len(bools) > 8:
            raise ValueError('Слишком много')
        q = 0
        for i in bools:
            q <<= 1
            q |= i
        self.write_char(q)

    def write_str_to_end(self, string: str):
        """put str (and end!!!)"""

        self.file.write(string.encode('utf-8'))

    def close(self):
        """close file"""

        self.file.close()


class FileType:
    """Class File Type"""

    def save(self, path: str, type_file: str):
        """save"""

        file = Ostream(path)
        date = datetime.now()
        file.write_int(date.day, 1)
        file.write_int(date.month, 1)
        file.write_int(date.year - 2000, 1)
        file.write_str(type_file, 1)
        self.save_(file)
        file.close()

    def save_(self, file: Ostream):
        """save data file"""

    def load(self, file: Istream):
        """load"""
