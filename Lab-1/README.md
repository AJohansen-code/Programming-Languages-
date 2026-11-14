# Lab 1 - ShiCode Lexer

## Language name and summary
The name of the language is ShiCode, the reason for the name is an homage to a well used username used throughout days being online (i.e. ShyBot), I wanted the language to have a bit of a personal touch. ShiCode is a dynamic, expression oriented language with a familiar C-style syntax, first class functions, and curly brace scoping with semicolons. It skips the Python style whitespace sensitivity to keep the token simple and parsing straightforward.  In addition, the operators and the signed numbers are separate at the lexer level to avoid any expression ambiguity. 

## EBNF (or link to GRAMMAR.md)
https://github.com/AJohansen-code/Programming-Languages-/blob/main/Lab-1/GRAMMAR.md

## Environment
* *OS:* Windows 11
* *Language and verison type :* Python 3.11+
* *Dependecies:* Python Standard Library only (`enum`, `typing`, `sys`, `unittest`). No external packages or virtual environment setup required.

## Run
-Run the lexer in the source file
-pass any '.shi' source file path in the command line argument:
'''bash
python lexer.py sample.shi

## Output format (LABEL lexeme; EOF / NEWLINE / INDENT notes)
https://github.com/AJohansen-code/Programming-Languages-/blob/main/Lab-1/test_results.txt

## AI / assistance
Through out this lab project I had Gemini and the Chat function in VSC. There used to help fix errors within the code (i.e. misspelling, inproper placements, or random characters accidently typed in), suggested fixes, and running a test to check if the code functions propely. 
 
