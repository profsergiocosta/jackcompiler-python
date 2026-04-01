# parser.py
# Analisador Sintático para a Linguagem Jack (nand2tetris)

from jacktoken import Token, TokenType
from typing import List, Optional


class Parser:
    """
    Analisador Sintático (Parser) para a linguagem Jack.
    Gera um arquivo XML representando a árvore sintática.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0          # Índice do token atual
        self.xml_output = []      # Lista para construir o XML
        self.indent_level = 0     # Nível de indentação XML

    # ==================================================================
    # Métodos de Navegação de Tokens
    # ==================================================================

    def peek(self, offset: int = 0) -> Optional[Token]:
        """
        Olha o token na posição atual + offset, sem avançar.
        """
        pos = self.current + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None

    def advance(self) -> Optional[Token]:
        """
        Avança para o próximo token e retorna o atual.
        """
        token = self.peek()
        if token:
            self.current += 1
        return token

    def match(self, expected_type: TokenType) -> Token:
        """
        Verifica se o token atual é do tipo esperado, escreve no XML e avança.
        """
        token = self.peek()
        print ("++++", token.to_xml(), expected_type)
        if token and token.type == expected_type:
            #self.write_token(token)  # ✅ Escreve o token no XML
            return self.advance()
        raise SyntaxError(
            f"Erro de sintaxe na linha {token.line if token else '?'}: "
            f"Esperado {expected_type.name}, encontrado {token}"
        )

    def match_keyword(self, expected_lexeme: str) -> Token:
        """
        Verifica se o token atual é uma keyword específica.
        """
        token = self.peek()
        if token and token.type.name in [
            'CLASS', 'CONSTRUCTOR', 'FUNCTION', 'METHOD', 'FIELD', 'STATIC',
            'VAR', 'INT', 'CHAR', 'BOOLEAN', 'VOID', 'TRUE', 'FALSE', 'NULL',
            'THIS', 'LET', 'DO', 'IF', 'ELSE', 'WHILE', 'RETURN'
        ]:
            if token.lexeme == expected_lexeme:
                self.write_token(token)
                return self.advance()
        raise SyntaxError(
            f"Erro de sintaxe: Esperado '{expected_lexeme}', encontrado '{token.lexeme if token else 'EOF'}'"
        )

    # ==================================================================
    # Métodos Auxiliares de XML
    # ==================================================================

    def open_tag(self, tag_name: str):
        """Abre uma tag XML com indentação."""
        indent = "  " * self.indent_level
        self.xml_output.append(f"{indent}<{tag_name}>")
        self.indent_level += 1

    def close_tag(self, tag_name: str):
        """Fecha uma tag XML com indentação."""
        self.indent_level -= 1
        indent = "  " * self.indent_level
        self.xml_output.append(f"{indent}</{tag_name}>")

    def write_token(self, token: Token):
        """Escreve o token no XML usando o método to_xml do Token."""
        indent = "  " * self.indent_level
        xml_line = token.to_xml()
        self.xml_output.append(f"{indent}{xml_line}")

    def get_xml(self) -> str:
        """Retorna o XML completo como string."""
        return "\n".join(self.xml_output)

    # ==================================================================
    # Ponto de Entrada Principal
    # ==================================================================

    def parse_class(self):
        """
        Compila uma classe completa.
        class → 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.open_tag("class")
        print ("TokenType.SEMICOLON",TokenType.SEMICOLON)
        self.match_keyword("class")                    # 'class'
        self.write_token(self.advance())               # className
        self.match(TokenType.LBRACE)                   # '{'
        
        # classVarDec*
        while self.peek() and self.peek().lexeme in ['static', 'field']:
            self.parse_class_var_dec()
            
        # subroutineDec*
        while self.peek() and self.peek().lexeme in ['constructor', 'function', 'method']:
            self.parse_subroutine()
            
        self.match(TokenType.RBRACE)                   # '}'
        self.close_tag("class")

    # ==================================================================
    # Declarações de Classe
    # ==================================================================

    def parse_class_var_dec(self):
        """
        Compila uma declaração de variável de classe (static ou field).
        classVarDec → ('static' | 'field') type varName (',' varName)* ';'
        """
        self.open_tag("classVarDec")
        
        # static ou field
        self.write_token(self.advance())
        
        # type (int, char, boolean, className)
        self.write_token(self.advance())
        
        # varName
        self.write_token(self.match(TokenType.IDENT))
        
        # (',' varName)*
        while self.peek() and self.peek().lexeme == ',':
            self.write_token(self.advance())           # ','
            self.write_token(self.match(TokenType.IDENT))  # varName
        
        self.match(TokenType.SEMICOLON)                # ';'
        
        self.close_tag("classVarDec")

    # ==================================================================
    # Subrotinas (function, method, constructor)
    # ==================================================================

    def parse_subroutine(self):
        """
        Compila uma subrotina completa (method, function, ou constructor).
        subroutineDec → ('constructor'|'function'|'method') type subroutineName '(' parameterList ')' subroutineBody
        """
        self.open_tag("subroutineDec")
        
        # (constructor|function|method)
        self.write_token(self.advance())
        
        # type (ou 'void')
        self.write_token(self.advance())
        
        # subroutineName
        self.write_token(self.match(TokenType.IDENT))
        
        # '('
        self.match(TokenType.LPAREN)
        
        # parameterList
        self.parse_parameter_list()
        
        # ')'
        self.match(TokenType.RPAREN)
        
        # subroutineBody
        self.parse_subroutine_body()
        
        self.close_tag("subroutineDec")

    def parse_parameter_list(self):
        """
        Compila a lista de parâmetros (possivelmente vazia).
        parameterList → ((type varName) (',' type varName)*)?
        """
        self.open_tag("parameterList")
        
        # Se não for ')', temos pelo menos um parâmetro
        if self.peek() and self.peek().type != TokenType.RPAREN:
            # type
            self.write_token(self.advance())
            # varName
            self.write_token(self.match(TokenType.IDENT))
            
            # (',' type varName)*
            while self.peek() and self.peek().lexeme == ',':
                self.write_token(self.advance())       # ','
                self.write_token(self.advance())       # type
                self.write_token(self.match(TokenType.IDENT))  # varName
        
        self.close_tag("parameterList")

    def parse_subroutine_body(self):
        """
        Compila o corpo de uma subrotina.
        subroutineBody → '{' varDec* statements '}'
        """
        self.open_tag("subroutineBody")
        
        self.match(TokenType.LBRACE)                   # '{'
        
        # varDec*
        while self.peek() and self.peek().lexeme == 'var':
            self.parse_var_dec()
        
        # statements
        self.parse_statements()
        
        self.match(TokenType.RBRACE)                   # '}'
        
        self.close_tag("subroutineBody")

    def parse_var_dec(self):
        """
        Compila uma declaração de variável local.
        varDec → 'var' type varName (',' varName)* ';'
        """
        self.open_tag("varDec")
        
        self.match_keyword("var")                      # 'var'
        
        # type
        self.write_token(self.advance())
        
        # varName
        self.write_token(self.match(TokenType.IDENT))
        
        # (',' varName)*
        while self.peek() and self.peek().lexeme == ',':
            self.write_token(self.advance())           # ','
            self.write_token(self.match(TokenType.IDENT))  # varName
        
        self.match(TokenType.SEMICOLON)                # ';'
        
        self.close_tag("varDec")

    # ==================================================================
    # Statements
    # ==================================================================

    def parse_statements(self):
        """
        Compila uma sequência de statements.
        statements → statement*
        """
        self.open_tag("statements")
        
        while self.peek() and self.peek().lexeme in ['let', 'if', 'while', 'do', 'return']:
            self.parse_statement()
        
        self.close_tag("statements")

    def parse_statement(self):
        """
        Despacha para o tipo correto de statement.
        """
        token = self.peek()
        if not token:
            return
            
        if token.lexeme == 'let':
            self.parse_let()
        elif token.lexeme == 'if':
            self.parse_if()
        elif token.lexeme == 'while':
            self.parse_while()
        elif token.lexeme == 'do':
            self.parse_do()
        elif token.lexeme == 'return':
            self.parse_return()
        else:
            raise SyntaxError(f"Statement esperado, encontrado: {token}")

    def parse_let(self):
        """
        Compila um comando let.
        letStatement → 'let' varName ('[' expression ']')? '=' expression ';'
        """
        print ("semicolon", TokenType.SEMICOLON)
        self.open_tag("letStatement")
        
        self.match_keyword("let")                      # 'let'
        self.write_token(self.match(TokenType.IDENT))  # varName
        
        # Verifica acesso a array opcional [...]
        if self.peek() and self.peek().lexeme == '[':
            self.match(TokenType.LBRACKET)             # '['
            self.parse_expression()                    # expression
            self.match(TokenType.RBRACKET)             # ']'
        
        self.match(TokenType.EQ)                       # '='
        self.parse_expression()                        # expression
        print ("espera virgula",TokenType.SEMICOLON)
        self.match(TokenType.SEMICOLON)                # ';'
        print ("aqui achou")
        self.close_tag("letStatement")

    def parse_if(self):
        """
        Compila um comando if (com else opcional).
        ifStatement → 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        self.open_tag("ifStatement")
        
        self.match_keyword("if")                       # 'if'
        self.match(TokenType.LPAREN)                   # '('
        self.parse_expression()                        # expression
        self.match(TokenType.RPAREN)                   # ')'
        self.match(TokenType.LBRACE)                   # '{'
        self.parse_statements()                        # statements
        self.match(TokenType.RBRACE)                   # '}'
        
        # Else opcional
        if self.peek() and self.peek().lexeme == 'else':
            self.match_keyword("else")                 # 'else'
            self.match(TokenType.LBRACE)               # '{'
            self.parse_statements()                    # statements
            self.match(TokenType.RBRACE)               # '}'
        
        self.close_tag("ifStatement")

    def parse_while(self):
        """
        Compila um comando while.
        whileStatement → 'while' '(' expression ')' '{' statements '}'
        """
        self.open_tag("whileStatement")
        
        self.match_keyword("while")                    # 'while'
        self.match(TokenType.LPAREN)                   # '('
        self.parse_expression()                        # expression
        self.match(TokenType.RPAREN)                   # ')'
        self.match(TokenType.LBRACE)                   # '{'
        self.parse_statements()                        # statements
        self.match(TokenType.RBRACE)                   # '}'
        
        self.close_tag("whileStatement")

    def parse_do(self):
        """
        Compila um comando do.
        doStatement → 'do' subroutineCall ';'
        """
        self.open_tag("doStatement")
        
        self.match_keyword("do")                       # 'do'
        self.parse_subroutine_call()                   # subroutineCall
        self.match(TokenType.SEMICOLON)                # ';'
        
        self.close_tag("doStatement")

    def parse_return(self):
        """
        Compila um comando return.
        returnStatement → 'return' expression? ';'
        """
        self.open_tag("returnStatement")
        
        self.match_keyword("return")                   # 'return'
        
        # Expressão opcional (return; ou return x;)
        if self.peek() and self.peek().type != TokenType.SEMICOLON:
            self.parse_expression()                    # expression (opcional)
        
        self.match(TokenType.SEMICOLON)                # ';'
        
        self.close_tag("returnStatement")

    # ==================================================================
    # Expressões e Termos
    # ==================================================================

    def parse_expression(self):
        """
        Compila uma expressão.
        expression → term (op term)*
        """
        self.open_tag("expression")
        
        self.parse_term()
        
        # (op term)*
        while self.peek() and self._is_operator(self.peek().lexeme):
            self.write_token(self.advance())           # op
            self.parse_term()                          # term
        
        self.close_tag("expression")

    def _is_operator(self, lexeme: str) -> bool:
        """Verifica se um lexema é um operador válido."""
        return lexeme in ['+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def parse_term(self):
        """
        Compila um termo.
        term → integerConstant | stringConstant | keywordConstant | varName | 
               varName '[' expression ']' | subroutineCall | '(' expression ')' | 
               unaryOp term
        
        Usa lookahead para distinguir entre:
        - variável simples (x)
        - acesso a array (x[expr])
        - chamada de subrotina (x() ou x.y())
        """
        self.open_tag("term")
        
        token = self.peek()

        print (">>>", token.to_xml())
        
        if not token:
            raise SyntaxError("Termo esperado, encontrado EOF")
        
        # integerConstant
        if token.type == TokenType.NUMBER:
            self.write_token(self.advance())
        
        # stringConstant
        elif token.type == TokenType.STRING:
            self.write_token(self.advance())
        
        # keywordConstant (true, false, null, this)
        elif token.type in [TokenType.TRUE, TokenType.FALSE, TokenType.NULL, TokenType.THIS]:
            self.write_token(self.advance())
        
        # identifier (pode ser var, array, ou subroutine call)
        elif token.type == TokenType.IDENT:
            self.write_token(self.advance())  # identifier
            
            # Lookahead para distinguir o tipo
            next_token = self.peek()
            
            if next_token and next_token.lexeme == '[':
                # Array access: var[expression]
                self.match(TokenType.LBRACKET)         # '['
                self.parse_expression()                # expression
                self.match(TokenType.RBRACKET)         # ']'
                
            elif next_token and next_token.lexeme in ['(', '.']:
                # Subroutine call: var() ou var.method()
                if next_token.lexeme == '.':
                    self.write_token(self.advance())   # '.'
                    self.write_token(self.match(TokenType.IDENT))  # methodName
                self.match(TokenType.LPAREN)           # '('
                self.parse_expression_list()           # expressionList
                self.match(TokenType.RPAREN)           # ')'
            
            # Se não for [ ou ( ou ., é apenas uma variável simples (nada mais a fazer)
        
        # ( expression ) - expressão entre parênteses
        elif token.type == TokenType.LPAREN:
            self.write_token(self.advance())           # '('
            self.parse_expression()                    # expression
            self.match(TokenType.RPAREN)               # ')'
        
        # unaryOp term - operador unário
        elif token.type in [TokenType.MINUS, TokenType.NOT]:
            print ("--------------")
            t = self.advance()
            self.write_token(t)           # '-' ou '~'
            print ("-----", self.get_xml(t))
            self.parse_term()                          # term
        
        else:
            raise SyntaxError(f"Termo esperado, encontrado: {token}")
        
        self.close_tag("term")

    def parse_expression_list(self):
        """
        Compila uma lista de expressões (possivelmente vazia).
        expressionList → (expression (',' expression)*)?
        """
        self.open_tag("expressionList")
        
        # Se não for ')', temos pelo menos uma expressão
        if self.peek() and self.peek().type != TokenType.RPAREN:
            self.parse_expression()
            
            # (',' expression)*
            while self.peek() and self.peek().lexeme == ',':
                self.write_token(self.advance())       # ','
                self.parse_expression()                # expression
        
        self.close_tag("expressionList")

    def parse_subroutine_call(self):
        """
        Compila uma chamada de subrotina.
        subroutineCall → subroutineName '(' expressionList? ')'
                       | (className | varName) '.' subroutineName '(' expressionList? ')'
        """
        # Primeiro identificador (nome da subrotina ou classe/objeto)
        self.write_token(self.advance())               # identifier
        
        # Verifica se é chamada de método (objeto.classe.metodo ou objeto.metodo)
        if self.peek() and self.peek().lexeme == '.':
            self.write_token(self.advance())           # '.'
            self.write_token(self.match(TokenType.IDENT))  # methodName
        
        # Parênteses e lista de expressões
        self.match(TokenType.LPAREN)                   # '('
        self.parse_expression_list()                   # expressionList
        self.match(TokenType.RPAREN)                   # ')'


# ==================================================================
# Função Principal para Execução
# ==================================================================

def parse_file(jack_path: str, output_path: str):
    """
    Função auxiliar para parsear um arquivo .jack e gerar o XML.
    """
    from scanner import Scanner
    
    # 1. Leitura do arquivo Jack
    with open(jack_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # 2. Análise Léxica (Scanner)
    scanner = Scanner(code)
    tokens = scanner.tokenize()
    
    # 3. Análise Sintática (Parser)
    parser = Parser(tokens)
    parser.parse_class()
    
    # 4. Escrita do XML
    xml_content = parser.get_xml()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Parser concluído: {output_path}")
    return xml_content


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 3:
        print("Uso: python parser.py <arquivo.jack> <saida.xml>")
        sys.exit(1)
    
    parse_file(sys.argv[1], sys.argv[2])