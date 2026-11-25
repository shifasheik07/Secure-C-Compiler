%{
#include <stdio.h>
#include "parser.tab.h"
%}

%option noyywrap yylineno

DIGIT [0-9]
LETTER [a-zA-Z_]
ID {LETTER}({LETTER}|{DIGIT})*

%%

"int"       { return INT; }
"char"      { return CHAR; }
"float"     { return FLOAT; }
"double"    { return DOUBLE; }
"void"      { return VOID; }

"if"        { return IF; }
"else"      { return ELSE; }
"while"     { return WHILE; }
"for"       { return FOR; }
"return"    { return RETURN; }

"=="        { return EQ; }
"!="        { return NE; }
"<="        { return LE; }
">="        { return GE; }

"&&"        { return AND; }
"||"        { return OR; }

"++"        { return INC; }
"--"        { return DEC; }

{ID}        { return IDENTIFIER; }

{DIGIT}+    { return NUMBER; }

\"([^\\\n]|\\.)*\" {
    return STRING;
}

[+\-*/%=<>] {
    return yytext[0];
}

[(){};,] {
    return yytext[0];
}

"["         { return '['; }
"]"         { return ']'; }

"//".*      { /* Ignore single-line comments */ }

[ \t\r\n]+  { /* Ignore whitespace */ }

^[ \t]*#[^\n]* {
    /* Ignore preprocessor directives */
}

. {
    printf("Lexical Error at line %d: Unknown character %s\n",
           yylineno, yytext);
    return yytext[0];
}

%%