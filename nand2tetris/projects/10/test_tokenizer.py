import unittest

from tokenizer import Tokenizer, TokenList, Keyword
from tokenizer import TokenType

class MyTestCase(unittest.TestCase):

    def test_has_more_tokens(self):
        tokenizer = Tokenizer([])
        self.assertFalse(tokenizer.has_more_tokens())
        token_list = TokenList(['while','(','a','=','3',")","{","a","=","a",'+',"3","}"])
        tokenizer = Tokenizer(token_list)
        self.assertTrue(tokenizer.has_more_tokens())
    def test_advance(self):
        lst = ['while', '(', 'a', '=', '3', ")", "{", "a", "=", "a", '+', "3", "}"]
        token_lst = TokenList(lst)
        tokenizer = Tokenizer(token_lst)
        for token in lst:
            self.assertEqual(tokenizer.advance(),token)

    def test_token_type(self):
        token_lst = ['while', '(', 'a', '=', '3', ")", "{", "a", "=", "a", '+', "3", "}"]
        token_type_lst = [TokenType.KEYWORD,TokenType.SYMBOL,TokenType.IDENTIFIER,TokenType.SYMBOL,
                          TokenType.INT_CONST,TokenType.SYMBOL,TokenType.SYMBOL,TokenType.IDENTIFIER,
                          TokenType.SYMBOL,TokenType.IDENTIFIER,TokenType.SYMBOL,TokenType.INT_CONST,
                          TokenType.SYMBOL]
        self.assertEqual(len(token_lst),len(token_type_lst))
        tk_lst = TokenList(token_lst)
        tokenizer = Tokenizer(tk_lst)
        for token,token_type in zip(token_lst,token_type_lst):
            tokenizer.advance()
            self.assertEqual(tokenizer.token_type(),token_type)

    def test_keyword(self):
        token_lst = ['while', '(', 'a', '=', '3', ")", "{", "a", "=", "a", '+', "3", "}"]
        tk_lst = TokenList(token_lst)
        tokenizer = Tokenizer(tk_lst)
        current_token = tokenizer.advance()
        self.assertEqual(tokenizer.keyword(),Keyword.WHILE)

    def test_symbol(self):
        token_lst = ['while', '(', 'a', '=', '3', ")", "{", "a", "=", "a", '+', "3", "}"]
        tk_lst = TokenList(token_lst)
        tokenizer = Tokenizer(tk_lst)
        current_token = tokenizer.advance()
        current_token = tokenizer.advance()
        self.assertEqual(tokenizer.symbol(),current_token)

    def test_identifier(self):
        token_lst = ['while', '(', 'a', '=', '3', ")", "{", "a", "=", "a", '+', "3", "}"]
        tk_lst = TokenList(token_lst)
        tokenizer = Tokenizer(tk_lst)
        current_token = tokenizer.advance()
        current_token = tokenizer.advance()
        current_token = tokenizer.advance()
        self.assertEqual(tokenizer.identifier(), current_token)
    def test_int_value(self):
        token_lst = ['while', '(', 'a', '=', '3', ")", "{", "a", "=", "a", '+', "3", "}"]
        tk_lst = TokenList(token_lst)
        tokenizer = Tokenizer(tk_lst)
        current_token = tokenizer.advance()
        current_token = tokenizer.advance()
        current_token = tokenizer.advance()
        current_token = tokenizer.advance()
        current_token = tokenizer.advance()
        self.assertEqual(tokenizer.int_value(), 3)
    def test_string_value(self):
        token_lst = [rf'"asda"']
        tk_lst = TokenList(token_lst)
        tokenizer = Tokenizer(tk_lst)
        current_token = tokenizer.advance()
        self.assertEqual(tokenizer.string_value(), 'asda')
    def test_peak(self):
        token_lst = ['while', '(', 'a', '=', '3', ")", "{", "a", "=", "a", '+', "3", "}"]
        tk_lst = TokenList(token_lst)
        tokenizer = Tokenizer(tk_lst)
        current_token = tokenizer.advance()
        self.assertEqual(tokenizer.peek(),'(')
if __name__ == '__main__':
    unittest.main()
