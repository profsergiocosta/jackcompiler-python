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
    
    def read_string(self) -> Token:
        self.advance()  # consome a aspa inicial "
        start = self.current

        # Lê até encontrar a aspa de fechamento ou fim do arquivo
        while self.peek() != '"' and self.peek() != '\\0':
            if self.peek() == '\\n':
                raise SyntaxError(f"String não fechada na linha {self.line}")
            self.advance()

        if self.peek() == '\\0':
            raise SyntaxError(f"String não fechada na linha {self.line}")

        lexeme = self.code[start:self.current]  # conteúdo sem aspas
        self.advance()  # consome a aspa final "
        return Token(TokenType.STRING, lexeme, self.line)
    
    def read_identifier(self) -> Token:
        start = self.current
        # Aceita letras, dígitos e underscore
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        lexeme = self.code[start:self.current]
        # Decide: é keyword ou identificador comum?
        token_type = self.KEYWORDS.get(lexeme, TokenType.IDENT)
        return Token(token_type, lexeme, self.line)
    
    def tokenize(self) -> list:
        while self.current < len(self.code):
            self.skip_whitespace()

            ch = self.peek()

            if ch.isdigit():
                self.tokens.append(self.read_number())
            elif ch == '"': 
                self.tokens.append(self.read_string())
            elif ch.isalpha() or ch == '_':  
                self.tokens.append(self.read_identifier())
            elif ch in self.SYMBOLS:  
                self.tokens.append(Token(self.SYMBOLS[ch], ch, self.line))
                self.advance()
            else:
                self.advance()

        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens