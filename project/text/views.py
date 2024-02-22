import os.path

from django.http import HttpResponse
from django.shortcuts import render
from FileType import FileType, Istream, Ostream

from main.models import User


# txt

class TxtType(FileType):
    def __init__(self):
        self.data = ''
        self.type = 'null'

    def Save_(self, file: Ostream):
        file.WriteStr(self.type, 0)
        file.WriteStrToEnd(self.data)

    def Load(self, file: Istream):
        self.type = file.GetStr(0)
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
    ans.type = q['sinte']
    return ans


def EditTxt(req, file):
    return render(req, 'txt/editTxt.html', {'text': '\n' + file.data, 'sinte': file.type})


# html
class FileHtml(FileType):
    def __init__(self):
        self.data = ''

    def Save_(self, file: Ostream):
        file.WriteStrToEnd(self.data)

    def Load(self, file: Istream):
        self.data = file.GetStrToEnd()


def HtmlFunToFile(data: bytes) -> FileHtml:
    ans = FileHtml()
    try:
        ans.data = data.decode('utf-8')
    except UnicodeDecodeError:
        ans.data = '<!DOCTYPE html>\n<body>\n\t<h1>Error load</h1>\n</body>'
    return ans


def HtmlFunFromFile(file: FileHtml) -> bytes:
    return file.data.encode('utf-8')


def HtmlLoadFunEdit(q):
    ans = FileHtml()
    ans.data = q['text']
    return ans


def EditHtml(req, file: FileHtml):
    if req.method == "POST":
        if 'delete_load' in req.POST:
            if os.path.exists('project/main/static/js/txt/data/' +
                        str(User.objects.filter(key=req.get_signed_cookie('key_user', default=''))[0].id) + '.html'):
                os.remove('project/main/static/js/txt/data/' +
                          str(User.objects.filter(key=req.get_signed_cookie('key_user', default=''))[0].id) + '.html')
                return HttpResponse(status=204)
        elif 'load' in req.POST and 'text' in req.POST:
            with open('project/main/static/js/txt/data/' +
                      str(User.objects.filter(key=req.get_signed_cookie('key_user', default=''))[0].id) + '.html',
                      'w') as file_:
                file_.write(req.POST['text'])
            return HttpResponse(status=204)

    return render(req, 'txt/editHtml.html', {'text': '\n' + file.data,
                                             'id': User.objects.filter(key=req.get_signed_cookie('key_user', default=''))[0].id})