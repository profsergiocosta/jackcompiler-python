# main.py
import sys
import os
from scanner import Scanner
from parser import Parser

def compile_file(jack_path, output_path):
    """
    Lê o código Jack, tokeniza, faz o parsing e salva a árvore sintática em XML.
    """
    try:
        # Garante que o diretório de saída exista
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(jack_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # 1. Análise Léxica (Scanner)
        scanner = Scanner(code)
        tokens = scanner.tokenize()

        # 2. Análise Sintática (Parser)
        parser = Parser(tokens)
        
        # O parser começa pela regra mestre 'class'
        parser.parse_class()

        # 3. Geração e Salvamento do XML
        xml_content = parser.get_xml()

        with open(output_path, 'w', encoding='utf-8') as f:
            # Adicionamos uma quebra de linha ao final para conformidade com editores
            f.write(xml_content + '\n')

        print(f"✅ Compilado com sucesso: {output_path}")

    except SyntaxError as e:
        print(f"🛑 Erro de Sintaxe: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{jack_path}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Erro inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # Uso: python main.py tests/Square/Main.jack output/Main.xml
    if len(sys.argv) != 3:
        print("Uso: python main.py <arquivo.jack> <saida.xml>")
        sys.exit(1)
        
    compile_file(sys.argv[1], sys.argv[2])