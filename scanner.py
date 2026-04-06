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
            '~': TokenType.NOT, # O símbolo NOT em Jack é o til
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

    def is_at_end(self) -> bool:
        return self.current >= len(self.code)

    def peek(self, offset=0) -> str:
        """Olha o caractere na posição atual + offset, sem avançar."""
        pos = self.current + offset
        if pos < len(self.code):
            return self.code[pos]
        return '\0' 

    def advance(self) -> str:
        """Avança um caractere, atualiza a linha e retorna o caractere consumido."""
        char = self.code[self.current]
        self.current += 1
        
        if char == '\n':
            self.line += 1
            
        return char

    def skip_line_comment(self):
        """Pula tudo até o final da linha."""
        # Já sabemos que começou com //, então avançamos até o \n ou fim
        while self.peek() != '\n' and not self.is_at_end():
            self.advance()

    def skip_block_comment(self):
        """Pula comentários de bloco /* ... */ ou /** ... */."""
        self.advance()  # consome o '*' (o '/' já foi consumido no skip_whitespace)

        while not self.is_at_end():
            c = self.peek()

            if c == '*' and self.peek(1) == '/':
                self.advance()  # '*'
                self.advance()  # '/'
                return # Comentário fechado com sucesso

            self.advance() # O advance já cuida do self.line += 1 se for '\n'

        # Se saiu do loop sem o return, o arquivo acabou antes do */
        raise SyntaxError(f"Erro na linha {self.line}: Comentário de bloco '/*' não fechado.")
            
    def skip_whitespace(self):
        """Consome espaços em branco, tabs e novas linhas."""
        while not self.is_at_end():
            c = self.peek()
            if c in (' ', '\t', '\r', '\n'):
                self.advance()
            else:
                break

    def read_number(self) -> Token:
        """Lê um número inteiro (integerConstant)."""
        start = self.current
        
        while self.peek().isdigit():
            self.advance()

        # O fatiamento pega do 'start' até o 'current' (que agora está após o último dígito)
        lexeme = self.code[start:self.current]
        return Token(TokenType.NUMBER, lexeme, self.line)


    def tokenize(self) -> list[Token]:
        while not self.is_at_end():
            self.skip_whitespace()
            if self.is_at_end(): break

            ch = self.peek()

            # Caso especial: Barra pode ser divisão ou comentário
            if ch == '/':
                if self.peek(1) == '/':
                    self.advance(); self.advance()
                    self.skip_line_comment()
                    continue
                elif self.peek(1) == '*':
                    self.advance() 
                    self.skip_block_comment()
                    continue
                else:
                    # É o símbolo de divisão '/'
                    lexeme = self.advance()
                    self.tokens.append(Token(self.SYMBOLS[lexeme], lexeme, self.line))
            
            # Identificadores e Keywords
            elif ch.isalpha() or ch == '_':
                self.tokens.append(self.read_identifier())

            # Números
            elif ch.isdigit():
                self.tokens.append(self.read_number())

            # Strings
            elif ch == '"':
                self.tokens.append(self.read_string())

            # Símbolos
            elif ch in self.SYMBOLS:
                lexeme = self.advance()
                self.tokens.append(Token(self.SYMBOLS[lexeme], lexeme, self.line))

            else:
                raise SyntaxError(f"Caractere ilegal '{ch}' na linha {self.line}")

        # Fim de arquivo
        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens

    def read_identifier(self) -> Token:
        """Lê um identificador ou uma palavra-chave (keyword)."""
        # Define o ponto de início (onde está a primeira letra ou _)
        start = self.current
        
        # Continua consumindo enquanto for letra, número ou underscore
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        # Extrai o texto completo
        lexeme = self.code[start:self.current]
        
        # O pulo do gato: tenta buscar no dicionário de keywords.
        # Se não existir, o padrão (default) é TokenType.IDENT.
        token_type = self.KEYWORDS.get(lexeme, TokenType.IDENT)
        
        return Token(token_type, lexeme, self.line)
    
    def read_string(self) -> Token:
        """Lê uma constante de string delimitada por aspas duplas."""
        # A aspa inicial já foi vista pelo tokenize, mas ainda não consumida pelo advance
        # Se o seu tokenize faz 'if ch == "\"": self.read_string()', 
        # então precisamos consumir a aspa de abertura agora:
        self.advance()  
        
        start = self.current

        # Lê até encontrar a aspa de fechamento ou fim do arquivo
        while self.peek() != '"' and not self.is_at_end():
            # No Jack, strings não podem quebrar linha
            if self.peek() == '\n':
                raise SyntaxError(f"Erro na linha {self.line}: String constante não pode conter quebra de linha.")
            self.advance()

        # Se saímos do loop porque o arquivo acabou e não achamos a aspa
        if self.is_at_end():
            raise SyntaxError(f"Erro na linha {self.line}: String não fechada (esperado '\"').")

        # Captura o conteúdo entre as aspas
        lexeme = self.code[start:self.current]
        
        # Consome a aspa de fechamento
        self.advance()  
        
        return Token(TokenType.STRING, lexeme, self.line)