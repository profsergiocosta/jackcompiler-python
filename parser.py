from jacktoken import Token, TokenType
from typing import List

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0          # Índice do token atual
        self.xml_output = []      # Lista para construir o XML
        self.indent_level = 0     # Nível de indentação XML

    def peek(self) -> Token:
        """Retorna o token atual sem avançar."""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None  # EOF

    def advance(self) -> Token:
        """Avança para o próximo token e retorna o atual."""
        token = self.peek()
        self.current += 1
        return token

    def match(self, expected_type: TokenType) -> Token:
        """Verifica se o token atual é do tipo esperado e avança."""
        token = self.peek()
        if token and token.type == expected_type:
            return self.advance()
        raise SyntaxError(f"Erro de sintaxe: Esperado {expected_type}, encontrado {token}")

    # --- Helpers de XML ---
    def open_tag(self, tag_name: str):
        """Abre uma tag XML com indentação."""
        indent = "  " * self.indent_level
        self.xml_output.append(f"{indent}<{tag_name}>")
        self.indent_level += 1

    def close_tag(self, tag_name: str):
        """Fecha uma tag XML com indentação."""
        self.indent_level -= 1
        indent = "  " * self.indent_level
        self.xml_output.append(f"{indent}</{tag_name}>")

    def write_token(self, token: Token):
        """Escreve o token atual no XML (usando o to_xml do Token)."""
        indent = "  " * self.indent_level
        # Reutilizamos o método to_xml do Token, mas ajustamos a indentação
        xml_line = token.to_xml() 
        self.xml_output.append(f"{indent}{xml_line}")

    def get_xml(self) -> str:
        return "\n".join(self.xml_output)
    
    def parse_term(self):
        self.open_tag("term")
        token = self.peek()
        
        if token.type in [TokenType.NUMBER]:
            self.write_token(self.advance())
        elif token.type in [TokenType.STRING]:
            self.write_token(self.advance())
        elif token.type in [TokenType.TRUE, TokenType.FALSE, TokenType.NULL, TokenType.THIS]:
            self.write_token(self.advance())
        elif token.type == TokenType.IDENT:
            # Aqui precisaremos de lookahead para distinguir var, array ou call
            # Por enquanto, tratamos como identificador simples
            self.write_token(self.advance())
        else:
            raise SyntaxError(f"Termo esperado, encontrado: {token.lexeme}")
            
        self.close_tag("term")