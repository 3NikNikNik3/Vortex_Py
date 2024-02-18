from datetime import datetime

class Istream:
    def __init__(self, path: str):
        with open(path, 'rb') as file:
            self.data = file.read()
        self.index = 0

    def Back(self, how: int):
        self.index = max(0, self.index - how)

    def Next(self, how: int):
        self.index = min(len(self.data), self.index + how)

    def GetChar(self) -> int:
        self.index += 1
        return self.data[self.index - 1]

    def Eof(self) -> bool:
        return self.index == len(self.data)

    def GetInt(self, count: int) -> int:
        if self.Eof(): return 0
        ans = 0
        for i in range(count):
            ans = ans + self.GetChar() * 256 ** i
        return ans

    def GetStrLen(self, len: int) -> str:
        ans = ''
        for i in range(len): ans += chr(self.GetInt(4))
        return ans

    def GetStr(self, stop: int) -> str:
        if self.Eof(): return ''
        ans = ''
        q = self.GetInt(4)
        while q != stop and not self.Eof():
            ans += chr(q)
            q = self.GetInt(4)
        if q != stop: ans += chr(q)
        return ans

    def GetBool(self, count: int = 8) -> list[bool]:
        if self.Eof(): return [False] * count
        ans = [False] * count
        q = self.GetChar()
        i = 0
        while q != 0 and count != i:
            ans[count - 1 - i] = bool(q & 1)
            i += 1
            q >>= 1
        return ans

    def GetStrToEnd(self) -> str:
        ans = self.data[self.index:].decode('utf-8')
        self.index = len(self.data)
        return ans


class Ostream:
    def __init__(self, path: str):
        self.file = open(path, 'wb')

    def WriteChar(self, char: int):
        self.file.write(bytes([char]))

    def WriteInt(self, num: int, count: int):
        for i in range(count):
            self.WriteChar(num % 256)
            num //= 256

    def WriteStrLen(self, string: str):
        for i in string:
            self.WriteInt(ord(i), 4)

    def WriteStr(self, string: str, stop: int):
        if not 0 <= stop <= 255: raise ValueError('0-255!')
        self.WriteStrLen(string)
        self.WriteInt(stop, 4)

    def WriteBool(self, bools: list[bool]):
        if len(bools) > 8: raise ValueError('Слишком много')
        q = 0
        for i in bools:
            q <<= 1
            q |= i
        self.WriteChar(q)

    def WriteStrToEnd(self, string: str):
        self.file.write(string.encode('utf-8'))

    def Close(self):
        self.file.close()


class FileType:
    def Save(self, path: str, type: str):
        file = Ostream(path)
        date = datetime.now()
        file.WriteInt(date.day, 1)
        file.WriteInt(date.month, 1)
        file.WriteInt(date.year - 2000, 1)
        file.WriteStr(type, 1)
        self.Save_(file)
        file.Close()

    def Save_(self, file: Ostream):
        pass

    def Load(self, file: Istream):
        pass

