class Istream:
    def __init__(self, path: str):
        with open(path, 'r') as file:
            self.data = file.read()
        self.index = 0

    def Back(self, how: int):
        self.index = max(0, self.index - how)

    def Next(self, how: int):
        self.index = min(len(self.data), self.index + how)

    def GetChar(self) -> str:
        self.index += 1
        return self.data[self.index - 1]

    def Eof(self) -> bool:
        return self.index == len(self.data)

    def GetInt(self, count: int) -> int:
        ans = 0
        for i in range(count):
            ans = ans + ord(self.GetChar()) * 256 ** i
        return ans

    def GetStrLen(self, len: int) -> str:
        ans = ''
        for i in range(len): ans += self.GetChar()
        return ans

    def GetStr(self, stop: int) -> str:
        ans = ''
        q = self.GetChar()
        while ord(q) != stop and not self.Eof():
            ans += q
            q = self.GetChar()
        return ans

    def GetBool(self, count: int = 8) -> list[bool]:
        ans = [False] * count
        q = ord(self.GetChar())
        i = 0
        while q != 0 and count != i:
            ans[count - 1 - i] = bool(q & 1)
            i += 1
            q >>= 1
        return ans


class Ostream:
    def __init__(self, path: str):
        self.file = open(path, 'w')

    def WriteChar(self, char: str):
        self.file.write(char)

    def WriteInt(self, num: int, count: int):
        for i in range(count):
            self.file.write(chr(num % 256))
            num //= 256

    def WriteStrLen(self, string: str):
        for i in string:
            self.WriteChar(i)

    def WriteStr(self, string: str, stop: int):
        for i in string:
            self.WriteChar(i)
        self.WriteChar(chr(stop))

    def WriteBool(self, bools: list[bool]):
        if len(bools) > 8: raise ValueError('Слишком много')
        q = 0
        for i in bools:
            q <<= 1
            q |= i
        self.WriteChar(chr(q))

    def Close(self):
        self.file.close()


class FileType:
    def Save(self, path: str, name: str):
        pass

    def Load(self):
        pass

