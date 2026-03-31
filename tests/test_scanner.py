
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


    # Palavra reservada
    scanner = Scanner("return")
    tokens = scanner.tokenize()
    assert tokens[0].type == TokenType.FUNCTION
    assert tokens[0].lexeme == "return"
    assert tokens[0].to_xml() == '<keyword> return </keyword>'

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

def test_comentarios_ignorados_xml():
    """Testa que comentários são ignorados e valida o XML do primeiro token."""
    code = ''' 
    /* bloco de comentário */
    let x = 5; // comentário de linha
    '''
    scanner = Scanner(code)
    tokens = [t for t in scanner.tokenize() if t.type != TokenType.EOF]
    
    # ✅ Validação principal: primeiro token deve ser <keyword> let </keyword>
    assert tokens[0].to_xml() == '<keyword> let </keyword>', \
        f"Primeiro token incorreto:\n  Esperado: <keyword> let </keyword>\n  Obtido:   {tokens[0].to_xml()}"
    
    # ✅ Valida sequência completa de tokens em XML
    esperado_xml = [
        '<keyword> let </keyword>',
        '<identifier> x </identifier>',
        '<symbol> = </symbol>',
        '<integerConstant> 5 </integerConstant>',
        '<symbol> ; </symbol>',
    ]
    
    for i, xml_esperado in enumerate(esperado_xml):
        assert tokens[i].to_xml() == xml_esperado, \
            f"Token {i} não corresponde:\n  Esperado: {xml_esperado}\n  Obtido:   {tokens[i].to_xml()}"
    
    # ✅ Garante que nenhum token de comentário apareceu
    for token in tokens:
        assert "comment" not in token.to_xml().lower(), \
            f"Comentário não foi ignorado: {token.to_xml()}"
    
    print("✅ Teste de comentários com XML passou!")

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
    
    scanner = Scanner(code)
    tokens = scanner.tokenize()
    
    # ✅ Remove o token EOF (não aparece no XML do nand2tetris)
    tokens_sem_eof = [t for t in tokens if t.type != TokenType.EOF]
    
    # ✅ Lista completa de XML esperado (ordem exata, formato nand2tetris)
    # ⚠️ Note: espaços dentro de TODAS as tags
    esperado_xml = [
        '<keyword> class </keyword>',
        '<identifier> Main </identifier>',
        '<symbol> { </symbol>',
        '<keyword> function </keyword>',
        '<keyword> void </keyword>',
        '<identifier> main </identifier>',
        '<symbol> ( </symbol>',
        '<symbol> ) </symbol>',
        '<symbol> { </symbol>',
        '<keyword> let </keyword>',
        '<identifier> x </identifier>',
        '<symbol> = </symbol>',
        '<integerConstant> 5 </integerConstant>',
        '<symbol> ; </symbol>',
        '<keyword> return </keyword>',
        '<symbol> ; </symbol>',
        '<symbol> } </symbol>',
        '<symbol> } </symbol>',
    ]
    
    # ✅ Validação 1: número correto de tokens (sem EOF)
    assert len(tokens_sem_eof) == len(esperado_xml), \
        f"Quantidade de tokens incorreta:\n  Esperado: {len(esperado_xml)}\n  Obtido: {len(tokens_sem_eof)}"
    
    # ✅ Validação 2: cada token na posição correta (via XML)
    for i, (token, xml_exp) in enumerate(zip(tokens_sem_eof, esperado_xml)):
        assert token.to_xml() == xml_exp, \
            f"Token {i} na posição incorreta:\n  Esperado: {xml_exp}\n  Obtido:   {token.to_xml()}"
    
    # ✅ Validação 3: gera o XML completo com wrapper <tokens>
    xml_completo = "<tokens>\n"
    for token in tokens_sem_eof:
        xml_completo += token.to_xml() + "\n"
    xml_completo += "</tokens>\n"
    
    # ✅ Validação 4: verifica estrutura do documento XML
    assert xml_completo.startswith("<tokens>\n"), "XML deve iniciar com <tokens>"
    assert xml_completo.endswith("</tokens>\n"), "XML deve terminar com </tokens>"
    
    # ✅ Validação 5: verifica que todos os tokens esperados estão no XML
    for xml_exp in esperado_xml:
        assert xml_exp + "\n" in xml_completo, f"Token não encontrado no XML: {xml_exp}"
    
    # ✅ Opcional: imprime o XML para conferência visual
    print("✅ Teste de código Jack completo com XML passou!")
    print("\n📄 XML Gerado:")
    print(xml_completo)

def test_validacao_nand2tetris_square_main():
    """
    Valida o scanner comparando com o arquivo MainT.xml oficial do nand2tetris.
    Este é o teste definitivo para o projeto!
    """
    import os
    
    # Caminhos dos arquivos
    jack_path = 'tests/nand2tetris_files/Square/Main.jack'
    xml_referencia_path = 'tests/nand2tetris_files/Square/MainT.xml'
    
    # Verifica se os arquivos existem
    assert os.path.exists(jack_path), f"Arquivo Jack não encontrado: {jack_path}"
    assert os.path.exists(xml_referencia_path), f"Arquivo XML de referência não encontrado: {xml_referencia_path}"
    
    # Lê o código Jack
    with open(jack_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Gera tokens com seu scanner
    scanner = Scanner(code)
    tokens = scanner.tokenize()
    
    # Gera XML no formato nand2tetris (sem EOF, com wrapper <tokens>)
    tokens_sem_eof = [t for t in tokens if t.type != TokenType.EOF]
    xml_output = "<tokens>\n"
    for token in tokens_sem_eof:
        xml_output += token.to_xml() + "\n"
    xml_output += "</tokens>\n"
    
    # Lê o XML de referência
    with open(xml_referencia_path, 'r', encoding='utf-8') as f:
        xml_referencia = f.read()
    
    # Normaliza quebras de linha (Windows vs Linux)
    xml_output = xml_output.replace('\r\n', '\n')
    xml_referencia = xml_referencia.replace('\r\n', '\n')
    
    # ✅ Comparação final
    assert xml_output == xml_referencia, \
        f"XML não corresponde!\n\nDiferenças encontradas.\nUse 'diff' para ver detalhes."
    
    print("✅ Validação nand2tetris Square/Main.jack PASSED!")
    print(f"   Tokens gerados: {len(tokens_sem_eof)}")