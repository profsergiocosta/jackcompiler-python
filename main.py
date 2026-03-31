from jacktoken import Token, TokenType

t = Token(TokenType.NUMBER, "42", 0)

print (t)
print (t.to_xml())

t = Token(TokenType.STRING, "ola mundo", 0)
print (t.to_xml())


t = Token(TokenType.PLUS, "+", 0)
print (t.to_xml())