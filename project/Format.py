from django.shortcuts import render

from FileType import FileType, Istream

from text import views as Text


class Format:
    def __init__(self, name: str, funTo, funFrom, type: int):
        self.name = name
        # функция преобразования datas в класс
        self.funTo = funTo
        self.funFrom = funFrom
        self.type = type


def test(i):
    return FileType()


def test_(i):
    return bytes()


DEFAULT = 0

Formats = [
    Format('.txt', Text.TxtFunToUtf8, Text.TxtFunFromUtf8, 0)
]

FunEdit = [
    Text.EditTxt
]

ClassEdit = [
    Text.TxtType
]

LoadFunEdit = [
    Text.TxtLoadFunEdit
]


def Get(name: str) -> Format:
    for i in Formats:
        if i.name == name:
            return i
    return Formats[DEFAULT]


def LoadFromFile(path: str) -> (int, FileType):
    file = Istream(path)
    file.Next(3)
    type = file.GetInt(2)
    ans = ClassEdit[type]()
    ans.Load(file)
    return type, ans
