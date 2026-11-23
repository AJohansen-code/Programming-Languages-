# Lab 2 - ShiCode Parser

## Language name and summary
The name of the language is ShiCode, the reason for the name is an homage to a well used username used throughout days being online (i.e. ShyBot), I wanted the language to have a bit of a personal touch. ShiCode is a dynamic, expression oriented language with a familiar C-style syntax, first class functions, and curly brace scoping with semicolons. It skips the Python style whitespace sensitivity to keep the token simple and parsing straightforward.  In addition, the operators and the signed numbers are separate at the lexer level to avoid any expression ambiguity. 

## EBNF (or link to GRAMMAR.md)
(https://github.com/AJohansen-code/Programming-Languages-/blob/main/Lab-2/GRAMMAR)

## Changes since Lab 1
* *Adding syntactic grammar rules:* Added more to the 'GRAMMAR' by including program, statements, and expressions. The full updated list will be inside the Lab 2 GRAMMAR file.  
* *No token changes:* All the tokens and lexical rules from Lab 1 'lexer.py' didn't need any changes.
* *aligned integer literal to the rules in EBNF:* Tightened `integer_literal` in the EBNF to `"0" | ( non_zero_digit , { digit } )` to match the lexer's rejection of leading zeros (e.g., `007`).


## Environment
* *OS:* Windows 11
* *Language and verison type :* Python 3.11+
* *Dependencies:* Python Standard Library only (`enum`, `typing`, `sys`, `os`, `glob`, `subprocess`). No external packages or virtual environment setup required.

## AI / assistance
Through out this lab project I had Gemini and the Chat function in VSC. There used to help fix errors within the code (i.e. misspelling, inproper placements, or random characters accidently typed in), suggested fixes, and running a test to check if the code functions properly. It also help and assist when VSC couldn't encode the test files due to the 'UTF-8' encoding error, the suggested fixed help get the test results working. 

 ## Run
-Run the Parse in the source file and Print the AST
Run `parser.py` on any ShiCode source file from the repository root: 
```bash
python parser.py tests/01_precedence.input.txt
