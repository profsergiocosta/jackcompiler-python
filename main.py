from jacktoken import Token, TokenType

from scanner import Scanner

t = Token(TokenType.NUMBER, "42", 0)

print (t)
print (t.to_xml())

t = Token(TokenType.STRING, "ola mundo", 0)
print (t.to_xml())


t = Token(TokenType.PLUS, "+", 0)
print (t.to_xml())

def test_codigo_jack_completo_xml():
    """
    Testa um trecho completo de código Jack validando o XML token por token.
    Formato exato do nand2tetris: <tokens> wrapper, sem EOF, espaços nas tags.
    """
    code = '''class Main {
    function void main() {
        let x = 5;
        return;
    }
}'''
    print(repr(code))
    
    scanner = Scanner(code)
    tokens = scanner.tokenize()
    print (tokens)

test_codigo_jack_completo_xml()