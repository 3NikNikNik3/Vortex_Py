class Istream:
    def __init__(self, path: str):
        with open(path, 'r') as file:
            self.data = file.read()
        self.index = 0

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

    def Close(self):
        self.file.close()


class FileType:
    def Save(self):
        pass

    def Load(self):
        pass

