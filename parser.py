from jacktoken import Token, TokenType
from typing import List, Optional

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.xml_output = []
        self.indent_level = 0

    # ==================================================================
    # Navegação e Casamento
    # ==================================================================

    def peek(self, offset: int = 0) -> Optional[Token]:
        pos = self.current + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None

    def advance(self) -> Token:
        token = self.peek()
        if token:
            self.current += 1
        return token

    def match(self, expected_type: TokenType) -> Token:
        """Verifica o tipo, escreve no XML e avança."""
        token = self.peek()
        if token and token.type == expected_type:
            self.write_token(token)
            return self.advance()
        
        lexeme = token.lexeme if token else "EOF"
        line = token.line if token else "?"
        raise SyntaxError(f"Linha {line}: Esperado {expected_type.name}, obtido '{lexeme}'")

    def match_type(self) -> Token:
        """Casamento para tipos: int, char, boolean ou className (IDENT)."""
        token = self.peek()
        if token and (token.type in [TokenType.INT, TokenType.CHAR, TokenType.BOOLEAN] or token.type == TokenType.IDENT):
            self.write_token(token)
            return self.advance()
        raise SyntaxError(f"Linha {token.line}: Tipo esperado, obtido '{token.lexeme}'")

    # ==================================================================
    # Auxiliares XML
    # ==================================================================

    def open_tag(self, tag: str):
        self.xml_output.append("  " * self.indent_level + f"<{tag}>")
        self.indent_level += 1

    def close_tag(self, tag: str):
        self.indent_level -= 1
        self.xml_output.append("  " * self.indent_level + f"</{tag}>")

    def write_token(self, token: Token):
        self.xml_output.append("  " * self.indent_level + token.to_xml())

    def get_xml(self) -> str:
        return "\n".join(self.xml_output)

    # ==================================================================
    # Regras Gramaticais
    # ==================================================================

    def parse_class(self):
        self.open_tag("class")
        self.match(TokenType.CLASS)
        self.match(TokenType.IDENT)  # className
        self.match(TokenType.LBRACE) # {

        while self.peek() and self.peek().type in [TokenType.STATIC, TokenType.FIELD]:
            self.parse_class_var_dec()

        while self.peek() and self.peek().type in [TokenType.CONSTRUCTOR, TokenType.FUNCTION, TokenType.METHOD]:
            self.parse_subroutine()

        self.match(TokenType.RBRACE) # }
        self.close_tag("class")

    def parse_class_var_dec(self):
        self.open_tag("classVarDec")
        self.write_token(self.advance()) # static | field
        self.match_type()                # type
        self.match(TokenType.IDENT)      # varName
        while self.peek() and self.peek().type == TokenType.COMMA:
            self.match(TokenType.COMMA)
            self.match(TokenType.IDENT)
        self.match(TokenType.SEMICOLON)
        self.close_tag("classVarDec")

    def parse_subroutine(self):
        self.open_tag("subroutineDec")
        self.write_token(self.advance()) # (constructor|function|method)
        
        # Tipo de retorno (void ou type)
        if self.peek().type == TokenType.VOID:
            self.match(TokenType.VOID)
        else:
            self.match_type()

        self.match(TokenType.IDENT)      # subroutineName
        self.match(TokenType.LPAREN)     # (
        self.parse_parameter_list()      # parameterList
        self.match(TokenType.RPAREN)     # )
        self.parse_subroutine_body()     # subroutineBody
        self.close_tag("subroutineDec")

    def parse_parameter_list(self):
        self.open_tag("parameterList")
        if self.peek() and self.peek().type != TokenType.RPAREN:
            self.match_type()
            self.match(TokenType.IDENT)
            while self.peek() and self.peek().type == TokenType.COMMA:
                self.match(TokenType.COMMA)
                self.match_type()
                self.match(TokenType.IDENT)
        self.close_tag("parameterList")

    def parse_subroutine_body(self):
        self.open_tag("subroutineBody")
        self.match(TokenType.LBRACE)
        while self.peek() and self.peek().type == TokenType.VAR:
            self.parse_var_dec()
        self.parse_statements()
        self.match(TokenType.RBRACE)
        self.close_tag("subroutineBody")

    def parse_var_dec(self):
        self.open_tag("varDec")
        self.match(TokenType.VAR)
        self.match_type()
        self.match(TokenType.IDENT)
        while self.peek() and self.peek().type == TokenType.COMMA:
            self.match(TokenType.COMMA)
            self.match(TokenType.IDENT)
        self.match(TokenType.SEMICOLON)
        self.close_tag("varDec")

    def parse_statements(self):
        self.open_tag("statements")
        while self.peek() and self.peek().type in [TokenType.LET, TokenType.IF, TokenType.WHILE, TokenType.DO, TokenType.RETURN]:
            self.parse_statement()
        self.close_tag("statements")

    def parse_statement(self):
        t = self.peek().type
        if t == TokenType.LET: self.parse_let()
        elif t == TokenType.IF: self.parse_if()
        elif t == TokenType.WHILE: self.parse_while()
        elif t == TokenType.DO: self.parse_do()
        elif t == TokenType.RETURN: self.parse_return()

    def parse_let(self):
        self.open_tag("letStatement")
        self.match(TokenType.LET)
        self.match(TokenType.IDENT) # varName
        if self.peek().type == TokenType.LBRACKET:
            self.match(TokenType.LBRACKET)
            self.parse_expression()
            self.match(TokenType.RBRACKET)
        self.match(TokenType.EQ)
        self.parse_expression()
        self.match(TokenType.SEMICOLON)
        self.close_tag("letStatement")

    def parse_do(self):
        self.open_tag("doStatement")
        self.match(TokenType.DO)
        self.parse_subroutine_call_parts() # Lógica compartilhada
        self.match(TokenType.SEMICOLON)
        self.close_tag("doStatement")

    def parse_if(self):
        self.open_tag("ifStatement")
        self.match(TokenType.IF); self.match(TokenType.LPAREN)
        self.parse_expression()
        self.match(TokenType.RPAREN); self.match(TokenType.LBRACE)
        self.parse_statements()
        self.match(TokenType.RBRACE)
        if self.peek() and self.peek().type == TokenType.ELSE:
            self.match(TokenType.ELSE); self.match(TokenType.LBRACE)
            self.parse_statements(); self.match(TokenType.RBRACE)
        self.close_tag("ifStatement")

    def parse_while(self):
        self.open_tag("whileStatement")
        self.match(TokenType.WHILE); self.match(TokenType.LPAREN)
        self.parse_expression()
        self.match(TokenType.RPAREN); self.match(TokenType.LBRACE)
        self.parse_statements(); self.match(TokenType.RBRACE)
        self.close_tag("whileStatement")

    def parse_return(self):
        self.open_tag("returnStatement")
        self.match(TokenType.RETURN)
        if self.peek() and self.peek().type != TokenType.SEMICOLON:
            self.parse_expression()
        self.match(TokenType.SEMICOLON)
        self.close_tag("returnStatement")

    def parse_expression(self):
        self.open_tag("expression")
        self.parse_term()
        ops = [TokenType.PLUS, TokenType.MINUS, TokenType.ASTERISK, TokenType.SLASH, 
               TokenType.AND, TokenType.OR, TokenType.LT, TokenType.GT, TokenType.EQ]
        while self.peek() and self.peek().type in ops:
            self.write_token(self.advance()) # op
            self.parse_term()
        self.close_tag("expression")

    def parse_term(self):
        self.open_tag("term")
        token = self.peek()
        
        if token.type == TokenType.NUMBER: self.write_token(self.advance())
        elif token.type == TokenType.STRING: self.write_token(self.advance())
        elif token.type in [TokenType.TRUE, TokenType.FALSE, TokenType.NULL, TokenType.THIS]:
            self.write_token(self.advance())
        elif token.type == TokenType.LPAREN:
            self.match(TokenType.LPAREN); self.parse_expression(); self.match(TokenType.RPAREN)
        elif token.type in [TokenType.MINUS, TokenType.NOT]: # Operadores unários
            self.write_token(self.advance())
            self.parse_term()
        elif token.type == TokenType.IDENT:
            next_t = self.peek(1)
            if next_t and next_t.type == TokenType.LBRACKET: # Array
                self.match(TokenType.IDENT)
                self.match(TokenType.LBRACKET); self.parse_expression(); self.match(TokenType.RBRACKET)
            elif next_t and next_t.type in [TokenType.LPAREN, TokenType.DOT]: # Subroutine
                self.parse_subroutine_call_parts()
            else: # Var simples
                self.match(TokenType.IDENT)
        self.close_tag("term")

    def parse_subroutine_call_parts(self):
        """Lógica para lidar com chamadas de subrotina sem abrir tag própria."""
        self.match(TokenType.IDENT) # name ou class/var
        if self.peek().type == TokenType.DOT:
            self.match(TokenType.DOT)
            self.match(TokenType.IDENT) # methodName
        self.match(TokenType.LPAREN)
        self.parse_expression_list()
        self.match(TokenType.RPAREN)

    def parse_expression_list(self):
        self.open_tag("expressionList")
        if self.peek() and self.peek().type != TokenType.RPAREN:
            self.parse_expression()
            while self.peek() and self.peek().type == TokenType.COMMA:
                self.match(TokenType.COMMA)
                self.parse_expression()
        self.close_tag("expressionList")