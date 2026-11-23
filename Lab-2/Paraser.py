import sys
from typing import List, Optional
from lexer import Lexer, LexerError, Token, TokenType


class ParseError(Exception):
      def __init__(self, expected: str, found_token: Token):
            found_desc = (
                  "EOF"
                  if found_token.type == TokenType.EOF
                  else f"{found_token.type.name} ({found_token.lexeme!r})"
            )
            message = (
                  f"Syntax error at line {found_token.line}, col {found_token.column}: "
                  f"expected {expected} but found {found_desc}"
            )
            super().__init__(message)
            self.line = found_token.line
            self.column = found_token.column


class ASTNode:
      def __init__(
            self,
            kind: str,
            vaule: Optional[str] = None,
            children: Optional[List["ASTNode"]] = None,
      ):
            self.kind = kind
            self.vaule = vaule
            self.children = children if children is not None else []

      def format_tree(self) -> str:
            lines: List[str] = []
            self._build_lines(lines, prefix="", is_last=True, is_root=True)
            return "\n".join(lines)

      def _build_lines(
            self, lines: List[str], prefix: str, is_last: bool, is_root: bool
      ) -> None:
            label = f"{self.kind} {self.vaule}" if self.vaule is not None else self.kind
            if is_root:
                  lines.append(label)
                  child_prefix = ""
            else:
                  connector = "└── " if is_last else "├── "
                  lines.append(f"{prefix}{connector}{label}")
                  child_prefix = prefix + ("    " if is_last else "│   ")

            for i, child in enumerate(self.children):
                  child._build_lines(
                        lines,
                        prefix=child_prefix,
                        is_last=(i == len(self.children) - 1),
                        is_root=False,
                  )


class Parser:
      def __init__(self, tokens: List[Token]):
            self.tokens = tokens
            self.current = 0

      def parse(self) -> ASTNode:
            statements: List[ASTNode] = []
            while not self._is_at_end():
                  statements.append(self._statement())
            return ASTNode("program", children=statements)

      # --- Statements

      def _statement(self) -> ASTNode:
            if self._match(TokenType.LET):
                  return self._let_stmt()
            if self._match(TokenType.FUN):
                  return self._fun_decl()
            if self._match(TokenType.PRINT):
                  return self._print_stmt()
            if self._match(TokenType.WHILE):
                  return self._while_stmt()
            if self._match(TokenType.IF):
                  return self._if_stmt()
            if self._match(TokenType.RETURN):
                  return self._return_stmt()
            if self._check(TokenType.LBRACE):
                  return self._block()
            if (
                  self._check(TokenType.IDENTIFIER)
                  and self._peek_next().type == TokenType.ASSIGN
            ):
                  return self._assign_stmt()
            if not self._can_start_expression():
                  raise ParseError("a statement", self._peek())
            return self._expr_stmt()

      def _let_stmt(self) -> ASTNode:
            name_tok = self._consume(TokenType.IDENTIFIER, "variable name after 'let'")
            self._consume(TokenType.ASSIGN, "'=' after variable name")
            initializer = self._expression()
            self._consume(TokenType.SEMICOLON, "';' after variable declaration")
            return ASTNode("Let", vaule=name_tok.lexeme, children=[initializer])

      def _assign_stmt(self) -> ASTNode:
            name_tok = self._advance()
            self._consume(TokenType.ASSIGN, "'=' in assignment")
            expr = self._expression()
            self._consume(TokenType.SEMICOLON, "';' after assignment")
            return ASTNode("Assign", vaule=name_tok.lexeme, children=[expr])

      def _print_stmt(self) -> ASTNode:
            expr = self._expression()
            self._consume(TokenType.SEMICOLON, "';' after print statement")
            return ASTNode("Print", children=[expr])

      def _return_stmt(self) -> ASTNode:
            if self._match(TokenType.SEMICOLON):
                  return ASTNode("Return")
            expr = self._expression()
            self._consume(TokenType.SEMICOLON, "';' after return value")
            return ASTNode("Return", children=[expr])

      def _expr_stmt(self) -> ASTNode:
            expr = self._expression()
            self._consume(TokenType.SEMICOLON, "';' after expression")
            return ASTNode("ExprStmt", children=[expr])

      def _block(self) -> ASTNode:
            self._consume(TokenType.LBRACE, "'{' to start block")
            statements: List[ASTNode] = []
            while not self._check(TokenType.RBRACE) and not self._is_at_end():
                  statements.append(self._statement())
            self._consume(TokenType.RBRACE, "'}' to close block")
            return ASTNode("Block", children=statements)

      def _if_stmt(self) -> ASTNode:
            self._consume(TokenType.LPAREN, "'(' after 'if'")
            condition = self._expression()
            self._consume(TokenType.RPAREN, "')' after if condition")
            then_branch = self._statement()

            children = [condition, then_branch]
            if self._match(TokenType.ELSE):
                  children.append(self._statement())
            return ASTNode("If", children=children)

      def _while_stmt(self) -> ASTNode:
            self._consume(TokenType.LPAREN, "'(' after 'while'")
            condition = self._expression()
            self._consume(TokenType.RPAREN, "')' after while condition")
            body = self._statement()
            return ASTNode("While", children=[condition, body])

      def _fun_decl(self) -> ASTNode:
            name_tok = self._consume(TokenType.IDENTIFIER, "function name after 'fun'")
            self._consume(TokenType.LPAREN, "'(' after function name")

            params: List[ASTNode] = []
            if not self._check(TokenType.RPAREN):
                  param_tok = self._consume(TokenType.IDENTIFIER, "parameter name")
                  params.append(ASTNode("Param", vaule=param_tok.lexeme))
                  while self._match(TokenType.COMMA):
                        param_tok = self._consume(
                              TokenType.IDENTIFIER, "parameter name after ','"
                        )
                        params.append(ASTNode("Param", vaule=param_tok.lexeme))

            self._consume(TokenType.RPAREN, "')' after parameters")
            body = self._block()
            return ASTNode(
                  "FunDecl",
                  vaule=name_tok.lexeme,
                  children=[ASTNode("Params", children=params), body],
            )

      # --- Expressions

      def _expression(self) -> ASTNode:
            return self._logic_or()

      def _logic_or(self) -> ASTNode:
            expr = self._logic_and()
            while self._match(TokenType.OR):
                  op = self._previous().lexeme
                  right = self._logic_and()
                  expr = ASTNode("BinOp", vaule=op, children=[expr, right])
            return expr

      def _logic_and(self) -> ASTNode:
            expr = self._equality()
            while self._match(TokenType.AND):
                  op = self._previous().lexeme
                  right = self._equality()
                  expr = ASTNode("BinOp", vaule=op, children=[expr, right])
            return expr

      def _equality(self) -> ASTNode:
            expr = self._comparison()
            while self._match(TokenType.EQ, TokenType.NEQ):
                  op = self._previous().lexeme
                  right = self._comparison()
                  expr = ASTNode("BinOp", vaule=op, children=[expr, right])
            return expr

      def _comparison(self) -> ASTNode:
            expr = self._term()
            while self._match(TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE):
                  op = self._previous().lexeme
                  right = self._term()
                  expr = ASTNode("BinOp", vaule=op, children=[expr, right])
            return expr

      def _term(self) -> ASTNode:
            expr = self._factor()
            while self._match(TokenType.SLASH, TokenType.STAR, TokenType.PRECENT):
                  op = self._previous().lexeme
                  right = self._unary()
                  expr = ASTNode("BinOp", vaule=op, children=[expr, right])
            return expr

      def _factor(self) -> ASTNode:
            expr = self._logic_and()
            while self._match(TokenType.OR):
                  op = self._previous().lexeme
                  right = self._logic_and()
                  expr = ASTNode("BinOp", vaule=op, children=[expr, right])
            return expr

      def _unary(self) -> ASTNode:
            if self._match(TokenType.Minus, TokenType. BANG):
                  op = self._previous().lexeme
                  right = self._logic_and()
                  expr = ASTNode("BinOp", vaule=op, children=[expr, right])
            return expr

      def _call(self) -> ASTNode:
             expr = self._primary()
             while True:
                   if self._match(TokenType.LPAREN):
                         args: List[ASTNode] = []
                         if not self._check(TokenType.RPAREN):
                               args.append(self._expression())
                               while self._match(TokenType.COMMA):
                                     args.append(self._expression())
                         self._consume(TokenType.RPAREN, "')' after arguments")
                         expr = ASTNode("call", children=[expr] + args)
                   elif self._match(TokenType.LBRACKET):
                         index_expr = self._expression()
                         self._consume(TokenType.RBRACKET, "']' after index expression")
                         expr = ASTNode("Index", children=[expr, index_expr])
                   else:
                         break
             return expr

      def _primary(self) -> ASTNode:
            if self._match(TokenType.FLOAT):
                  return ASTNode("Float", vaule=self._previous().lexeme)
            if self._match(TokenType.INT):
                  return ASTNode("Int", vaule=self._previous().lexeme)
            if self._match(TokenType.STRING):
                  return ASTNode("String", vaule=self._previous().lexeme)
            if self._match(TokenType.TRUE):
                  return ASTNode("Bool", vaule="true")
            if self._match(TokenType.FALSE):
                  return ASTNode("Bool", vaule="false")
            if self._match(TokenType.IDENTIFIER):
                  return ASTNode("Var", vaule=self._previous().lexeme)

            if self._match(TokenType.LBRACKET):
                  elements: List[ASTNode] = []
                  if not self._check(TokenType.RBRACKET):
                        elements.append(self._expression())
                        while self._match(TokenType.COMMA):
                              elements.append(self._expression())
                  self._consume(TokenType.RBRACKET, "']' after array elements")
                  return ASTNode("Array", children=elements)

            if self._match(TokenType.LPAREN):
                  expr = self._expression()
                  self._consume(TokenType.RPAREN, "')' after expression")
                  return expr
            raise ParseError("an expression", self._peek())

      # --- Token Helpers

      def _can_start_expression(self) -> bool:
            return self._peek().type in {
                  TokenType.FLOAT,
                  TokenType.INT,
                  TokenType.STRING,
                  TokenType.IDENTIFIER,
                  TokenType.TRUE,
                  TokenType.FALSE,
                  TokenType.BANG,
                  TokenType.MINUS,
                  TokenType.LBRACKET,
                  TokenType.LPAREN,
            }

      def _match(self, *types: TokenType) -> bool:
            for t in types:
                if self._check(t):
                    self._advance()
                    return True
            return False

      def _consume(self, token_type: TokenType, expected_desc: str) -> Token:
            if self._check(token_type):
                  return self._advance()
            raise ParseError(expected_desc, self._peek())

      def _check(self, token_type: TokenType) -> bool:
            if self._is_at_end():
                  return False
            return self._peek().type == token_type

      def _advance(self) -> Token:
            if not self._is_at_end():
                self.current += 1
            return self._previous()
                
      def _is_at_end(self) -> bool:
            return self._peek().type == TokenType.EOF

      def _peek(self) -> Token:
            return self.tokens[self.current]

      def _peek_next(self) -> Token:
            if self.current + 1 >= len(self.tokens):
                return self.tokens[-1]
            return self.tokens[self.current + 1]

      def _previous(self) -> Token:
            return self.tokens[self.current -1]

      def parse_source(source: str) -> str:
          tokens = Lexer(source).tokenize()
          ast = Parser(tokens).parse()  
          return ast.format_tree()

      if __name__ == "__main__":
            if len(sys.argv) < 2:
                  print("Usage: python parser.py <source_file> [--tokens]", file=sys.stderr)
                  sys.exit(1)

            filepath = sys.argv[1]
            show_tokens = "--tokens" in sys.argv[2:]

            with open(filepath, "r", encoding="utf-8") as f:
                  source_code = f.read()

            try:
                  tokens = Lexer(source_code).tokenize()
                  if show_tokens:
                        for tok in tokens:
                              print(tok)
                  else:
                        tree = Parser(tokens).parse()
                        print(tree.format_tree())
            except (LexerError, ParseError) as err:
                  print(err)
                  sys.exit(1)
                      

            
      
            
