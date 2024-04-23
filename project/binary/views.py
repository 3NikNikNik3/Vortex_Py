"""views bin"""

from django.shortcuts import render
from file_type import FileType, Istream, Ostream
from text import views as Text


class BinType(FileType):
    """file bin"""

    def __init__(self):
        self.data = bytes()

    def save_(self, file: Ostream):
        """save"""

        file.file.write(self.data)

    def load(self, file: Istream):
        """load"""

        self.data = file.data[file.index:]


def bin_from(data: bytes):
    """bytes to file"""

    q = BinType()
    q.data = data
    return q


def bin_to(file: BinType) -> bytes:
    """file to bytes"""

    return file.data


def edit_to_file(req) -> BinType:
    """file from editor"""

    ans = BinType()
    q = []
    for i in range(0, len(req['bin']), 2):
        q.append(int(req['bin'][i:i + 2], 16))
    ans.data = bytes(q)
    return ans


# Create your views here.
def edit(req, file: BinType):
    """page"""

    q = ''
    for i in file.data:
        if i < 16:
            q += '0'
        q += hex(i)[2:].upper()
    return render(req, 'bin/EditBin.html', {'data': q})


def txt_to_bin(file: Text.TxtType, req):
    """file txt to file bin"""

    ans = BinType()
    ans.data = file.data.encode()
    return ans


def bin_to_txt(file: BinType, req):
    """file bin to file txt"""

    ans = Text.TxtType()
    if 'ut' in req:
        ans.data = file.data.decode()
    else:
        for i in file.data:
            ans.data += chr(i)
    return ans


def new_file(req):
    """new file"""

    return bin_from(bytes([0]))
