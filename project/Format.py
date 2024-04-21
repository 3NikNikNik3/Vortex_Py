from django.shortcuts import render

from FileType import FileType, Istream

from text import views as Text
from binary import views as Bin


class Format:
    def __init__(self, name: str, funTo, funFrom, type: str, ext: str, max_size: int):
        self.name = name
        # функция преобразования datas в класс
        self.funTo = funTo
        self.funFrom = funFrom
        self.type = type
        self.ext = ext
        self.max_size = max_size


def GetTextFromFile(path: str) -> str:
    with open(f'project/main/templates/{path}', 'r') as file:
        data = file.read()
    return data


class Transform:
    def __init__(self, where: str, funCan, funMain, option: str | None):
        self.where = where
        self.funCan = funCan
        self.funMain = funMain
        self.option = option

    def GetHtmlOption(self) -> str:
        if self.option is None:
            return '<p>Их нет</p>'
        return GetTextFromFile(self.option)


class NewFile:
    def __init__(self, option: str | None, fun):
        self.option = option
        self.fun = fun

    def GetHtmlOption(self) -> str:
        if self.option is None:
            return ''
        return GetTextFromFile(self.option)


class Type:
    def __init__(self, funedit, loadfunedit, classedit, name: str, new_file: NewFile, transform: list[Transform]):
        self.FunEdit = funedit
        self.ClassEdit = classedit
        self.LoadFunEdit = loadfunedit
        self.name = name
        self.new_file = new_file
        self.transform = transform

    def GetTrans(self, name: str) -> Transform | None:
        for i in self.transform:
            if i.where == name:
                return i
        return None


DEFAULT = 0

Formats = [
    Format('.txt (utf-8) (codes)', Text.TxtFunToUtf8, Text.TxtFunFromUtf8, 'txt/text', '.txt', 102400),
    Format('.txt', Text.TxtFunToASCII, Text.TxtFunFromASCII, 'txt/text', '.txt', 102400),
    Format('(bytes)', Bin.BinTo, Bin.BinFrom, 'bin/bin', '', 10240),
    Format('.html', Text.HtmlFunFromFile, Text.HtmlFunToFile, 'txt/html', '.html', 102400)
]

Types = {
    'txt/text': Type(Text.EditTxt, Text.TxtLoadFunEdit, Text.TxtType, 'Текст', NewFile(None, Text.NewFile),
                     [Transform('bin/bin', lambda x: True, Bin.TxtToBin, None),
                      Transform('txt/html', lambda  x: True, Text.TextToHtml, None)]),
    'bin/bin': Type(Bin.Edit, Bin.EditToFile, Bin.BinType, 'Батник', NewFile(None, Bin.NewFile),
                    [Transform('txt/text', lambda x: True, Bin.BinToTxt, 'bin/toTxt.html')]),
    'txt/html': Type(Text.EditHtml, Text.HtmlLoadFunEdit, Text.FileHtml, 'HTML файлы', NewFile(None, Text.NewFileHtml), [
        Transform('txt/text', lambda x: True, Text.HtmlToText, None)
    ])
}


def Get(name: str) -> Format:
    for i in Formats:
        if i.name == name:
            return i
    return Formats[DEFAULT]


def LoadFromFile(path: str) -> (int, FileType):
    file = Istream(path)
    file.Next(3)
    type = file.GetStr(1)
    ans = Types[type].ClassEdit()
    ans.Load(file)
    return type, ans
