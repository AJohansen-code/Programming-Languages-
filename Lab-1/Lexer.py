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
    ASSIGN = auto() #"="
    MINUS = auto()  #"-"
    PLUS = auto()   #"+"
    SLASH = auto()  #"/"
    STAR = auto()   #"*"
    MODULO = auto() #"%"
    NOT = auto()    #"!"
    NEQ = auto()    #"!="
    EQ = auto()     #"=="
    LT = auto()     #"<"
    LTE = auto()    #"<="
    GT = auto()     #">"
    GTE = auto()    #">="
    AND = auto()    #"&&"
    OR =  auto()    #"||"

    # Punctuation
    LPAREN = auto() #"("
    RPAREN = auto() #")"
    LBRACKET = auto() #"["
    RBRACKET = auto() #"]"
    LBRACE = auto() #"{"
    RBRACE = auto() #"}"
    SEMICOLON = auto() #";"
    COMMA = auto() #","

    EOF = auto() 

    #Keywords
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
        def __init__(self, token_type: TokenType, lexeme: str, literal: Any, line: int, column: int ):
            self.type = token_type
            self.lexeme = lexeme
            self.literal = literal
            self.line = line
            self.column = column

        def __repr__(self) -> str:
            val_str = f" ({self.literal!r})" if self.literal is not None else ""
            return f"Token({self.type.name}, '{self.lexeme}'{val_str}, at {self.line}:{self.column})"

    class LexerError(Exception):
        def __init__(self, message: str, line: int,  column: int):
            super().__init__(f"LexerError at {line}:{column}: {message}")
            self.line = line
            self.column = column

class Lexer:
    TOKEN_SPECIFICATION = [
        ("COMMENT", r"//.*"),
        ("FLOAT", r"\d+\.\d+([eE][+-]?\d+)?"),
        ("INT", r"\d+"),
        ("STRING", r'"([^"\\]|\\.)*"'),
        ("OP_COMPLEX", r"==|!=|<=|>=|&&|\|\|",),
        ("OP_SIMPLE", r"[+\-*/%=<>!]",),
        ("PUNCT", r"[(){}\[\],;]"),
        ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),
        ("NEWLINE", r"\n"),
        ("SKIP", r"[ \t\r]+"),
        ("MISMATCH", r"."),
    ]

    MASTER_REGEX = re.compile(
        "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in TOKEN_SPECIFICATION)
    )

    def __init__(self, source_code: str):
        self.source_code = source_code

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        line_num = 1
        line_start = 0

        for match in self.MASTER_REGEX.finditer(self.source_code):
            kind = match.lastgroup
            vaule = match.group()
            column = match.start() - line_start + 1

            if kind == "SKIP" or kind == "COMMENT":
                continue
            elif kind == "NEWLINE":
                line_start = match.end()
                line_num += 1
                continue
            elif kind == "INT":
                tokens.append(Token(TokenType.INT, int(value), line_num, column))
            elif kind == "FLOAT":
                tokens.append(Token(TokenType.FLOAT, float(value), line_num, column))
            elif kind == "STRING":
                # Process escapes and drop bounding quotation marks
                processed_str = bytes(value[1:-1], "utf-8").decode("unicode_escape")
                tokens.append(Token(TokenType.STRING, processed_str, line_num, column))
            elif kind == "ID":
                if value in KEYWORDS:
                    tokens.append(Token(TokenType.KEYWORD, value, line_num, column))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, value, line_num, column))
            elif kind in ("OP_COMPLEX", "OP_SIMPLE", "PUNCT"):
                tokens.append(Token(TokenType(value), value, line_num, column))
            elif kind == "MISMATCH":
                raise LexerError(f"Unexpected character {value!r}", line_num, column)

        tokens.append(Token(TokenType.EOF, None, line_num, len(self.source_code) - line_start + 1))
        return tokens

#Demo test run
if __name__ == "__main__":
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

    lexer = Lexer(code)
    try:
        token_stream = lexer.tokenize()
        for tok in token_stream:
            print(tok)
    except LexerError as err:
        print(err)

