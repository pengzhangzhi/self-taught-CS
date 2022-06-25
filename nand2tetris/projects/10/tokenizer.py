'''=================================================

@Project -> File：10->tokenizer

@IDE：PyCharm

@coding: utf-8

@time:2022/5/19 15:24

@author:Pengzhangzhi

@Desc：
=================================================='''
import enum
from enum import Enum, auto
import re


class TokenList(object):
    def __init__(self, token_lst: [str]):
        self.token_lst = token_lst[::-1]

    def pop(self):
        return self.token_lst.pop()

    def __iter__(self):
        return iter(self.token_lst)

    def __next__(self):
        return next(self.token_lst)

    def __getitem__(self, i):
        return self.token_lst[i]

    def __len__(self):
        return len(self.token_lst)


class Keyword(Enum):
    CLASS = auto()
    constructor = auto()
    function = auto()
    method = auto()
    field = auto()
    static = auto()
    var = auto()
    int = auto()
    char = auto()
    boolean = auto()
    void = auto()
    true = auto()
    false = auto()
    null = auto()
    this = auto()
    let = auto()
    do = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()

    def keyword_lst():
        return ['class', 'constructor', 'function',
                'method', 'field', 'static', 'var', 'int', 'char',
                'boolean', 'void', 'true', 'false', 'null', 'this',
                'let', 'do', 'if', 'else', 'while', 'return']

    def mapping():
        keywords = Keyword.keyword_lst()
        return {str_kw: kw for str_kw, kw in zip(keywords, Keyword)}


class TokenType(Enum):
    KEYWORD = auto()
    SYMBOL = auto()
    IDENTIFIER = auto()
    INT_CONST = auto()
    STRING_CONST = auto()


class list:
    """Inner representation of a command."""

    def __init__(self, first, rest=None):
        self.first = first
        self.rest = rest or nil


class Nil:
    pass


nil = Nil()


class TokenizerException(Exception):
    pass


class EndToken:
    pass


ENDTOKEN = EndToken()


class Tokenizer:
    """A tokenizer that convert a jack file into meaningful tokens. """

    def __init__(self, token_lst: TokenList):
        self.token_lst = token_lst
        self.current_token: str = None
        self.keywords = Keyword.keyword_lst()
        self.symbols = ['{', '}', '(', ')', '[', ']', '.', ',',
                        ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def peek(self):
        """return the next token without reading it."""
        if self.has_more_tokens():
            return self.token_lst[-1]
        else:
            return ENDTOKEN

    def has_more_tokens(self):
        """return true if there has more tokens unreaded."""
        return len(self.token_lst) != 0

    def advance(self):
        """read the next token as the current_token"""
        if self.has_more_tokens():
            self.current_token = self.token_lst.pop()
            return self.current_token
        else:
            return ENDTOKEN

    def token_type(self):
        """return the ret_type of current token.
            raise TypeError if unable to classify current token to any known ret_type.
        """
        digit_regex = re.compile(r'\d+')
        string_regx = re.compile(r'"[a-zA-Z0-9]+"')
        identifier_regex = re.compile(r"[a-zA-Z_]+[a-zA-Z0-9]*")
        if self.current_token in self.keywords:
            ret_type = TokenType.KEYWORD
        elif self.current_token in self.symbols:
            ret_type = TokenType.SYMBOL
        elif digit_regex.match(self.current_token):
            ret_type = TokenType.INT_CONST
        elif string_regx.match(self.current_token):
            ret_type = TokenType.STRING_CONST
        elif identifier_regex.match(self.current_token):
            ret_type = TokenType.IDENTIFIER
        else:
            raise TokenizerException(f"Invalid TokenType, unable to recognize {self.current_token}")
        return ret_type

    def keyword(self):
        """return the keyword of current_token,
            raise TokenizerException when can't find a keyword for current token.
        """
        if self.token_type() == TokenType.KEYWORD:
            keyword = Keyword.mapping().get(self.current_token.lower())
            if keyword is None:
                raise TokenizerException(f"unable to find keyword for `{self.current_token}`")
            return keyword
        else:
            return None

    def symbol(self):
        """return the symbol of current_token"""
        target_type = TokenType.SYMBOL
        return self.evaluate(target_type)

    def evaluate(self, target_type):
        """return the current token if its type is target_type.
        """
        if self.token_type() == target_type:
            return self.current_token
        else:
            return None

    def identifier(self):
        """return the identifier of current_token"""
        target_type = TokenType.IDENTIFIER
        return self.evaluate(target_type)

    def int_value(self):
        """return the int value of current_token"""
        return int(self.evaluate(TokenType.INT_CONST))

    def string_value(self):
        """return the string value of current_token"""
        return self.evaluate(TokenType.STRING_CONST)[1:-1]


class CompilationEngine:
    """
    CompilationEngine read syntax elements in JackTokenizer and generate list obj.
    AF:
        AF(tokenizer) = an engine that analyzes syntax elements from tokenizer and output list obj.
    Rep Invariant:
        tokenizer is a JackTokenizer object that has been initialized to read the Jack class file.
        output_lst is a list obj.
        current_token is an attribute of tokenizer.
    Rep Exposure:
        tokenizer is immutable.
        output_lst is mutable and defensive copy is used.

    """

    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.filed_keywords = ['static', 'field']
        self.subroutine_keywords = ['constructor', 'function', 'method']
        self.user_defined_types = []
        self.build_in_types = ['int', 'char', 'boolean']
        self.build_in_subroutine_types = ['void']
    def compile_class(self)->list:
        """
        compile the class file.
        This method should be called at the beginning of compilation.
        Returns:
            a list obj that represents the class file.
        """
        class_token = self.tokenizer.advance()
        assert  self.tokenizer.token_type() == TokenType.KEYWORD
        assert  self.tokenizer.keyword() == Keyword.CLASS
        class_name = self.assert_identifier()
        self.assert_left_paren()
        var_dec_lst = []
        while self.tokenizer.peek() in self.filed_keywords:
            var_dec_lst.append(self.compile_class_var_dec())
        subroutine_dec_lst = []
        while self.tokenizer.peek() in self.subroutine_keywords:
            subroutine_dec_lst.append(self.compile_subroutine_dec())
        self.assert_right_brace()
        ret = {
            'class': class_token,
            'class_name': class_name,
            'var_dec_lst': var_dec_lst,
            'subroutine_dec_lst': subroutine_dec_lst,
        }
        self.user_defined_types.append(class_name)
        return ret

    def assert_identifier(self):
        class_name = self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenType.IDENTIFIER
        return class_name

    def compile_class_var_dec(self)->list:
        """
        compile the class variable declaration.
        Returns:
            a list obj that represents the class variable declaration.
        """
        var_dec_token = self.tokenizer.advance()
        assert  self.tokenizer.token_type() == TokenType.KEYWORD
        assert  self.tokenizer.keyword() in self.filed_keywords
        var_type = self.compile_var_type()
        var_name = self.assert_identifier()
        self.tokenizer.advance()
        var_name_lst = [var_name]
        while self.tokenizer.peek() == ',':
            self.assert_comma()
            var_name = self.assert_identifier()
        self.assert_semi_colon()
        ret = {
            'var_dec': var_dec_token,
            'var_type': var_type,
            'var_name': var_name_lst,
        }
        return ret

    def assert_semi_colon(self):
        semi_token = self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenType.SYMBOL
        assert self.tokenizer.symbol() == ';'

    def assert_comma(self):
        comma_token = self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenType.SYMBOL
        assert self.tokenizer.symbol() == ','

    def compile_var_type(self)->str:
        """
        compile the variable type.
        Returns:
            a string that represents the variable type.
        """
        var_type = self.tokenizer.advance()
        assert var_type in self.build_in_types + self.user_defined_types
        return var_type

    def compile_subroutine(self)->list:
        """
        compile the subroutine, constructor, method, and function.
        Returns:
            a list obj that represents the subroutine.
        """
        subroutine_token = self.tokenizer.advance()
        assert  self.tokenizer.token_type() == TokenType.KEYWORD
        assert  self.tokenizer.keyword() in self.subroutine_keywords
        subroutine_ret_type = self.tokenizer.advance()
        assert subroutine_ret_type in self.build_in_subroutine_types + self.user_defined_types
        subroutine_name = self.assert_identifier()
        self.assert_left_paren()
        self.tokenizer.advance()
        arg_lst = self.compile_parameter_list()
        self.assert_right_paren()
        subroutine_body_token = self.compile_subroutine_body()
        ret = {
            'subroutine': subroutine_token,
            'subroutine_ret_type': subroutine_ret_type,
            'subroutine_name': subroutine_name,
            'arg_lst': arg_lst,
            'subroutine_body': subroutine_body_token,
        }
        return ret

    def assert_right_paren(self):
        right_paren_token = self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenType.SYMBOL
        assert self.tokenizer.symbol() == ')'

    def assert_left_paren(self):
        left_paren_token = self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenType.SYMBOL
        assert self.tokenizer.symbol() == '('

    def compile_parameter_list(self)->list:
        """
        compile the parameter list.
        Returns:
            a list obj that represents the parameter list.
        """
        if self.tokenizer.peek() in self.build_in_types + self.user_defined_types:
            var_type = self.compile_var_type()
            var_name = self.assert_identifier()
            var_name_lst = [var_name]
            while self.tokenizer.peek() == ',':
                self.assert_comma()
                var_name = self.assert_identifier()
                var_name_lst.append(var_name)
            ret = {
                'var_type': var_type,
                'var_name_lst': var_name_lst,
            }
            return ret
        else:
            return {}

    def compile_subroutine_body(self)->list:
        """
        compile the subroutine body.
        Returns:
            a list obj that represents the subroutine body.
        """
        self.assert_left_brace()
        var_dec_lst = []
        while self.tokenizer.peek() == 'var':
            var_dec_token = self.compile_var_dec()
            var_dec_lst.append(var_dec_token)
        statements = self.compile_statements()
        self.assert_right_brace()
        ret = {
            'var_dec_lst': var_dec_lst,
            'statements': statements,
        }
        return ret


    def assert_right_brace(self):
        right_brace_token = self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenType.SYMBOL
        assert self.tokenizer.symbol() == '}'

    def compile_var_dec(self)->list:
        """
        compile the variable declaration.
        Returns:
            a list obj that represents the variable declaration.
        """
        var_dec_token = self.tokenizer.advance()
        assert self.tokenizer.keyword() == 'var'
        var_type = self.compile_var_type()
        var_name = self.assert_identifier()
        var_name_lst = [var_name]
        while self.tokenizer.peek() == ',':
            self.assert_comma()
            var_name = self.assert_identifier()
            var_name_lst.append(var_name)
        self.assert_semicolon()
        ret = {
            'var_dec_token': var_dec_token,
            'var_type': var_type,
            'var_name_lst': var_name_lst,
        }
        return ret


    def compile_statements(self)->list:
        """
        compile the statements.
        Returns:
            a list obj that represents the statements.
        """
        ...

    def assert_left_squre_bracket(self):
        square_bracket_token = self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenType.SYMBOL
        assert self.tokenizer.symbol() == '['

    def assert_right_squre_bracket(self):
        square_bracket_token = self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenType.SYMBOL
        assert self.tokenizer.symbol() == ']'
    def assert_equal_sign(self):
        equal_sign_token = self.tokenizer.advance()
        assert self.tokenizer.token_type() == TokenType.SYMBOL
        assert self.tokenizer.symbol() == '='
    def compile_let(self)->list:
        """
        compile the let statement.
        Returns:
            a list obj that represents the let statement.
        """
        let_token = self.tokenizer.advance()
        assert self.tokenizer.keyword() == 'let'
        var_name = self.assert_identifier()
        if self.tokenizer.peek() == '[':
            self.assert_left_squre_bracket()
            left_expression = self.compile_expression()
            self.assert_right_squre_bracket()
        self.assert_equal_sign()
        right_expression = self.compile_expression()
        self.assert_semicolon()
        ret = {
            'let_token': let_token,
            'var_name': var_name,
            'left_expression': left_expression,
            'right_expression': right_expression,
        }
        return ret



    def compile_if(self)->list:
        """
        compile the if statement.
        Returns:
            a list obj that represents the if statement.
        """
        if_token = self.assert_if()
        self.assert_left_parenthesis()
        expression = self.compile_expression()
        self.assert_right_parenthesis()
        self.assert_left_brace()
        statements = self.compile_statements()
        self.assert_right_brace()
        if self.tokenizer.keyword() == 'else':
            else_token = self.assert_else()
            self.assert_left_brace()
            else_statements = self.compile_statements()
            self.assert_right_brace()
        else:
            else_token = None
            else_statements = {}
        ret = {
            'if_token': if_token,
            'expression': expression,
            'statements': statements,
            'else_token': else_token,
            'else_statements': else_statements,
        }
        return ret


    def assert_else(self):
        else_token = self.tokenizer.advance()
        assert self.tokenizer.keyword() == 'else'
        return else_token

    def assert_if(self):
        if_token = self.tokenizer.advance()
        assert self.tokenizer.keyword() == 'if'
        return if_token

    def assert_while(self):
        while_token = self.tokenizer.advance()
        assert self.tokenizer.keyword() == 'while'
        return while_token

    def compile_while(self)->list:
        """
        compile the while statement.
        Returns:
            a list obj that represents the while statement.
        """
        while_token = self.assert_while()
        self.assert_left_parenthesis()
        expression = self.compile_expression()
        self.assert_right_parenthesis()
        self.assert_left_brace()
        statements = self.compile_statements()
        self.assert_right_brace()
        ret = {
            'while_token': while_token,
            'expression': expression,
            'statements': statements,
        }
        return ret


    def compile_do(self)->list:
        """
        compile the do statement.
        Returns:
            a list obj that represents the do statement.
        """
        do_token = self.tokenizer.advance()
        assert self.tokenizer.keyword() == 'do'
        subroutine_call = self.compile_subroutine_call()
        self.assert_semicolon()
        ret = {
            'do_token': do_token,
            'subroutine_call': subroutine_call,
        }
        return ret
    def compile_return(self)->list:
        """
        compile the return statement.
        Returns:
            a list obj that represents the return statement.
        """
        return_token = self.tokenizer.advance()
        assert self.tokenizer.keyword() == 'return'
        if self.tokenizer.peek() != ';':
            expression = self.compile_expression()
        else:
            expression = {}
        self.assert_semicolon()
        ret = {
            'return_token': return_token,
            'expression': expression,
        }
        return ret

    def compile_expression(self)->list:
        """
        compile the expression.
        Returns:
            a list obj that represents the expression.
        """
        left_term = self.compile_term()
        op_term_lst = []
        while self.tokenizer.peek() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            op = self.tokenizer.advance()
            term = self.compile_term()
            op_term_lst.append({
                'op': op,
                'term': term,
            })
        ret = {
            'left_term': left_term,
            'op_term_lst': op_term_lst,
        }
        return ret





    def compile_term(self)->list:
        """
        compile the term.
        Returns:
            a list obj that represents the term.
        """
        try:
            return self.compile_subroutine_call()
        except CompilationSubroutineException:
            token = self.tokenizer.advance()
            if self.tokenizer.token_type() == TokenType.INT_CONST:
                ret = {
                    'type': TokenType.INT_CONST,
                    'value': token,
                }
            elif self.tokenizer.token_type() == TokenType.STRING_CONST:
                ret = {
                    'type': TokenType.STRING_CONST,
                    'value': token,
                }
            elif self.tokenizer.token_type() == TokenType.KEYWORD:
                if self.tokenizer.keyword() == 'true':
                    ret = {
                        'type': TokenType.KEYWORD,
                        'value': 'true',
                    }
                elif self.tokenizer.keyword() == 'false':
                    ret = {
                        'type': TokenType.KEYWORD,
                        'value': 'false',
                    }
                elif self.tokenizer.keyword() == 'null':
                    ret = {
                        'type': TokenType.KEYWORD,
                        'value': 'null',
                    }
                elif self.tokenizer.keyword() == 'this':
                    ret = {
                        'type': TokenType.KEYWORD,
                        'value': 'this',
                    }
                else:
                    raise Exception('unexpected keyword: {}'.format(self.tokenizer.keyword()))
            elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
                if self.tokenizer.peek() == '[':
                    expression = self.compile_expression()
                    self.assert_right_squre_bracket()
                    ret = {
                        'type': 'var_expression',
                        'value': token,
                        'expression': expression,
                    }

                # subroutineCall
                else:
                    ret = {
                        'type': 'var',
                        'value': token,
                    }
            elif self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == '(':
                expression = self.compile_expression()
                self.assert_right_parenthesis()
                ret = {
                    'type': 'expression',
                    'value': token,
                    'expression': expression,
                }
            elif token in ['-', '~']:
                term = self.compile_term()
                ret = {
                    'type': 'unary_op',
                    'op': token,
                    'term': term,
                }
            else:
                raise Exception('unexpected token: {}'.format(token))
            return ret






    def compile_expression_list(self)->list:
        """
        compile the expression list.
        Returns:
            a list obj that represents the expression list.
        """
        ...

    def compile_subroutine_call(self)->list:
        """
        compile the subroutine call.
        Returns:
            a list obj that represents the subroutine call.
        """
        name = self.assert_identifier()
        if self.tokenizer.peek() == '(':
            self.assert_left_parenthesis()
            expression_list = self.compile_expression_list()
            self.assert_right_parenthesis()
            return {
                'name': name,
                'expression_list': expression_list,
            }
        elif self.tokenizer.peek() == '.':
            self.assert_dot()
            subroutine_name = self.assert_identifier()
            self.assert_left_paren()
            expression_list = self.compile_expression_list()
            self.assert_right_paren()
            return {
                'name': name,
                'subroutine_name': subroutine_name,
                'expression_list': expression_list,
            }
        else:
            raise CompilationSubroutineException('unexpected token: {}'.format(self.tokenizer.peek()))

class CompilationSubroutineException(Exception):
    pass

class Analyzer(object):
    """read a jack file output a tokenized xml token tree."""

    def __init__(self, filename):
        assert filename.endswith('.jack')
        # with open(filename) as f:
        #     jack_codes = f.readlines()
        #     self.jack_codes = self.preprocess(jack_codes)
        # self.jack_compilation_Engine = CompilationEngine()

    def analyze(self, ):
        self.lst_representation = list('underdefine')
