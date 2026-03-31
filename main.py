# Crie um script simples para gerar XML

from scanner import Scanner
from jacktoken import TokenType

with open('tests/nand2tetris_files/Square/Main.jack', 'r') as f:
    code = f.read()

scanner = Scanner(code)
tokens = scanner.tokenize()

xml = '<tokens>\n'
for t in tokens:
    if t.type != TokenType.EOF:
        xml += t.to_xml() + '\n'
xml += '</tokens>\n'

with open('output/Square/MainT.xml', 'w') as f:
    f.write(xml)

print('✅ XML gerado em output/Square/MainT.xml')
