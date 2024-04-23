"""views main"""

import os.path

from django.http import HttpResponse
from django.shortcuts import render
from file_type import FileType, Istream, Ostream

from main.models import User


# txt

class TxtType(FileType):
    """File txt"""

    def __init__(self):
        self.data = ''
        self.type = 'null'

    def save_(self, file: Ostream):
        """save"""

        file.write_str(self.type, 0)
        file.write_str_to_end(self.data)

    def load(self, file: Istream):
        """load"""

        self.type = file.get_str(0)
        self.data = file.get_str_to_end()


def txt_fun_to_utf8(file: TxtType) -> bytes:
    """file to bytes utf8"""

    return file.data.encode('utf-8')


def txt_fun_to_ascii(file: TxtType) -> bytes:
    """file to bytes ascii"""

    ans = []
    for i in file.data:
        ans.append(ord(i))
    try:
        return bytes(ans)
    except ValueError:
        return bytes([ord(i) for i in 'errorLoad'])


def txt_fun_from_utf8(data: bytes) -> TxtType:
    """bytes utf8 to file"""

    ans = TxtType()
    try:
        ans.data = data.decode('utf-8')
    except UnicodeDecodeError:
        ans.data = 'error'
    return ans


def txt_fun_from_ascii(data: bytes) -> TxtType:
    """bytes ascii to file"""

    ans = TxtType()
    for i in data:
        ans.data += chr(i)
    return ans


def txt_load_fun_edit(q):
    """file from editor"""

    ans = TxtType()
    if 'text' in q and 'sinte' in q:
        ans.data = q['text']
        ans.type = q['sinte']
    return ans


def edit_txt(req, file):
    """page"""

    return render(req, 'txt/editTxt.html', {'text': '\n' + file.data, 'sinte': file.type})


def new_file(req):
    """new txt file"""

    return TxtType()


def text_to_html(file, post):
    """from txt to html"""

    ans = FileHtml()
    ans.data = file.data
    return ans


def html_to_text(file, post):
    """from html to txt"""

    ans = TxtType()
    ans.data = file.data
    return ans


# html
class FileHtml(FileType):
    """File html"""

    def __init__(self):
        self.data = ''

    def save_(self, file: Ostream):
        """save"""

        file.write_str_to_end(self.data)

    def load(self, file: Istream):
        """load"""

        self.data = file.get_str_to_end()


def html_fun_to_file(data: bytes) -> FileHtml:
    """bytes to file"""

    ans = FileHtml()
    try:
        ans.data = data.decode('utf-8')
    except UnicodeDecodeError:
        ans.data = '<!DOCTYPE html>\n<body>\n\t<h1>Error load</h1>\n</body>'
    return ans


def html_fun_from_file(file: FileHtml) -> bytes:
    """file to bytes"""

    return file.data.encode('utf-8')


def html_load_fun_edit(q):
    """file from editor"""

    ans = FileHtml()
    ans.data = q['text']
    return ans


def edit_html(req, file: FileHtml):
    """page"""

    if req.method == "POST":
        if 'delete_load' in req.POST:
            if os.path.exists('project/main/static/js/txt/data/' +
                              str(User.objects.filter(key=req.get_signed_cookie('key_user',
                                                      default=''))[0].id) + '.html'):
                os.remove('project/main/static/js/txt/data/' +
                          str(User.objects.filter(key=req.get_signed_cookie('key_user', default=''))
                              [0].id) + '.html')
                return HttpResponse(status=204)
        elif 'load' in req.POST and 'text' in req.POST:
            with open('project/main/static/js/txt/data/' +
                      str(User.objects.filter(key=req.get_signed_cookie('key_user', default=''))
                          [0].id) + '.html', 'w', encoding="utf-8") as file_:
                file_.write(req.POST['text'])
            return HttpResponse(status=204)

    return render(req, 'txt/editHtml.html', {'text': '\n' + file.data,
                            'id': User.objects.filter(key=req.get_signed_cookie('key_user',
                                                      default=''))[0].id})


def new_file_html(req):
    """new html file"""

    ans = FileHtml()
    ans.data = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Page</title>
</head>
<body>

</body>
</html>'''
    return ans
