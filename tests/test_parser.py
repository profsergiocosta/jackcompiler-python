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