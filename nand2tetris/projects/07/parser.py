'''=================================================

@Project -> File：07->parser.py

@IDE：PyCharm

@coding: utf-8

@time:2022/5/19 9:58

@author:Pengzhangzhi

@Desc：
translate vm command to assembly command.
=================================================='''


class Parser:
    """
    process VM command for code writer to translate.
    """

    def __init__(self, vm_filename):
        self.arith_dict = {
            "not": "!", "neg": "-", "add": "+", "sub": "-", "and": "&", "or": "|",
            "eq": "JNE", "lt": "JGE", "gt": "JLE",
        }
        self.mapping = {
            "local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT",
            "temp": "5", "pointer": "3",
        }


    def _preprocess(self):
        """strip commands, remove blank lines and comments."""
        ...

    def has_more_command(self):
        """return True if there is more command"""
        ...

    def advance(self, ):
        """read the next command"""
        ...

    def command_type(self):
        """return the current command type"""
        ...

    def arg1(self):
        """return the first arg of current command."""
        ...

    def arg2(self):
        """return the second arg of current command."""
        ...


class CodeWriter:
    """translate vm command to hack assembly commands.

    """

    def __init__(self, filename):
        ...

    def write_arithmetic(self, command: str):
        """write the assembly code of arithmetic operations """
        ...

    def write_push_pop(self, command: str, segment: str, index: int):
        ...


class pipeline:
    def __init__(self, vm_filename):
        self.parser = Parser(vm_filename)
        assembly_path = vm_filename.replace('vm', 'asm')
        self.code_writer = CodeWriter(assembly_path)

    def translate(self):
        """
        translate the given vm file into assembly codes.
        """


if __name__ == '__main':
    ...
