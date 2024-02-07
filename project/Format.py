from FileType import FileType

class Format:
    def __init__(self, name: str, fun):
        self.name = name
        # функция преобразования datas в класс
        self.fun = fun


def test(i):
    return FileType()

DEFAULT = '.txt'
ARRAY = {
    '.txt': Format('.txt', test)
}


def Get(name: str) -> Format:
    if name in ARRAY:
        return ARRAY[name]
    return ARRAY[DEFAULT]
