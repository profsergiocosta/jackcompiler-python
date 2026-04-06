from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # Literals (Valores únicos automáticos)
    NUMBER = auto()
    STRING = auto()
    IDENT = auto()

    # Symbols
    LPAREN = auto(); RPAREN = auto()
    LBRACE = auto(); RBRACE = auto()
    LBRACKET = auto(); RBRACKET = auto()
    COMMA = auto(); SEMICOLON = auto()
    DOT = auto(); PLUS = auto()
    MINUS = auto(); ASTERISK = auto()
    SLASH = auto(); AND = auto()
    OR = auto(); NOT = auto()
    LT = auto(); GT = auto()
    EQ = auto()

    # Keywords
    CLASS = auto(); CONSTRUCTOR = auto(); FUNCTION = auto()
    METHOD = auto(); FIELD = auto(); STATIC = auto()
    VAR = auto(); INT = auto(); CHAR = auto()
    BOOLEAN = auto(); VOID = auto(); TRUE = auto()
    FALSE = auto(); NULL = auto(); THIS = auto()
    LET = auto(); DO = auto(); IF = auto()
    ELSE = auto(); WHILE = auto(); RETURN = auto()

    EOF = auto()

@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int

    def to_xml(self) -> str:
        category = self._get_category()
        value = self._escape_xml(self.lexeme)
        return f"<{category}> {value} </{category}>"
    
    def _get_category(self) -> str:
        """Define a tag XML baseada no intervalo do enum"""
        t = self.type
        # Verificação por identidade de membros, agora eles são únicos!
        if t == TokenType.IDENT:
            return "identifier"
        if t == TokenType.NUMBER:
            return "integerConstant"
        if t == TokenType.STRING:
            return "stringConstant"
        
        # Lógica para Keywords (baseada nos nomes das variantes)
        keywords = {
            "CLASS", "CONSTRUCTOR", "FUNCTION", "METHOD", "FIELD", 
            "STATIC", "VAR", "INT", "CHAR", "BOOLEAN", "VOID", 
            "TRUE", "FALSE", "NULL", "THIS", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN"
        }
        if t.name in keywords:
            return "keyword"
        
        return "symbol"

    def _escape_xml(self, text: str) -> str:
        # Removido as aspas das strings se for stringConstant (padrão Jack/Nand2Tetris)
        if self.type == TokenType.STRING:
            text = text.replace('"', '')
            
        escapes = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
        }
        for char, escaped in escapes.items():
            text = text.replace(char, escaped)
        return text

# Teste de Igualdade
print(f"COMMA == PLUS? {TokenType.COMMA == TokenType.PLUS}") # Retornará False
print (Token(TokenType.COMMA,",",1).to_xml())