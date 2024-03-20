from django.shortcuts import render

from FileType import FileType, Istream

from text import views as Text
from binary import views as Bin


class Format:
    def __init__(self, name: str, funTo, funFrom, type: str, ext: str):
        self.name = name
        # функция преобразования datas в класс
        self.funTo = funTo
        self.funFrom = funFrom
        self.type = type
        self.ext = ext


class Transform:
    def __init__(self, where: str, funCan, funMain, option: str | None):
        self.where = where
        self.funCan = funCan
        self.funMain = funMain
        self.option = option

    def GetHrmlOption(self) -> str:
        if self.option is None:
            return '<p>Их нет</p>'
        with open('project/main/templates/' + self.option, 'r') as file:
            data = file.read()
        return data


class Type:
    def __init__(self, funedit, loadfunedit, classedit, name: str, transform: list[Transform]):
        self.FunEdit = funedit
        self.ClassEdit = classedit
        self.LoadFunEdit = loadfunedit
        self.name = name
        self.transform = transform

    def GetTrans(self, name: str) -> Transform | None:
        for i in self.transform:
            if i.where == name:
                return i
        return None


DEFAULT = 0

Formats = [
    Format('.txt (utf-8) (codes)', Text.TxtFunToUtf8, Text.TxtFunFromUtf8, 'txt/text', '.txt'),
    Format('.txt', Text.TxtFunToASCII, Text.TxtFunFromASCII, 'txt/text', '.txt'),
    Format('(bytes)', Bin.BinTo, Bin.BinFrom, 'bin/bin', '')
]

Types = {
    'txt/text': Type(Text.EditTxt, Text.TxtLoadFunEdit, Text.TxtType, 'Текст',
                     []),
    'bin/bin': Type(Bin.Edit, Bin.EditToFile, Bin.BinType, 'Батник', [])
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
