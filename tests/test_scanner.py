
from scanner import Scanner
from jacktoken import Token, TokenType

def test_numero_basico():
    """Testa o reconhecimento de um número inteiro simples."""
    code = "289"
    scanner = Scanner(code)
    tokens = scanner.tokenize()
    # ✅ Valida a saída XML diretamente
    assert tokens[0].to_xml() == '<integerConstant> 289 </integerConstant>'
    
    print("✅ Teste passou!")


def test_numeros_com_xml():
    """Testa vários números e valida o XML completo."""
    casos = [
        ("0", '<integerConstant> 0 </integerConstant>'),
        ("289", '<integerConstant> 289 </integerConstant>'),
        ("42", '<integerConstant> 42 </integerConstant>'),
        ("  123  ", '<integerConstant> 123 </integerConstant>'),  # com espaços
    ]
    
    for code, xml_esperado in casos:
        scanner = Scanner(code)
        tokens = scanner.tokenize()
        
        # Ignora token EOF
        token = tokens[0]
        
        assert token.to_xml() == xml_esperado, f"Falhou para: {code}"
    
    print("✅ Todos os testes de número com XML passaram!")

def test_string_basica():
    """Testa o reconhecimento de uma string simples."""
    code = '"hello"'
    scanner = Scanner(code)
    tokens = scanner.tokenize()

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].lexeme == "hello"  # sem aspas!
    assert tokens[0].to_xml() == '<stringConstant> hello </stringConstant>'