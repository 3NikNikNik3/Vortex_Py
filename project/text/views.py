from django.shortcuts import render
from FileType import FileType, Istream, Ostream


class TxtType(FileType):
    def __init__(self):
        self.data = ''

    def Save_(self, file: Ostream):
        file.WriteStrToEnd(self.data)

    def Load(self, file: Istream):
        self.data = file.GetStrToEnd()

def TxtFunToUtf8(file: TxtType):
    return file.data.encode('utf-8')

def TxtFunToASCII(file: TxtType):
    ans = []
    for i in file.data:
        ans.append(ord(i))
    try:
        return bytes(ans)
    except ValueError:
        return bytes([ord(i) for i in 'errorLoad'])

def TxtFunFromUtf8(data: bytes):
    ans = TxtType()
    try:
        ans.data = data.decode('utf-8')
    except UnicodeDecodeError:
        ans.data = 'error'
    return ans

def TxtFunFromASCII(data: bytes):
    ans = TxtType()
    for i in data:
        ans.data += chr(i)
    return ans

def TxtLoadFunEdit(q):
    ans = TxtType()
    ans.data = q['text']
    return ans

# Create your views here.
def EditTxt(req, file):
    return render(req, 'txt/editTxt.html', {'text': '\n' + file.data})