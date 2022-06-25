'''=================================================

@Project -> File：06->main.py

@IDE：PyCharm

@coding: utf-8

@time:2022/5/16 22:02

@author:Pengzhangzhi

@Desc：
Implementation of a compiler that convert assembly code into binary machine code.

The input is a file (.asm) contains lines of assembly code.
The output is a file of the same name with suffix .hack, contains lines of binary code.

This program contains four parts:

1. parser
2. code, provide the binary code of corresponding assembly code.
3. symbol table, to look up symbols.
4. main
=================================================='''
from enum import Enum


class ParseError(Exception):
    pass


class InvaidCommand(object):
    pass


INVALID_COMMAND = InvaidCommand()


class CommandType(Enum):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2


class Parser:
    """
        A parser that read the asm file and construct them into python internal representations.
        AF:
            AF(asm_file) = a parser that parses the asm_file into internal representations.
        RI:
            asm_file must ends with .asm
        Rep exposure:
            field are mutable.
            defensive copy are used.
    """

    def __init__(self, filename):
        self.filename = filename
        self.asm_file = open(filename, 'r').read().split('\n')
        self.asm_file = self._preprocess(self.asm_file)
        self.current_line_idx = -1
        self.current_command = None

        self.sym_table = {
            "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
            "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5,
            "R6": 6, "R7": 7, "R8": 8, "R9": 9, "R10": 10, "R11": 11,
            "R12": 12, "R13": 13, "R14": 14, "R15": 15,
            "SCREEN": 16384, "KBD": 24576}  # pre-defined label
        self.comp_table = {
            "0": "0101010", "1": "0111111", "-1": "0111010",
            "D": "0001100", "A": "0110000", "!D": "0001101",
            "!A": "0110001", "-D": "0001111", "-A": "0110011",
            "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
            "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
            "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
            "M": "1110000", "!M": "1110001", "-M": "1110011",
            "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
            "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
            "D|M": "1010101"
        }
        self.dest_table = {
            "null": "000", "M": "001", "D": "010", "MD": "011",
            "A": "100", "AM": "101", "AD": "110", "AMD": "111"
        }
        self.jmp_table = {
            "null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
            "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
        }
        self.allocatable_address = 16
        self.binary_code_lst = []
        self.check_rep()

    def check_rep(self):
        assert self.filename.endswith('.asm'), 'filename must end with .asm'
        assert self.current_line_idx < len(self.asm_file), 'the idx is larger than the asm file length!'

    def _preprocess(self, file):
        """

        :param file:
        :return:
        """
        out = []
        for i in range(len(file)):
            file[i] = file[i].strip()

            if not (file[i] == r'\n'
                    or file[i] == ''
                    or file[i].startswith(r'//')):
                file[i] = file[i].split('//')[0].strip()
                out.append(file[i])
        return out

    def advance(self):
        """read the next command if there is next command. else return @TODO"""
        if self.has_more_command():
            self.current_line_idx += 1
            self.current_command = self.asm_file[self.current_line_idx]
            return self.current_command
        else:
            return INVALID_COMMAND

    def get_command_type(self,command):
        import re
        if command.startswith(r"@"):
            return CommandType.A_COMMAND
        elif "(" in command and ")" in command:
            return CommandType.L_COMMAND
        else:
            return CommandType.C_COMMAND

    def command_type(self) -> CommandType:
        """return the type of current command. """
        return self.get_command_type(self.current_command)

    def has_more_command(self) -> bool:
        """return true if there is command unreaded. """
        if self.current_line_idx + 1 >= len(self.asm_file):
            return False
        else:
            return True

    def symbol(self) -> int:
        """return the value of symbol in current command. """
        return self.extract_symbol(self.current_command)

    def is_c_command(self) -> bool:
        """
        return true if the current command is c_command.b
        """
        return self.command_type() == CommandType.C_COMMAND

    def is_a_command(self) -> bool:
        return self.command_type() == CommandType.A_COMMAND

    def is_l_command(self) -> bool:
        return self.command_type() == CommandType.L_COMMAND

    def dest(self):
        """return the 助记符 of current command."""
        if not self.is_c_command():
            return INVALID_COMMAND
        return self.extract_component(self.dest_table,'=')

    def comp(self):
        if not self.is_c_command():
            return INVALID_COMMAND
        if '=' in self.current_command:
            first, rest = self.current_command.split('=')
        else:
            rest = self.current_command
        if ';' in rest:
            comp = rest.split(';')[0]
        else:
            comp = rest
        return self.comp_table.get(comp)

    def jump(self):
        if not self.is_c_command():
            return INVALID_COMMAND
        command = self.current_command
        if ';' in command:
            first, jump = command.split(';')
        else:
            jump = 'null'
        return self.jmp_table.get(jump)

    def extract_component(self,table,split_symbol='='):
        command = self.current_command
        if split_symbol in command:
            key, rest = command.split(split_symbol)
        else:
            key = 'null'
        return table.get(key)

    def c_command(self):
        """return the binary code of a c command"""
        dest_binary = self.dest()
        comp_binary = self.comp()
        jump_binary = self.jump()
        return '111' + dest_binary + comp_binary + jump_binary

    def decimal_2_binary(self,code):
        """convert string of decimal 2 binary"""
        return bin(int(code))[2:]
    def a_command(self):
        "return the binary code of an a command"
        if self.current_command.isdecimal():
            ret = self.decimal_2_binary(self.current_command)
        elif self.symbol() and self.sym_table.get(self.symbol()):
            predefined_symbol = self.sym_table.get(self.symbol())
            ret = self.decimal_2_binary(predefined_symbol)
        else:
            self.sym_table[self.current_command[1:]] = self.allocatable_address
            ret = self.decimal_2_binary(self.allocatable_address)
            self.allocatable_address += 1
        binary = self.decimal_2_binary(ret)
        pad_zero = (16 - len(binary))
        if pad_zero > 0:
            binary = '0'*pad_zero+binary
        return binary

    def extract_symbol(self,command):
        """extract symbol from a command or l command"""
        if self.command_type() == CommandType.A_COMMAND:
            return command[1:]
        if self.command_type() == CommandType.L_COMMAND:
            return command[1:-1]
        else:
            return INVALID_COMMAND
    def first_pass(self):
        "construct the mapping of commands and their addresses"
        f_p_idx = -1
        out = []
        for i in range(len(self.asm_file)):
            command = self.asm_file[i]
            if self.get_command_type(command) == CommandType.L_COMMAND:
                self.sym_table[command[1:-1]] = f_p_idx + 1
            else:
                out.append(command)
        self.asm_file = out

    def second_pass(self):
        """pass the no_label_codes and get the binary code of each line."""
        current_command = self.advance()
        while current_command is not INVALID_COMMAND:
            if self.is_c_command():
                code = self.c_command()
            elif self.is_a_command():
                code = self.a_command()
            else:
                raise Exception(f"{self.current_command}, Invalid command! Unable to parse!")
            self.binary_code_lst.append(code)
            current_command = self.advance()

    def save_binary_code(self):

        filename = self.filename.replace('asm','hack')
        with open(filename, 'w') as f:
            f.write("\n".join(self.binary_code_lst))

    def parse(self):
        self.first_pass()
        self.second_pass()
        self.save_binary_code()


print("parsing!")
import sys
filepath = "max/Max.asm"
parser = Parser(filepath)
parser.parse()
