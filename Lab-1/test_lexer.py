import unittest
from lexer import Lexer, TokenType, LexerError


class TestShiCodeLexer(unittest.TestCase):

    def tokenize(self, source: str):
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        return [t for t in tokens if t.type != TokenType.EOF]

    def test_integers(self):
        tokens = self.tokenize("0 42 1000")
        self.assertEqual([t.type for t in tokens], [TokenType.INT, TokenType.INT, TokenType.INT])
        self.assertEqual([t.literal for t in tokens], [0, 42, 1000])

    def test_floats(self):
        tokens = self.tokenize("3.14 0.5 1e-3 2.5E+2 00.25")
        self.assertEqual([t.type for t in tokens], [TokenType.FLOAT] * 5)
        self.assertAlmostEqual(tokens[0].literal, 3.14)
        self.assertAlmostEqual(tokens[1].literal, 0.5)
        self.assertAlmostEqual(tokens[2].literal, 0.001)
        self.assertAlmostEqual(tokens[3].literal, 250.0)
        self.assertAlmostEqual(tokens[4].literal, 0.25)

    def test_leading_zeros_in_integers_raise_error(self):
        for bad_int in ["00", "01", "007"]:
            with self.subTest(bad_int=bad_int):
                with self.assertRaises(LexerError):
                    self.tokenize(bad_int)

    def test_strings_and_escapes(self):
        tokens = self.tokenize('"hello" "line1\\nline2\\t\\r" "\\"quoted\\\\path\\/file\\""')
        self.assertEqual([t.type for t in tokens], [TokenType.STRING] * 3)
        self.assertEqual(tokens[0].literal, "hello")
        self.assertEqual(tokens[1].literal, "line1\nline2\t\r")
        self.assertEqual(tokens[2].literal, '"quoted\\path/file"')

    def test_keywords_and_identifiers(self):
        tokens = self.tokenize("let fun if else while return print true false my_var count1 fn")
        expected_types = [
            TokenType.LET, TokenType.FUN, TokenType.IF, TokenType.ELSE,
            TokenType.WHILE, TokenType.RETURN, TokenType.PRINT,
            TokenType.TRUE, TokenType.FALSE,
            TokenType.IDENTIFIER, TokenType.IDENTIFIER, TokenType.IDENTIFIER
        ]
        self.assertEqual([t.type for t in tokens], expected_types)
        self.assertEqual(tokens[7].literal, True)
        self.assertEqual(tokens[8].literal, False)
        self.assertEqual(tokens[11].lexeme, "fn")

    def test_operators(self):
        tokens = self.tokenize("+ - * / % == != <= >= < > = && || !")
        expected = [
            TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.PERCENT,
            TokenType.EQ, TokenType.NEQ, TokenType.LTE, TokenType.GTE, TokenType.LT, TokenType.GT,
            TokenType.ASSIGN, TokenType.AND, TokenType.OR, TokenType.BANG
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_delimiters_including_brackets(self):
        tokens = self.tokenize("( ) { } [ ] , ;")
        expected = [
            TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACE, TokenType.RBRACE,
            TokenType.LBRACKET, TokenType.RBRACKET,
            TokenType.COMMA, TokenType.SEMICOLON
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_comments_and_whitespace(self):
        source = """
        // this is a comment
        let arr = [1, 2]; // inline comment
        // trailing comment
        """
        tokens = self.tokenize(source)
        expected = [
            TokenType.LET, TokenType.IDENTIFIER, TokenType.ASSIGN,
            TokenType.LBRACKET, TokenType.INT, TokenType.COMMA, TokenType.INT, TokenType.RBRACKET,
            TokenType.SEMICOLON
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_coordinates(self):
        source = "fun test(a) {\n    return a[0];\n}"
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        self.assertEqual((tokens[0].line, tokens[0].column), (1, 1))
        self.assertEqual((tokens[1].line, tokens[1].column), (1, 5))
        self.assertEqual((tokens[6].line, tokens[6].column), (2, 5))
        self.assertEqual((tokens[8].line, tokens[8].column), (2, 13))


    def test_unterminated_string_raises_error(self):
        with self.assertRaises(LexerError):
            self.tokenize('"unclosed string')

    def test_invalid_escape_raises_error(self):
        with self.assertRaises(LexerError):
            self.tokenize('"bad\\escape"')

    def test_single_ampersand_raises_error(self):
        with self.assertRaises(LexerError):
            self.tokenize("let x = a & b;")


if __name__ == "__main__":
    unittest.main()
