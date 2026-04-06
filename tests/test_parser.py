from parser import Parser
from scanner import Scanner

from jacktoken import TokenType

def test_parse_term_integer():
    code = "10"
    tokens = Scanner(code).tokenize()
    # Remove EOF para o teste focar no termo
    tokens = [t for t in tokens if t.type.name != 'EOF']

    parser = Parser(tokens)
    parser.parse_term()
    xml = parser.get_xml()

    assert "<term>" in xml
    assert "<integerConstant> 10 </integerConstant>" in xml

def parse_term(self):
        self.open_tag("term")
        token = self.peek()

        if token.type in [TokenType.NUMBER]:
            self.write_token(self.advance())
        elif token.type in [TokenType.STRING]:
            self.write_token(self.advance())
        elif token.type in [TokenType.TRUE, TokenType.FALSE, 
			        TokenType.NULL, TokenType.THIS]:
            self.write_token(self.advance())
        elif token.type == TokenType.IDENT:
            # Aqui precisaremos de lookahead para distinguir var, array ou call
            # Por enquanto, tratamos como identificador simples
            self.write_token(self.advance())
        else:
            raise SyntaxError(f"Termo esperado, encontrado: {token.lexeme}")

        self.close_tag("term")

def test_parse_expression():
    code = "10 + 20"
    tokens = [t for t in Scanner(code).tokenize() if t.type.name != 'EOF']
    parser = Parser(tokens)
    parser.parse_expression()
    xml = parser.get_xml()

    assert "<expression>" in xml
    assert "<symbol> + </symbol>" in xml

def test_parse_let():
    code = "let x = 5;"
    tokens = [t for t in Scanner(code).tokenize() if t.type.name != 'EOF']
    parser = Parser(tokens)
    parser.parse_let()
    xml = parser.get_xml()

    assert "<letStatement>" in xml
    assert "<keyword> let </keyword>" in xml