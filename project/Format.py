from django.shortcuts import render

from FileType import FileType, Istream

from text import views as Text


class Format:
    def __init__(self, name: str, funTo, funFrom, type: str, ext: str):
        self.name = name
        # функция преобразования datas в класс
        self.funTo = funTo
        self.funFrom = funFrom
        self.type = type
        self.ext = ext

class Type:
    def __init__(self, funedit, loadfunedit, classedit):
        self.FunEdit = funedit
        self.ClassEdit = classedit
        self.LoadFunEdit = loadfunedit


DEFAULT = 0

Formats = [
    Format('.txt (utf-8)', Text.TxtFunToUtf8, Text.TxtFunFromUtf8, 'txt/text', '.txt'),
    Format('.txt', Text.TxtFunToASCII, Text.TxtFunFromASCII, 'txt/text', '.txt')
]

Types = {
    'txt/text': Type(Text.EditTxt, Text.TxtLoadFunEdit, Text.TxtType)
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
