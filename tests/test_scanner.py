
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

def test_identificadores_e_keywords():
    """Testa identificadores e palavras reservadas."""
    # Identificador comum
    scanner = Scanner("minhaVar123")
    tokens = scanner.tokenize()
    assert tokens[0].type == TokenType.IDENT
    assert tokens[0].lexeme == "minhaVar123"
    assert tokens[0].to_xml() == '<identifier> minhaVar123 </identifier>'

    # Palavra reservada
    scanner = Scanner("function")
    tokens = scanner.tokenize()
    assert tokens[0].type == TokenType.FUNCTION
    assert tokens[0].lexeme == "function"
    assert tokens[0].to_xml() == '<keyword> function </keyword>'

def test_simbolos_xml():
    """Testa o reconhecimento de símbolos validando a saída XML."""
    code = "x + y;"
    scanner = Scanner(code)
    tokens = scanner.tokenize()

    # ✅ Formato XML esperado (com espaços dentro das tags)
    esperado_xml = [
        '<identifier> x </identifier>',
        '<symbol> + </symbol>',
        '<identifier> y </identifier>',
        '<symbol> ; </symbol>',
    ]
    
    # Ignora o token EOF no final
    tokens_sem_eof = [t for t in tokens if t.type != TokenType.EOF]
    
    for i, xml_esperado in enumerate(esperado_xml):
        assert tokens_sem_eof[i].to_xml() == xml_esperado, \
            f"Token {i} não corresponde:\n  Esperado: {xml_esperado}\n  Obtido:   {tokens_sem_eof[i].to_xml()}"
    
    print("✅ Teste de símbolos com XML passou!")