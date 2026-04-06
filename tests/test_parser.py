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
    """Auxiliar para tokenizar código e manter o EOF para o Parser."""
    return Scanner(code).tokenize()

def _normalize_xml(xml_str: str) -> str:
    """Normaliza quebras de linha e espaços para comparação robusta."""
    return xml_str.replace('\r\n', '\n').replace('\r', '\n').strip()

# ==================================================================
# Testes para parse_term
# ==================================================================

class TestParseTerm:
    """Testes para o método parse_term."""

    def test_parse_term_integer(self):
        code = "10"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        assert "<integerConstant> 10 </integerConstant>" in xml

    def test_parse_term_string(self):
        code = '"hello"'
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        assert "<stringConstant> hello </stringConstant>" in xml

    def test_parse_term_keywords(self):
        for kw in ["true", "false", "null", "this"]:
            tokens = _get_tokens(kw)
            parser = Parser(tokens)
            parser.parse_term()
            assert f"<keyword> {kw} </keyword>" in parser.get_xml()

    def test_parse_term_array_access(self):
        code = "arr[i + 1]"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_term()
        xml = parser.get_xml()
        assert "<identifier> arr </identifier>" in xml
        assert "<symbol> [ </symbol>" in xml
        assert "<symbol> + </symbol>" in xml

    def test_parse_term_unary(self):
        """Testa operadores unários - e ~"""
        for op in ["-5", "~isRunning"]:
            tokens = _get_tokens(op)
            parser = Parser(tokens)
            parser.parse_term()
            xml = parser.get_xml()
            assert f"<symbol> {op[0]} </symbol>" in xml

# ==================================================================
# Testes para parse_expression
# ==================================================================

class TestParseExpression:
    def test_expression_logical_and_escaping(self):
        """Testa se o Parser escapa corretamente o símbolo & para XML."""
        code = "a & b"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_expression()
        xml = parser.get_xml()
        assert "<symbol> &amp; </symbol>" in xml

    def test_expression_arithmetic(self):
        code = "1 + 2 * 3"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_expression()
        xml = parser.get_xml()
        assert "<symbol> + </symbol>" in xml
        assert "<symbol> * </symbol>" in xml

# ==================================================================
# Testes para Statements (let, do, if, while, return)
# ==================================================================

class TestStatements:
    def test_parse_let_simple(self):
        code = "let x = 5;"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_let()
        xml = parser.get_xml()
        assert "<letStatement>" in xml
        assert "<symbol> = </symbol>" in xml

    def test_parse_do_call(self):
        code = "do Output.printInt(1);"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_do()
        xml = parser.get_xml()
        assert "<doStatement>" in xml
        assert "<identifier> Output </identifier>" in xml
        assert "<identifier> printInt </identifier>" in xml

    def test_parse_if_else(self):
        code = "if (x < 0) { let x = 0; } else { let x = 1; }"
        tokens = _get_tokens(code)
        parser = Parser(tokens)
        parser.parse_if()
        xml = parser.get_xml()
        assert "<ifStatement>" in xml
        assert "<keyword> else </keyword>" in xml

# ==================================================================
# Testes de Validação com Projetos Oficiais (Nand2Tetris)
# ==================================================================

class TestValidationNand2Tetris:
    """Validação final comparando com arquivos .xml de referência."""

    @pytest.mark.parametrize("project_dir, jack_file", [
        ("Square", "Main.jack"),
        ("Square", "Square.jack"),
        ("Square", "SquareGame.jack"),
        ("ArrayTest", "Main.jack")
    ])
    def test_official_files(self, project_dir, jack_file):
        base_path = f'tests/nand2tetris_files/{project_dir}'
        jack_path = os.path.join(base_path, jack_file)
        xml_ref_path = os.path.join(base_path, jack_file.replace('.jack', '.xml'))

        if not os.path.exists(jack_path) or not os.path.exists(xml_ref_path):
            pytest.skip(f"Arquivos não encontrados em {base_path}")

        with open(jack_path, 'r', encoding='utf-8') as f:
            code = f.read()

        tokens = Scanner(code).tokenize()
        parser = Parser(tokens)
        parser.parse_class()
        
        xml_output = _normalize_xml(parser.get_xml())
        with open(xml_ref_path, 'r', encoding='utf-8') as f:
            xml_ref = _normalize_xml(f.read())

        # Comparação exata de estrutura XML
        assert xml_output == xml_ref, f"Falha na validação de {jack_file}"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])