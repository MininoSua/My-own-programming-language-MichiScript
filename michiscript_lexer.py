"""
MichiScript Lexer (Analizador Léxico)
Convierte el código fuente en tokens
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    """Tipos de tokens"""
    # Literales
    NUMBER = auto()
    STRING = auto()
    BOOL = auto()
    NULL = auto()
    
    # Identificadores y palabras clave
    IDENTIFIER = auto()
    
    # Palabras clave
    SI = auto()          # if
    SINO = auto()        # else
    MIENTRAS = auto()    # while
    PARA = auto()        # for
    EN = auto()          # in
    FUNCION = auto()     # function
    RETORNA = auto()     # return
    VARIABLE = auto()    # variable declaration
    MIAU = auto()        # comment
    TRAER = auto()       # print
    PEDIR = auto()       # input
    RASCAR = auto()      # break
    RONRONEAR = auto()   # continue
    GATITO = auto()      # class
    OLFATEAR = auto()    # import
    VERDADERO = auto()   # true
    FALSO = auto()        # false
    NULO = auto()        # null
    
    # Operadores
    PLUS = auto()        # +
    MINUS = auto()       # -
    MULTIPLY = auto()    # *
    DIVIDE = auto()      # /
    MODULO = auto()      # %
    POWER = auto()       # ^
    
    # Comparación
    EQUAL = auto()       # ==
    NOT_EQUAL = auto()   # !=
    LESS = auto()        # <
    GREATER = auto()     # >
    LESS_EQUAL = auto()  # <=
    GREATER_EQUAL = auto() # >=
    
    # Lógicos
    AND = auto()         # &&
    OR = auto()          # ||
    NOT = auto()         # !
    
    # Asignación
    ASSIGN = auto()      # =
    PLUS_ASSIGN = auto() # +=
    MINUS_ASSIGN = auto() # -=
    MUL_ASSIGN = auto()  # *=
    DIV_ASSIGN = auto()  # /=
    
    # Delimitadores
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    COMMA = auto()       # ,
    COLON = auto()       # :
    SEMICOLON = auto()   # ;
    DOT = auto()         # .
    ARROW = auto()       # ->
    
    # Especiales
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    """Representa un token"""
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}, {self.column})"


class Lexer:
    """Analizador léxico de MichiScript"""
    
    KEYWORDS = {
        'si': TokenType.SI,
        'sino': TokenType.SINO,
        'mientras': TokenType.MIENTRAS,
        'para': TokenType.PARA,
        'en': TokenType.EN,
        'funcion': TokenType.FUNCION,
        'retorna': TokenType.RETORNA,
        'variable': TokenType.VARIABLE,
        'traer': TokenType.TRAER,
        'pedir': TokenType.PEDIR,
        'rascar': TokenType.RASCAR,
        'ronronear': TokenType.RONRONEAR,
        'gatito': TokenType.GATITO,
        'olfatear': TokenType.OLFATEAR,
        'verdadero': TokenType.VERDADERO,
        'falso': TokenType.FALSO,
        'nulo': TokenType.NULO,
        'miau': TokenType.MIAU,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, message: str):
        """Lanza un error léxico"""
        raise SyntaxError(f"Error léxico en línea {self.line}, columna {self.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Mira el carácter actual sin avanzar"""
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        """Avanza a la siguiente posición y retorna el carácter actual"""
        if self.pos >= len(self.source):
            return None
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def skip_whitespace(self):
        """Salta espacios en blanco (excepto newlines)"""
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Salta comentarios que comienzan con 'miau'"""
        if self.peek() == 'm' and self.peek(1) == 'i' and self.peek(2) == 'a' and self.peek(3) == 'u':
            # Verificar que sea palabra completa
            if self.peek(4) in (None, ' ', '\t', '\n'):
                while self.peek() and self.peek() != '\n':
                    self.advance()
                return True
        return False
    
    def read_string(self, quote_char: str) -> str:
        """Lee una cadena de caracteres"""
        value = ""
        self.advance()  # Skip la comilla inicial
        
        while self.peek() and self.peek() != quote_char:
            if self.peek() == '\\':
                self.advance()
                next_char = self.advance()
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == 'r':
                    value += '\r'
                elif next_char == '\\':
                    value += '\\'
                elif next_char == quote_char:
                    value += quote_char
                else:
                    value += next_char
            else:
                value += self.advance()
        
        if not self.peek():
            self.error(f"Cadena sin cerrar")
        
        self.advance()  # Skip la comilla final
        return value
    
    def read_number(self) -> float:
        """Lee un número entero o flotante"""
        num_str = ""
        has_dot = False
        
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            if self.peek() == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += self.advance()
        
        return float(num_str) if has_dot else int(num_str)
    
    def read_identifier(self) -> str:
        """Lee un identificador o palabra clave"""
        ident = ""
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        return ident
    
    def tokenize(self) -> List[Token]:
        """Tokeniza el código fuente"""
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Saltar comentarios
            if self.skip_comment():
                continue
            
            line = self.line
            col = self.column
            char = self.peek()
            
            # Newline
            if char == '\n':
                self.advance()
                # Ignorar newlines múltiples
                while self.peek() == '\n':
                    self.advance()
                continue
            
            # Cadenas
            if char in ('"', "'"):
                value = self.read_string(char)
                self.tokens.append(Token(TokenType.STRING, value, line, col))
                continue
            
            # Números
            if char.isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, line, col))
                continue
            
            # Identificadores y palabras clave
            if char.isalpha() or char == '_':
                ident = self.read_identifier()
                token_type = self.KEYWORDS.get(ident, TokenType.IDENTIFIER)
                
                # Valores especiales
                if token_type == TokenType.VERDADERO:
                    self.tokens.append(Token(token_type, True, line, col))
                elif token_type == TokenType.FALSO:
                    self.tokens.append(Token(token_type, False, line, col))
                elif token_type == TokenType.NULO:
                    self.tokens.append(Token(token_type, None, line, col))
                else:
                    value = True if token_type == TokenType.VERDADERO else (False if token_type == TokenType.FALSO else ident)
                    self.tokens.append(Token(token_type, value, line, col))
                continue
            
            # Operadores y delimitadores
            self.advance()
            
            # Operadores de dos caracteres
            if char == '=' and self.peek() == '=':
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, '==', line, col))
            elif char == '!' and self.peek() == '=':
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', line, col))
            elif char == '<' and self.peek() == '=':
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', line, col))
            elif char == '>' and self.peek() == '=':
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', line, col))
            elif char == '&' and self.peek() == '&':
                self.advance()
                self.tokens.append(Token(TokenType.AND, '&&', line, col))
            elif char == '|' and self.peek() == '|':
                self.advance()
                self.tokens.append(Token(TokenType.OR, '||', line, col))
            elif char == '+' and self.peek() == '=':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS_ASSIGN, '+=', line, col))
            elif char == '-' and self.peek() == '=':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS_ASSIGN, '-=', line, col))
            elif char == '*' and self.peek() == '=':
                self.advance()
                self.tokens.append(Token(TokenType.MUL_ASSIGN, '*=', line, col))
            elif char == '/' and self.peek() == '=':
                self.advance()
                self.tokens.append(Token(TokenType.DIV_ASSIGN, '/=', line, col))
            elif char == '-' and self.peek() == '>':
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, '->', line, col))
            
            # Operadores de un carácter
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', line, col))
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', line, col))
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', line, col))
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', line, col))
            elif char == '%':
                self.tokens.append(Token(TokenType.MODULO, '%', line, col))
            elif char == '^':
                self.tokens.append(Token(TokenType.POWER, '^', line, col))
            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', line, col))
            elif char == '<':
                self.tokens.append(Token(TokenType.LESS, '<', line, col))
            elif char == '>':
                self.tokens.append(Token(TokenType.GREATER, '>', line, col))
            elif char == '!':
                self.tokens.append(Token(TokenType.NOT, '!', line, col))
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', line, col))
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', line, col))
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', line, col))
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', line, col))
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '[', line, col))
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']', line, col))
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', line, col))
            elif char == ':':
                self.tokens.append(Token(TokenType.COLON, ':', line, col))
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', line, col))
            elif char == '.':
                self.tokens.append(Token(TokenType.DOT, '.', line, col))
            else:
                self.error(f"Carácter no reconocido: {char}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
