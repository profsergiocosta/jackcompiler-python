from parser import Parser
from scanner import Scanner

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
    print (xml)
    assert "<letStatement>" in xml
    assert "<keyword> let </keyword>" in xml