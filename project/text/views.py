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

def TxtFunFromUtf8(data: bytes):
    ans = TxtType()
    ans.data = data.decode('utf-8')
    return ans

def TxtLoadFunEdit(q):
    ans = TxtType()
    ans.data = q['text']
    return ans

# Create your views here.
def EditTxt(req, file):
    return render(req, 'txt/editTxt.html', {'text': file.data})