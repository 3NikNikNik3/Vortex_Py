from django.shortcuts import render
from FileType import FileType, Istream, Ostream

class BinType(FileType):
    def __init__(self):
        self.data = bytes()

    def Save_(self, file: Ostream):
        file.file.write(self.data)

    def Load(self, file: Istream):
        self.data = file.data[file.index:]

def BinFrom(data: bytes):
    q = BinType()
    q.data = data
    return q

def BinTo(file: BinType):
    return file.data

def EditToFile(req):
    print(req)
    ans = BinType()
    q = []
    for i in range(0, len(req['bin']), 2):
        q.append(int(req['bin'][i:i + 2], 16))
    ans.data = bytes(q)
    return ans

# Create your views here.
def Edit(req, file: BinType):
    q = ''
    for i in file.data:
        if i < 16:
            q += '0'
        q += hex(i)[2:].upper()
    return render(req, 'bin/EditBin.html', {'data': q})