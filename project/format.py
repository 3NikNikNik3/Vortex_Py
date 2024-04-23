"""Format"""

import typing
from dataclasses import dataclass

from django.http import HttpRequest
from django.shortcuts import HttpResponse

from file_type import FileType, Istream

from text import views as Text
from binary import views as Bin


@dataclass
class Format:
    """Format file load"""

    name: str
    fun_to: typing.Callable[[FileType], bytes]
    fun_from: typing.Callable[[bytes], FileType]
    type_file: str
    ext: str
    max_size: int


def get_text_from_file(path: str) -> str:
    """get text from file"""
    with open(f'main/templates/{path}', 'r', encoding="utf-8") as file:
        data = file.read()
    return data


class Transform:
    """Transform file"""

    def __init__(self, where: str, fun_can, fun_main, option: str | None):
        self.where = where
        self.fun_can = fun_can
        self.fun_main = fun_main
        self.option = option

    def get_html_option(self) -> str:
        """Get html text option or none"""

        if self.option is None:
            return '<p>Их нет</p>'
        return get_text_from_file(self.option)


class NewFile:
    """About create file"""

    def __init__(self, option: str | None, fun):
        self.option = option
        self.fun = fun

    def get_html_option(self) -> str:
        """Get html text option or not"""

        if self.option is None:
            return ''
        return get_text_from_file(self.option)


@dataclass
class Type:
    """Type file"""

    fun_edit: typing.Callable[[HttpRequest, FileType], HttpResponse]
    load_fun_edit: typing.Callable[[HttpRequest], FileType]
    class_edit: FileType
    name: str
    new_file: NewFile
    transform: list[Transform]

    def get_trans(self, name: str) -> Transform | None:
        """I have this transform"""

        for i in self.transform:
            if i.where == name:
                return i
        return None


DEFAULT = 0

Formats = [
    Format('.txt (utf-8) (codes)', Text.txt_fun_to_utf8, Text.txt_fun_from_utf8,
           'txt/text', '.txt', 102400),
    Format('.txt', Text.txt_fun_to_ascii, Text.txt_fun_from_ascii, 'txt/text', '.txt', 102400),
    Format('(bytes)', Bin.bin_to, Bin.bin_from, 'bin/bin', '', 10240),
    Format('.html', Text.html_fun_from_file, Text.html_fun_to_file, 'txt/html', '.html', 102400)
]

Types = {
    'txt/text': Type(Text.edit_txt, Text.txt_load_fun_edit, Text.TxtType, 'Текст',
                     NewFile(None, Text.new_file),
                     [Transform('bin/bin', lambda x: True, Bin.txt_to_bin, None),
                      Transform('txt/html', lambda x: True, Text.text_to_html, None)]),
    'bin/bin': Type(Bin.edit, Bin.edit_to_file, Bin.BinType, 'Батник', NewFile(None, Bin.new_file),
                    [Transform('txt/text', lambda x: True, Bin.bin_to_txt, 'bin/toTxt.html')]),
    'txt/html': Type(Text.edit_html, Text.html_load_fun_edit, Text.FileHtml, 'HTML файлы',
                     NewFile(None, Text.new_file_html), [
                         Transform('txt/text', lambda x: True, Text.html_to_text, None)
                     ])
}


def get(name: str) -> Format:
    """Get format"""

    for i in Formats:
        if i.name == name:
            return i
    return Formats[DEFAULT]


def load_from_file(path: str) -> (int, FileType):
    """Get FileType from file"""

    file = Istream(path)
    file.next(3)
    type_file = file.get_str(1)
    ans = Types[type_file].class_edit()
    ans.load(file)
    return type_file, ans
