from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    """Tipos de tokens suportados"""

    # Literals
    NUMBER = "integerConst"
    STRING = "stringConst"
    IDENT = "identifier"

    # Symbols
    LPAREN = "symbol"
    RPAREN = "symbol"
    LBRACE = "symbol"
    RBRACE = "symbol"
    LBRACKET = "symbol"
    RBRACKET = "symbol"
    COMMA = "symbol"
    SEMICOLON = "symbol"
    DOT = "symbol"
    PLUS = "symbol"
    MINUS = "symbol"
    ASTERISK = "symbol"
    SLASH = "symbol"
    AND = "symbol"
    OR = "symbol"
    NOT = "symbol"
    LT = "symbol"
    GT = "symbol"
    EQ = "symbol"

    # Keywords
    CLASS = "keyword"
    CONSTRUCTOR = "keyword"
    FUNCTION = "keyword"
    METHOD = "keyword"
    FIELD = "keyword"
    STATIC = "keyword"
    VAR = "keyword"
    INT = "keyword"
    CHAR = "keyword"
    BOOLEAN = "keyword"
    VOID = "keyword"
    TRUE = "keyword"
    FALSE = "keyword"
    NULL = "keyword"
    THIS = "keyword"
    LET = "keyword"
    DO = "keyword"
    IF = "keyword"
    ELSE = "keyword"
    WHILE = "keyword"
    RETURN = "keyword"

    EOF = "eof"




@dataclass
class Token:
    """Representa um token do programa"""
    type: TokenType
    lexeme: str
    line: int