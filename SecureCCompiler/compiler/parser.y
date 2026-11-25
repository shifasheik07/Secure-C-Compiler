%{
#include <stdio.h>
#include <stdlib.h>
#include "../security/security.h"
#include <process.h>

extern FILE *yyin;

int yylex(void);
void yyerror(const char *s);
%}

%define parse.error verbose

/* Token declarations */

%token INT CHAR FLOAT DOUBLE VOID
%token IF ELSE WHILE FOR RETURN
%token IDENTIFIER NUMBER STRING
%nonassoc IFX
%nonassoc ELSE

%token EQ NE LE GE
%token AND OR
%token INC DEC

%left OR
%left AND
%left EQ NE
%left '<' '>' LE GE
%left '+' '-'
%left '*' '/' '%'

%%

/* Grammar rules */

program:
    external_list
    {
        printf("\nSyntax Analysis Successfully!\n");
    }
    ;

external_list:
    external
    | external_list external
    ;

external:
    function_definition
    | declaration
    ;

function_definition:
    type_specifier IDENTIFIER '(' parameter_list_opt ')' compound_statement
    ;

parameter_list_opt:
    /* Empty */
    | parameter_list
    ;

parameter_list:
    parameter
    | parameter_list ',' parameter
    ;

parameter:
    type_specifier IDENTIFIER
    ;

type_specifier:
    INT
    | CHAR
    | FLOAT
    | DOUBLE
    | VOID
    ;

declaration:
    type_specifier init_declarator_list ';'
    ;

init_declarator_list:
    init_declarator
    | init_declarator_list ',' init_declarator
    ;

init_declarator:
    IDENTIFIER
    | IDENTIFIER '=' expression
    | IDENTIFIER '[' array_size_opt ']'
    | IDENTIFIER '[' array_size_opt ']' '=' expression
    ;

array_size_opt:
    /* Empty */
    | NUMBER
    ;

compound_statement:
    '{' statement_list_opt '}'
    ;

statement_list_opt:
    /* Empty */
    | statement_list
    ;

statement_list:
    statement
    | statement_list statement
    ;

statement:
    declaration
    | expression_statement
    | compound_statement
    | selection_statement
    | iteration_statement
    | jump_statement
    ;

expression_statement:
    expression_opt ';'
    ;

expression_opt:
    /* Empty */
    | expression
    ;

selection_statement:
    
    IF '(' expression ')' statement %prec IFX
    | IF '(' expression ')' statement ELSE statement
    ;

iteration_statement:
    WHILE '(' expression ')' statement
    | FOR '(' expression_opt ';' expression_opt ';' expression_opt ')' statement
    ;

jump_statement:
    RETURN expression_opt ';'
    ;

expression:
    IDENTIFIER '=' expression
    | logical_expression
    ;

logical_expression:
    relational_expression
    | logical_expression AND relational_expression
    | logical_expression OR relational_expression
    ;

relational_expression:
    additive_expression
    | relational_expression '<' additive_expression
    | relational_expression '>' additive_expression
    | relational_expression LE additive_expression
    | relational_expression GE additive_expression
    | relational_expression EQ additive_expression
    | relational_expression NE additive_expression
    ;

additive_expression:
    multiplicative_expression
    | additive_expression '+' multiplicative_expression
    | additive_expression '-' multiplicative_expression
    ;

multiplicative_expression:
    primary_expression
    | multiplicative_expression '*' primary_expression
    | multiplicative_expression '/' primary_expression
    | multiplicative_expression '%' primary_expression
    ;

primary_expression:
    IDENTIFIER
    | NUMBER
    | STRING
    | '(' expression ')'
    | IDENTIFIER '(' argument_list_opt ')'
    ;

argument_list_opt:
    /* Empty */
    | argument_list
    ;

argument_list:
    expression
    | argument_list ',' expression
    ;

%%

void yyerror(const char *s)
{
    fprintf(stderr, "Syntax Error: %s\n", s);
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Usage: secure_compiler.exe <C source file>\n");
        return 1;
    }

    int warnings = check_security(argv[1]);

    if (warnings < 0)
    {
        printf("Security analysis failed.\n");
        return 1;
    }

    FILE *source = fopen(argv[1], "r");

    if (source == NULL)
    {
        perror("Cannot open source file");
        return 1;
    }

    yyin = source;

    printf("\n===== SYNTAX ANALYSIS =====\n");

    int result = yyparse();

    fclose(source);

    if (result == 0)
        printf("Program is syntactically valid.\n");
    else
        printf("Program contains syntax errors.\n");

    if (result == 0 && warnings == 0)
    {
        printf("\n===== GCC COMPILATION =====\n");

        char quoted_source[4096];

snprintf(
    quoted_source,
    sizeof(quoted_source),
    "\"%s\"",
    argv[1]
);

const char *gcc_args[] = {
    "gcc",
    "-o",
    "compiled_program.exe",
    quoted_source,
    NULL
};

        int compile_result = _spawnvp(
            _P_WAIT,
            "gcc",
            gcc_args
        );

        if (compile_result == 0)
            printf("Compilation successful! Executable: compiled_program.exe\n");
        else
            printf("GCC compilation failed.\n");
    }
    else
    {
        printf("\nCompilation skipped due to syntax errors or security warnings.\n");
    }

    return (result == 0) ? 0: 1;
}