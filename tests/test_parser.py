# tests/test_parser.py
# Testes Unitários para o Analisador Sintático (Parser) - Jack Language

import pytest
import os
from scanner import Scanner
from parser import Parser
from jacktoken import TokenType


# ==================================================================
# Funções Auxiliares para Testes
# ==================================================================

def _get_tokens(code: str):
    """
    Auxiliar para tokenizar código e remover o token EOF.
    """
    tokens = Scanner(code).tokenize()
    return [t for t in tokens if t.type != TokenType.EOF]


def _normalize_xml(xml_str: str) -> str:
    """
    Normaliza quebras de linha e espaços para comparação robusta.
    """
    return xml_str.replace('\r\n', '\n').replace('\r', '\n').strip()


def _load_file(relative_path: str) -> str:
    """
    Carrega o conteúdo de um arquivo relativo à pasta do projeto.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, relative_path)
    
    if not os.path.exists(full_path):
        pytest.skip(f"Arquivo não encontrado: {full_path}")
    
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()


# ==================================================================
# Testes para parse_term
# ==================================================================

class TestParseTerm:
    """Testes para o método parse_term."""

    def test_parse_term_integer(self):
        """Testa termo com número inteiro."""
        code = "10"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<integerConstant> 10 </integerConstant>" in xml

    def test_parse_term_string(self):
        """Testa termo com string."""
        code = '"hello"'
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<stringConstant> hello </stringConstant>" in xml

    def test_parse_term_keyword_true(self):
        """Testa termo com keyword true."""
        code = "true"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<keyword> true </keyword>" in xml

    def test_parse_term_keyword_false(self):
        """Testa termo com keyword false."""
        code = "false"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<keyword> false </keyword>" in xml

    def test_parse_term_keyword_null(self):
        """Testa termo com keyword null."""
        code = "null"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<keyword> null </keyword>" in xml

    def test_parse_term_keyword_this(self):
        """Testa termo com keyword this."""
        code = "this"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<keyword> this </keyword>" in xml

    def test_parse_term_identifier(self):
        """Testa termo com identificador simples."""
        code = "varName"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<identifier> varName </identifier>" in xml

    def test_parse_term_array_access(self):
        """Testa termo com acesso a array: arr[0]."""
        code = "arr[0]"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<identifier> arr </identifier>" in xml
        assert "<symbol> [ </symbol>" in xml
        assert "<integerConstant> 0 </integerConstant>" in xml
        assert "<symbol> ] </symbol>" in xml

    def test_parse_term_subroutine_call_simple(self):
        """Testa termo com chamada de subrotina: foo()."""
        code = "foo()"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<identifier> foo </identifier>" in xml
        assert "<symbol> ( </symbol>" in xml
        assert "<symbol> ) </symbol>" in xml

    def test_parse_term_subroutine_call_method(self):
        """Testa termo com chamada de método: obj.method()."""
        code = "obj.method()"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<identifier> obj </identifier>" in xml
        assert "<symbol> . </symbol>" in xml
        assert "<identifier> method </identifier>" in xml

    def test_parse_term_parenthesized_expression(self):
        """Testa termo com expressão entre parênteses: (x)."""
        code = "(x)"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<symbol> ( </symbol>" in xml
        assert "<identifier> x </identifier>" in xml
        assert "<symbol> ) </symbol>" in xml

    def test_parse_term_unary_minus(self):
        """Testa termo com operador unário -: -5."""
        code = "-5"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<symbol> - </symbol>" in xml
        assert "<integerConstant> 5 </integerConstant>" in xml

    def test_parse_term_unary_not(self):
        """Testa termo com operador unário ~: ~x."""
        code = "~x"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        
        assert "<term>" in xml
        assert "<symbol> ~ </symbol>" in xml
        assert "<identifier> x </identifier>" in xml


# ==================================================================
# Testes para parse_expression
# ==================================================================

class TestParseExpression:
    """Testes para o método parse_expression."""

    def test_parse_expression_simple(self):
        """Testa expressão simples: 10 + 20."""
        code = "10 + 20"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_expression()
        xml = parser.get_xml()
        
        assert "<expression>" in xml
        assert "<integerConstant> 10 </integerConstant>" in xml
        assert "<symbol> + </symbol>" in xml
        assert "<integerConstant> 20 </integerConstant>" in xml

    def test_parse_expression_multiple_ops(self):
        """Testa expressão com múltiplos operadores: 1 + 2 * 3."""
        code = "1 + 2 * 3"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_expression()
        xml = parser.get_xml()
        
        assert "<expression>" in xml
        assert "<symbol> + </symbol>" in xml
        assert "<symbol> * </symbol>" in xml

    def test_parse_expression_comparison(self):
        """Testa expressão com comparação: x < y."""
        code = "x < y"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_expression()
        xml = parser.get_xml()
        
        assert "<expression>" in xml
        assert "<symbol> &lt; </symbol>" in xml  # XML escaped


# ==================================================================
# Testes para parse_let
# ==================================================================

class TestParseLet:
    """Testes para o método parse_let."""

    def test_parse_let_simple(self):
        """Testa let simples: let x = 5;."""
        code = "let x = 5;"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_let()
        xml = parser.get_xml()
        
        assert "<letStatement>" in xml
        assert "<keyword> let </keyword>" in xml
        assert "<identifier> x </identifier>" in xml
        assert "<symbol> = </symbol>" in xml
        assert "<integerConstant> 5 </integerConstant>" in xml
        assert "<symbol> ; </symbol>" in xml

    def test_parse_let_array(self):
        """Testa let com array: let arr[0] = 10;."""
        code = "let arr[0] = 10;"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_let()
        xml = parser.get_xml()
        
        assert "<letStatement>" in xml
        assert "<symbol> [ </symbol>" in xml
        assert "<symbol> ] </symbol>" in xml


# ==================================================================
# Testes para parse_if
# ==================================================================

class TestParseIf:
    """Testes para o método parse_if."""

    def test_parse_if_simple(self):
        """Testa if sem else."""
        code = "if (true) { }"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_if()
        xml = parser.get_xml()
        
        assert "<ifStatement>" in xml
        assert "<keyword> if </keyword>" in xml
        assert "<symbol> ( </symbol>" in xml
        assert "<symbol> ) </symbol>" in xml
        assert "<symbol> { </symbol>" in xml
        assert "<symbol> } </symbol>" in xml

    def test_parse_if_with_else(self):
        """Testa if com else."""
        code = "if (true) { } else { }"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_if()
        xml = parser.get_xml()
        
        assert "<ifStatement>" in xml
        assert "<keyword> else </keyword>" in xml


# ==================================================================
# Testes para parse_while
# ==================================================================

class TestParseWhile:
    """Testes para o método parse_while."""

    def test_parse_while_simple(self):
        """Testa while simples."""
        code = "while (false) { }"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_while()
        xml = parser.get_xml()
        
        assert "<whileStatement>" in xml
        assert "<keyword> while </keyword>" in xml


# ==================================================================
# Testes para parse_do
# ==================================================================

class TestParseDo:
    """Testes para o método parse_do."""

    def test_parse_do_simple(self):
        """Testa do simples: do foo();."""
        code = "do foo();"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_do()
        xml = parser.get_xml()
        
        assert "<doStatement>" in xml
        assert "<keyword> do </keyword>" in xml
        assert "<identifier> foo </identifier>" in xml
        assert "<symbol> ; </symbol>" in xml

    def test_parse_do_with_args(self):
        """Testa do com argumentos: do foo(1, 2);."""
        code = "do foo(1, 2);"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_do()
        xml = parser.get_xml()
        
        assert "<doStatement>" in xml
        assert "<integerConstant> 1 </integerConstant>" in xml
        assert "<integerConstant> 2 </integerConstant>" in xml


# ==================================================================
# Testes para parse_return
# ==================================================================

class TestParseReturn:
    """Testes para o método parse_return."""

    def test_parse_return_empty(self):
        """Testa return sem expressão."""
        code = "return;"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_return()
        xml = parser.get_xml()
        
        assert "<returnStatement>" in xml
        assert "<keyword> return </keyword>" in xml
        assert "<symbol> ; </symbol>" in xml

    def test_parse_return_with_expr(self):
        """Testa return com expressão."""
        code = "return 5;"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_return()
        xml = parser.get_xml()
        
        assert "<returnStatement>" in xml
        assert "<integerConstant> 5 </integerConstant>" in xml


# ==================================================================
# Testes para parse_statements
# ==================================================================

class TestParseStatements:
    """Testes para o método parse_statements."""

    def test_parse_statements_single(self):
        """Testa lista com um statement."""
        code = "return;"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_statements()
        xml = parser.get_xml()
        
        assert "<statements>" in xml
        assert "<returnStatement>" in xml

    def test_parse_statements_multiple(self):
        """Testa lista com múltiplos statements."""
        code = "let x = 1; return;"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_statements()
        xml = parser.get_xml()
        
        assert "<statements>" in xml
        assert "<letStatement>" in xml
        assert "<returnStatement>" in xml


# ==================================================================
# Testes para parse_var_dec
# ==================================================================

class TestParseVarDec:
    """Testes para o método parse_var_dec."""

    def test_parse_var_dec_simple(self):
        """Testa declaração de variável simples."""
        code = "var int x;"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_var_dec()
        xml = parser.get_xml()
        
        assert "<varDec>" in xml
        assert "<keyword> var </keyword>" in xml
        assert "<keyword> int </keyword>" in xml
        assert "<identifier> x </identifier>" in xml

    def test_parse_var_dec_multiple(self):
        """Testa declaração com múltiplas variáveis."""
        code = "var int x, y, z;"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_var_dec()
        xml = parser.get_xml()
        
        assert "<varDec>" in xml
        assert "<identifier> x </identifier>" in xml
        assert "<identifier> y </identifier>" in xml
        assert "<identifier> z </identifier>" in xml


# ==================================================================
# Testes para parse_parameter_list
# ==================================================================

class TestParseParameterList:
    """Testes para o método parse_parameter_list."""

    def test_parse_parameter_list_empty(self):
        """Testa lista de parâmetros vazia."""
        code = ")"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_parameter_list()
        xml = parser.get_xml()
        
        assert "<parameterList>" in xml

    def test_parse_parameter_list_single(self):
        """Testa lista com um parâmetro."""
        code = "int x)"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_parameter_list()
        xml = parser.get_xml()
        
        assert "<parameterList>" in xml
        assert "<keyword> int </keyword>" in xml
        assert "<identifier> x </identifier>" in xml

    def test_parse_parameter_list_multiple(self):
        """Testa lista com múltiplos parâmetros."""
        code = "int x, char y, boolean z)"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_parameter_list()
        xml = parser.get_xml()
        
        assert "<parameterList>" in xml
        assert "<keyword> int </keyword>" in xml
        assert "<keyword> char </keyword>" in xml
        assert "<keyword> boolean </keyword>" in xml


# ==================================================================
# Testes para parse_class_var_dec
# ==================================================================

class TestParseClassVarDec:
    """Testes para o método parse_class_var_dec."""

    def test_parse_class_var_dec_static(self):
        """Testa declaração static."""
        code = "static int x;"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_class_var_dec()
        xml = parser.get_xml()
        
        assert "<classVarDec>" in xml
        assert "<keyword> static </keyword>" in xml

    def test_parse_class_var_dec_field(self):
        """Testa declaração field."""
        code = "field int x;"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_class_var_dec()
        xml = parser.get_xml()
        
        assert "<classVarDec>" in xml
        assert "<keyword> field </keyword>" in xml


# ==================================================================
# Testes para parse_subroutine
# ==================================================================

class TestParseSubroutine:
    """Testes para o método parse_subroutine."""

    def test_parse_subroutine_function(self):
        """Testa declaração de função."""
        code = "function void main() { }"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_subroutine()
        xml = parser.get_xml()
        
        assert "<subroutineDec>" in xml
        assert "<keyword> function </keyword>" in xml
        assert "<keyword> void </keyword>" in xml
        assert "<identifier> main </identifier>" in xml

    def test_parse_subroutine_method(self):
        """Testa declaração de método."""
        code = "method int getValue() { }"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_subroutine()
        xml = parser.get_xml()
        
        assert "<subroutineDec>" in xml
        assert "<keyword> method </keyword>" in xml

    def test_parse_subroutine_constructor(self):
        """Testa declaração de construtor."""
        code = "constructor Foo new() { }"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_subroutine()
        xml = parser.get_xml()
        
        assert "<subroutineDec>" in xml
        assert "<keyword> constructor </keyword>" in xml


# ==================================================================
# Testes para parse_class
# ==================================================================

class TestParseClass:
    """Testes para o método parse_class."""

    def test_parse_class_minimal(self):
        """Testa classe mínima vazia."""
        code = "class Main { }"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_class()
        xml = parser.get_xml()
        
        assert "<class>" in xml
        assert "</class>" in xml
        assert "<keyword> class </keyword>" in xml
        assert "<identifier> Main </identifier>" in xml

    def test_parse_class_with_var(self):
        """Testa classe com variável de classe."""
        code = "class Main { static int x; }"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_class()
        xml = parser.get_xml()
        
        assert "<class>" in xml
        assert "<classVarDec>" in xml

    def test_parse_class_with_function(self):
        """Testa classe com função."""
        code = "class Main { function void main() { return; } }"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_class()
        xml = parser.get_xml()
        
        assert "<class>" in xml
        assert "<subroutineDec>" in xml
        assert "<function void main>" or "<keyword> function </keyword>" in xml


# ==================================================================
# Testes de Validação com Arquivos Oficiais nand2tetris
# ==================================================================

class TestValidationNand2Tetris:
    """Testes de validação com arquivos oficiais do nand2tetris."""

    def test_validacao_parser_square_main(self):
        """
        Valida o Parser comparando com o arquivo Square.xml oficial.
        Este é o teste definitivo para o projeto!
        """
        # Caminhos dos arquivos (ajuste conforme sua estrutura)
        jack_path = 'tests/nand2tetris_files/Square/Main.jack'
        xml_referencia_path = 'tests/nand2tetris_files/Square/Main.xml'
        
        # Verifica se os arquivos existem
        if not os.path.exists(jack_path):
            pytest.skip(f"Arquivo Jack não encontrado: {jack_path}")
        if not os.path.exists(xml_referencia_path):
            pytest.skip(f"Arquivo XML de referência não encontrado: {xml_referencia_path}")
        
        # Lê o código Jack
        with open(jack_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Gera tokens com o Scanner
        tokens = Scanner(code).tokenize()
        
        # Gera XML com o Parser
        parser = Parser(tokens)
        parser.parse_class()
        xml_output = parser.get_xml()
        
        # Lê o XML de referência
        with open(xml_referencia_path, 'r', encoding='utf-8') as f:
            xml_referencia = f.read()
        
        # Normaliza quebras de linha
        xml_output = _normalize_xml(xml_output)
        xml_referencia = _normalize_xml(xml_referencia)
        
        # Comparação final
        assert xml_output == xml_referencia, \
            f"XML não corresponde!\n\nUse 'diff' para ver detalhes."
        
        print(f"✅ Validação nand2tetris Square/Main.jack PASSED!")

    def test_validacao_parser_square(self):
        """Valida o Parser com Square.jack."""
        jack_path = 'tests/nand2tetris_files/Square/Square.jack'
        xml_referencia_path = 'tests/nand2tetris_files/Square/Square.xml'
        
        if not os.path.exists(jack_path):
            pytest.skip(f"Arquivo Jack não encontrado: {jack_path}")
        if not os.path.exists(xml_referencia_path):
            pytest.skip(f"Arquivo XML de referência não encontrado: {xml_referencia_path}")
        
        with open(jack_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tokens = Scanner(code).tokenize()
        parser = Parser(tokens)
        parser.parse_class()
        xml_output = parser.get_xml()
        
        with open(xml_referencia_path, 'r', encoding='utf-8') as f:
            xml_referencia = f.read()
        
        xml_output = _normalize_xml(xml_output)
        xml_referencia = _normalize_xml(xml_referencia)
        
        assert xml_output == xml_referencia, \
            f"XML não corresponde para Square.jack!"
        
        print(f"✅ Validação nand2tetris Square/Square.jack PASSED!")

    def test_validacao_parser_square_game(self):
        """Valida o Parser com SquareGame.jack."""
        jack_path = 'tests/nand2tetris_files/Square/SquareGame.jack'
        xml_referencia_path = 'tests/nand2tetris_files/Square/SquareGame.xml'
        
        if not os.path.exists(jack_path):
            pytest.skip(f"Arquivo Jack não encontrado: {jack_path}")
        if not os.path.exists(xml_referencia_path):
            pytest.skip(f"Arquivo XML de referência não encontrado: {xml_referencia_path}")
        
        with open(jack_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tokens = Scanner(code).tokenize()
        parser = Parser(tokens)
        parser.parse_class()
        xml_output = parser.get_xml()
        
        with open(xml_referencia_path, 'r', encoding='utf-8') as f:
            xml_referencia = f.read()
        
        xml_output = _normalize_xml(xml_output)
        xml_referencia = _normalize_xml(xml_referencia)
        
        assert xml_output == xml_referencia, \
            f"XML não corresponde para SquareGame.jack!"
        
        print(f"✅ Validação nand2tetris Square/SquareGame.jack PASSED!")

    def test_validacao_todos_arquivos(self):
        """
        Valida todos os arquivos .jack da pasta Square contra seus XML de referência.
        """
        pasta_jack = 'tests/nand2tetris_files/Square'
        
        if not os.path.exists(pasta_jack):
            pytest.skip(f"Pasta não encontrada: {pasta_jack}")
        
        arquivos_testados = 0
        arquivos_passaram = 0
        
        for filename in os.listdir(pasta_jack):
            if filename.endswith('.jack'):
                arquivos_testados += 1
                
                jack_path = os.path.join(pasta_jack, filename)
                xml_referencia_path = os.path.join(
                    pasta_jack, 
                    filename.replace('.jack', '.xml')
                )
                
                if not os.path.exists(xml_referencia_path):
                    print(f"⚠️ Sem XML de referência para {filename}")
                    continue
                
                with open(jack_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                tokens = Scanner(code).tokenize()
                parser = Parser(tokens)
                parser.parse_class()
                xml_output = parser.get_xml()
                
                with open(xml_referencia_path, 'r', encoding='utf-8') as f:
                    xml_referencia = f.read()
                
                xml_output = _normalize_xml(xml_output)
                xml_referencia = _normalize_xml(xml_referencia)
                
                if xml_output == xml_referencia:
                    arquivos_passaram += 1
                    print(f"✅ {filename} -> PASSED")
                else:
                    print(f"❌ {filename} -> FAILED")
                    # Salva XML gerado para debug
                    output_path = f"output/Square/{filename.replace('.jack', '.xml')}"
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(xml_output)
                    print(f"   XML gerado salvo em: {output_path}")
        
        assert arquivos_passaram == arquivos_testados, \
            f"{arquivos_testados - arquivos_passaram} arquivo(s) falharam!"
        
        print(f"\n🎉 {arquivos_passaram}/{arquivos_testados} arquivos validados!")


# ==================================================================
# Execução Direta (opcional)
# ==================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])