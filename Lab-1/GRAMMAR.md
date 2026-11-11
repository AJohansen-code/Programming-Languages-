(* ShiCode Lexical EBNF *)

letter    = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
          | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" ;

digit     = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

non_zero_digit   = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

identifier   = ( letter | "_" ) , { letter | digit | "_" } ;

keyword    = "let" | "fun" | "return" | "else" | "while" | "if" | "true" 
            | "false" | "print" ;

integer_literal = digit , { digit } ;
exponent        = ( "e" | "E" ) , [ "+" | "-" ] , digit , { digit } ;
float_literal   = digit , { digit } , "." , digit , { digit } , [ exponent ] ;


escape_seq = "\" , ( '"' | "\" | "/" | "n" | "t" | "r" ) ;
string_char = ( ? all characters ? - ('"' | "\" | "\n" ) ) | escape_seq ; 
string_literal = '"' , { string_char } , '"' ;

punctuation  = "(" | ")" | "{" | "}" | "[" | "]" | "," | ";" ;

operator   = "==" | "!=" | "!" | "<" | ">" | "<=" | ">=" | "=" | "&&" 
           | "||" | "/" | "+" | "-" | "*" | "%" ;

comment    = "//" , { ? all characters ? - "\n" } ;
whitespace = " " | "\t" | "\r" | "\n" ;
