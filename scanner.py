from jacktoken import Token, TokenType

class Scanner:
    def __init__(self, code: str):
        self.code = code          # código fonte completo
        self.current = 0          # posição atual no código
        self.line = 1             # linha atual (para mensagens de erro)
        self.tokens = []          # lista de tokens reconhecidos

        # Mapa de símbolos da linguagem Jack
        self.SYMBOLS = {
            '(': TokenType.LPAREN, ')': TokenType.RPAREN,
            '{': TokenType.LBRACE, '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
            ',': TokenType.COMMA, ';': TokenType.SEMICOLON,
            '.': TokenType.DOT, '+': TokenType.PLUS,
            '-': TokenType.MINUS, '*': TokenType.ASTERISK,
            '/': TokenType.SLASH, '&': TokenType.AND,
            '|': TokenType.OR, '<': TokenType.LT,
            '>': TokenType.GT, '=': TokenType.EQ,
        }

        # Mapa de palavras reservadas
        self.KEYWORDS = {
            'class': TokenType.CLASS, 'constructor': TokenType.CONSTRUCTOR,
            'function': TokenType.FUNCTION, 'method': TokenType.METHOD,
            'field': TokenType.FIELD, 'static': TokenType.STATIC,
            'var': TokenType.VAR, 'int': TokenType.INT,
            'char': TokenType.CHAR, 'boolean': TokenType.BOOLEAN,
            'void': TokenType.VOID, 'true': TokenType.TRUE,
            'false': TokenType.FALSE, 'null': TokenType.NULL,
            'this': TokenType.THIS, 'let': TokenType.LET,
            'do': TokenType.DO, 'if': TokenType.IF,
            'else': TokenType.ELSE, 'while': TokenType.WHILE,
            'return': TokenType.RETURN,
        }

    def peek(self, offset=0) -> str:
        """Olha o caractere na posição atual + offset, sem avançar."""
        pos = self.current + offset
        if pos < len(self.code):
            return self.code[pos]
        return '\\0'  # caractere nulo = fim do código

    def advance(self) -> None:
        """Avança um caractere e atualiza a contagem de linhas."""
        if self.current < len(self.code):
            if self.code[self.current] == '\\n':
                self.line += 1
            self.current += 1

    def skip_whitespace(self):
        """Pula espaços, tabs e quebras de linha."""
        while self.peek() in ' \\t\\r\\n':
            if self.peek() == '\\n':
                self.line += 1
            self.advance()

    def read_number(self) -> Token:
        start = self.current
        # Consome todos os dígitos consecutivos
        while self.peek().isdigit():
            self.advance()

        lexeme = self.code[start:self.current]
        return Token(TokenType.NUMBER, lexeme, self.line)
    
    def tokenize(self) -> list:
        while self.current < len(self.code):
            self.skip_whitespace()

            ch = self.peek()

            if ch.isdigit():
                self.tokens.append(self.read_number())
            else:
                # Ainda não lidamos com outros caracteres
                self.advance()

        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens