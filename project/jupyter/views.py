import json
from django.shortcuts import render
from FileType import FileType, Istream, Ostream
from text import views as Text


class CodeBlock:
    def __init__(self, source=""):
        self.source = source

    def block_code_to_json(self):
        ans = []
        for i in self.source.split('\n'):
            ans.append(i + '\n')
        ans[-1] = ans[-1][:-1]
        return {"source": ans}

    @classmethod
    def json_code_to_block(cls, json_data):
        if type(json_data.get("source", "")) == list:
            ans = ''
            for i in json_data.get("source", ""):
                ans += i
            return cls(ans)
        return cls(json_data.get("source", ""))


class CodeBlocks:
    def __init__(self, blocks=None, metadata=None):
        self.blocks = blocks if blocks is not None else []
        self.metadata = metadata if metadata is not None else {}

    def block_code_to_json(self):
        json_data = {
            "cells": []
        }

        for block in self.blocks:
            cell_data = {
                "cell_type": "code",
                "execution_count": None,
                "outputs": [],
                "metadata": {},
                **block.block_code_to_json()
            }
            json_data["cells"].append(cell_data)

        json_data["metadata"] = json.dumps(self.metadata)

        json_data["nbformat"] = 4
        json_data["nbformat_minor"] = 5

        return json_data

    @classmethod
    def json_code_to_block(cls, json_data):
        blocks = []
        metadata = {}
        if "cells" in json_data:
            for cell in json_data["cells"]:
                block = CodeBlock.json_code_to_block(cell)
                blocks.append(block)
        if "metadata" in json_data:
            metadata = json.loads(json_data['metadata'])

        return cls(blocks, metadata)


class FileJup(FileType):
    def __init__(self):
        self.data = CodeBlocks()

    def Save_(self, file: Ostream):
        file.WriteStrToEnd(json.dumps(self.data.block_code_to_json()))

    def Load(self, file: Istream):
        self.data = CodeBlocks.json_code_to_block(json.loads(file.GetStrToEnd()))


def JupFrom(data: bytes):
    ans = FileJup()
    try:
        ans.data = CodeBlocks.json_code_to_block(json.loads(data.decode()))
    except json.decoder.JSONDecodeError:
        ans.data = CodeBlocks()
        ans.data.blocks.append(CodeBlock('error load'))
    return ans


def JupTo(file: FileJup):
    return json.dumps(file.data.block_code_to_json()).encode()


def EditToFile(req):
    ans = FileJup()
    if 'count' in req:
        for i in range(int(req['count'])):
            if f'block_{i}' in req:
                ans.data.blocks.append(CodeBlock(req[f'block_{i}']))
    if 'metadata' in req:
        ans.data.metadata = req['metadata']
    return ans


def Edit(req, file: FileJup):
    con = {'count': len(file.data.blocks), 'metadata': file.data.metadata, 'type': 'none'}
    if 'python' in file.data.metadata:
        con['type'] = 'python'
    elif 'javascript' in file.data.metadata:
        con['type'] = 'javascript'
    arr = []
    for i in range(len(file.data.blocks)):
        arr.append({'id': i, 'value': file.data.blocks[i].source})
    con.update({'blocks': arr})
    return render(req, 'jupyter/edit.html', con)


def NewFile(req):
    ans = FileJup()
    ans.data.blocks.append(CodeBlock())
    return ans


'''with open('test.json', 'r') as file: # читаем предложенный файл 'test.json'
    json_data = json.load(file)

code_blocks = CodeBlocks.json_code_to_block(json_data) # Функция из json в класс

# Пример вывода блоков:
for block in code_blocks.blocks:
    print(block)
# Ну и инфы по файлу:
print("Additional Data:", code_blocks.additional_data)

json_output = code_blocks.block_code_to_json() # Функция из класса в json

# Пример преобразоывания в файл 'output.json'
with open('output.json', 'w') as output_file:
    json.dump(json_output, output_file, indent=2)'''
