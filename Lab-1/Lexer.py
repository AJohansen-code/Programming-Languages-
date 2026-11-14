import sys
from enum import Enum, auto
from typing import Any, List


class TokenType(Enum):
    # Literals
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # Operators
    ASSIGN = auto()  # "="
    MINUS = auto()  # "-"
    PLUS = auto()  # "+"
    SLASH = auto()  # "/"
    STAR = auto()  # "*"
    PERCENT = auto()  # "%"
    BANG = auto()  # "!"
    NEQ = auto()  # "!="
    EQ = auto()  # "=="
    LT = auto()  # "<"
    LTE = auto()  # "<="
    GT = auto()  # ">"
    GTE = auto()  # ">="
    AND = auto()  # "&&"
    OR = auto()  # "||"

    # Punctuation
    LPAREN = auto()  # "("
    RPAREN = auto()  # ")"
    LBRACKET = auto()  # "["
    RBRACKET = auto()  # "]"
    LBRACE = auto()  # "{"
    RBRACE = auto()  # "}"
    SEMICOLON = auto()  # ";"
    COMMA = auto()  # ","

    EOF = auto()

    # Keywords
    LET = auto()
    FUN = auto()
    RETURN = auto()
    ELSE = auto()
    WHILE = auto()
    IF = auto()
    TRUE = auto()
    FALSE = auto()
    PRINT = auto()


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: Any, line: int, column: int):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        val_str = f" ({self.literal!r})" if self.literal is not None else ""
        return f"Token({self.type.name}, '{self.lexeme}'{val_str}, at {self.line}:{self.column})"


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"LexerError at {line}:{column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    KEYWORDS = {
        "let": TokenType.LET,
        "fun": TokenType.FUN,
        "else": TokenType.ELSE,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "while": TokenType.WHILE,
        "if": TokenType.IF,
        "return": TokenType.RETURN,
        "print": TokenType.PRINT,
    }

    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.token_start_column = 1

    def tokenize(self) -> List[Token]:
        while not self._is_at_end():
            self.start = self.current
            self.token_start_column = self.column
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    # Scanning the Logic
    def _scan_token(self) -> None:
        c = self._advance()

        if c in (" ", "\r", "\t"):
            return
        if c == "\n":
            self.line += 1
            self.column = 1
            return

        if c == "/" and self._peek() == "/":
            while self._peek() != "\n" and not self._is_at_end():
                self._advance()
            return

        # Punctuation
        if c == "(":
            self._add_token(TokenType.LPAREN)
        elif c == ")":
            self._add_token(TokenType.RPAREN)
        elif c == "[":
            self._add_token(TokenType.LBRACKET)
        elif c == "]":
            self._add_token(TokenType.RBRACKET)
        elif c == "{":
            self._add_token(TokenType.LBRACE)
        elif c == "}":
            self._add_token(TokenType.RBRACE)
        elif c == ";":
            self._add_token(TokenType.SEMICOLON)
        elif c == ",":
            self._add_token(TokenType.COMMA)
        elif c == "+":
            self._add_token(TokenType.PLUS)
        elif c == "-":
            self._add_token(TokenType.MINUS)
        elif c == "*":
            self._add_token(TokenType.STAR)
        elif c == "/":
            self._add_token(TokenType.SLASH)
        elif c == "%":
            self._add_token(TokenType.PERCENT)
        elif c == "!":
            self._add_token(TokenType.NEQ if self._match("=") else TokenType.BANG)
        elif c == "=":
            self._add_token(TokenType.EQ if self._match("=") else TokenType.ASSIGN)
        elif c == "<":
            self._add_token(TokenType.LTE if self._match("=") else TokenType.LT)
        elif c == ">":
            self._add_token(TokenType.GTE if self._match("=") else TokenType.GT)
        elif c == "&":
            if self._match("&"):
                self._add_token(TokenType.AND)
            else:
                raise LexerError("Problem with character '&'. Did you mean to put in '&&'?", self.line, self.token_start_column)
        elif c == "|":
            if self._match("|"):
                self._add_token(TokenType.OR)
            else:
                raise LexerError("Problem with character '|'. Did you mean to put in '||'?", self.line, self.token_start_column)

        # Literals and Identifiers
        elif c == '"':
            self._string()
        elif c.isdigit():
            self._number()
        elif c.isalpha() or c == "_":
            self._identifier()
        else:
            raise LexerError(f"Problem with character: {c!r}", self.line, self.token_start_column)

    # Literal Handlers
    def _string(self) -> None:
        chars: List[str] = []

        while not self._is_at_end() and self._peek() != '"':
            ch = self._advance()
            if ch == "\n":
                raise LexerError("Unterminated string literal across newline", self.line, self.token_start_column)
            if ch == "\\":
                if self._is_at_end():
                    raise LexerError("Unterminated escape sequence at end of file", self.line, self.token_start_column)
                escape_char = self._advance()
                escape_map = {
                    "n": "\n",
                    "r": "\r",
                    "t": "\t",
                    "/": "/",
                    "\\": "\\",
                    '"': '"',
                }
                if escape_char in escape_map:
                    chars.append(escape_map[escape_char])
                else:
                    raise LexerError(f"Unterminated string literal: unknown escape '{escape_char}'", self.line, self.token_start_column)
            else:
                chars.append(ch)

        if self._is_at_end():
            raise LexerError("Unterminated string literal", self.line, self.token_start_column)

        self._advance() 
        value = "".join(chars)
        self._add_token(TokenType.STRING, literal=value)

    def _number(self) -> None:
        is_float = False

        while self._peek().isdigit():
            self._advance()

        if self._peek() == "." and self._peek_next().isdigit():
            is_float = True
            self._advance()
            while self._peek().isdigit():
                self._advance()

        if self._peek() in ("e", "E"):
            next_char = self._peek_next()
            if next_char.isdigit() or (next_char in ("+", "-") and self._peek_ahead(2).isdigit()):
                is_float = True
                self._advance()
                if self._peek() in ("+", "-"):
                    self._advance()
                while self._peek().isdigit():
                    self._advance()

        lexeme = self.source[self.start:self.current]

        if not is_float and len(lexeme) > 1 and lexeme.startswith("0"):
            raise LexerError(
                f"Leading zero are not allowed in integer literals: '{lexeme}'",
                self.line,
                self.token_start_column,
            )

        value = float(lexeme) if is_float else int(lexeme)
        self._add_token(TokenType.FLOAT if is_float else TokenType.INT, literal=value)

    def _identifier(self) -> None:
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        text = self.source[self.start:self.current]
        token_type = self.KEYWORDS.get(text, TokenType.IDENTIFIER)

        literal = None
        if token_type == TokenType.TRUE:
            literal = True
        elif token_type == TokenType.FALSE:
            literal = False

        self._add_token(token_type, literal=literal)

    def _is_at_end(self) -> bool:
        return self.current >= self.length

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        return self._peek_ahead(1)

    def _peek_ahead(self, n: int) -> str:
        index = self.current + n
        if index >= self.length:
            return "\0"
        return self.source[index]

    def _add_token(self, token_type: TokenType, literal: Any = None) -> None:
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, lexeme, literal, self.line, self.token_start_column))


# Demo test run
if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            code = f.read()
    else:
        code = """
        fun factorial(n) {
            if (n <= 1) {
                return 1;
            }
            return n * factorial(n - 1);
        }

        let pi = 3.14159;
        print("Factorial of 5: " + factorial(5));
        """

    try:
        lexer = Lexer(code)
        token_stream = lexer.tokenize()
        for tok in token_stream:
            print(tok)
    except LexerError as err:
        print(err)

