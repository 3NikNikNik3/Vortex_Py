"""jupyter notebook"""

import json
from django.shortcuts import render
from file_type import FileType, Istream, Ostream
from text import views as Text


class CodeBlock:
    """code block"""

    def __init__(self, source=""):
        self.source = source

    def block_code_to_json(self):
        """block to json"""

        ans = []
        for i in self.source.split('\n'):
            ans.append(i + '\n')
        ans[-1] = ans[-1][:-1]
        return {"source": ans}

    @classmethod
    def json_code_to_block(cls, json_data):
        """json to block"""

        if isinstance(json_data.get("source", ""), list):
            return cls(''.join(json_data.get("source", "")))
        return cls(json_data.get("source", ""))


class CodeBlocks:
    """code blocks"""

    def __init__(self, blocks=None, metadata=None):
        self.blocks = blocks if blocks is not None else []
        self.metadata = metadata if metadata is not None else '{}'

    def block_code_to_json(self):
        """blocks to json"""

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

        json_data["metadata"] = json.loads(self.metadata)

        json_data["nbformat"] = 4
        json_data["nbformat_minor"] = 5

        return json_data

    @classmethod
    def json_code_to_block(cls, json_data):
        """json to block"""

        blocks = []
        metadata = {}
        if "cells" in json_data:
            for cell in json_data["cells"]:
                block = CodeBlock.json_code_to_block(cell)
                blocks.append(block)
        if "metadata" in json_data:
            metadata = json.dumps(json_data['metadata'])

        return cls(blocks, metadata)


class FileJup(FileType):
    """main file"""

    def __init__(self):
        self.data = CodeBlocks()

    def save_(self, file: Ostream):
        """save"""

        file.write_str_to_end(json.dumps(self.data.block_code_to_json()))

    def load(self, file: Istream):
        """load"""

        self.data = CodeBlocks.json_code_to_block(json.loads(file.get_str_to_end()))


def jup_from(data: bytes) -> FileJup:
    """from bytes"""

    ans = FileJup()
    try:
        ans.data = CodeBlocks.json_code_to_block(json.loads(data.decode()))
    except json.decoder.JSONDecodeError:
        ans.data = CodeBlocks()
        ans.data.blocks.append(CodeBlock('error load'))
    return ans


def jup_to(file: FileJup) -> bytes:
    """to bytes"""

    return json.dumps(file.data.block_code_to_json()).encode()


def edit_to_file(req) -> FileJup:
    """from editor"""

    ans = FileJup()
    if 'count' in req:
        for i in range(int(req['count'])):
            if f'block_{i}' in req:
                ans.data.blocks.append(CodeBlock(req[f'block_{i}']))
    if 'metadata' in req:
        ans.data.metadata = req['metadata']
    return ans


def edit(req, file: FileJup):
    """page edit"""

    con = {'count': len(file.data.blocks), 'metadata': file.data.metadata, 'type': 'none'}
    if 'python' in file.data.metadata:
        con['type'] = 'python'
    elif 'javascript' in file.data.metadata:
        con['type'] = 'javascript'
    arr = []
    for i, val in enumerate(file.data.blocks):
        arr.append({'id': i, 'value': val.source})
    con.update({'blocks': arr})
    return render(req, 'jupyter/edit.html', con)


def new_file(req) -> FileJup:
    """create new file"""

    ans = FileJup()
    ans.data.blocks.append(CodeBlock())
    return ans
