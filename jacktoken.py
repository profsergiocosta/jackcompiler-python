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

    def to_xml(self) -> str:
        category = self._get_category()
        value = self._escape_xml(self.lexeme)
        return f"<{category}> {value} </{category}>"
    
    def _get_category(self) -> str:
        if self.type == TokenType.IDENT:
            return "identifier"
        elif self.type == TokenType.NUMBER:
            return "integerConstant"
        elif self.type == TokenType.STRING:
            return "stringConstant"
        elif self.type.name in [e.name for e in TokenType if e.value == "keyword"]:
            return "keyword"
        else:
            return "symbol"
    
    def _escape_xml(self, text: str) -> str:
        escapes = {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            '&': '&amp;'
        }
        for char, escaped in escapes.items():
            text = text.replace(char, escaped)
        return text