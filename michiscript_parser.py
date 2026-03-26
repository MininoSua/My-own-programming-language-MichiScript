"""
MichiScript Parser (Analizador Sintáctico)
Convierte tokens en AST
"""

from typing import List, Optional, Dict
from michiscript_lexer import Token, TokenType, Lexer
from michiscript_ast import *


class Parser:
    """Analizador sintáctico de MichiScript"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, message: str):
        """Lanza un error de sintaxis"""
        token = self.current()
        raise SyntaxError(f"Error de sintaxis en línea {token.line}, columna {token.column}: {message}")
    
    def current(self) -> Token:
        """Retorna el token actual"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek(self, offset: int = 1) -> Token:
        """Mira el siguiente token"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]  # EOF
    
    def advance(self) -> Token:
        """Avanza al siguiente token"""
        token = self.current()
        if token.type != TokenType.EOF:
            self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """Espera un tipo de token específico"""
        if self.current().type != token_type:
            self.error(f"Se esperaba {token_type.name}, se obtuvo {self.current().type.name}")
        return self.advance()
    
    def match(self, *token_types: TokenType) -> bool:
        """Verifica si el token actual coincide con alguno de los tipos"""
        return self.current().type in token_types
    
    def consume(self, token_type: TokenType) -> Token:
        """Consume un token si coincide, sino retorna None"""
        if self.match(token_type):
            return self.advance()
        return None
    
    def parse(self) -> Program:
        """Parsea el programa completo"""
        statements = []
        
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Parsea una sentencia"""
        # Ignorar puntos y comas y newlines
        while self.consume(TokenType.SEMICOLON):
            pass
        
        if self.match(TokenType.EOF):
            return None
        
        # Palabra clave: si
        if self.match(TokenType.SI):
            return self.parse_if_stmt()
        
        # Palabra clave: mientras
        if self.match(TokenType.MIENTRAS):
            return self.parse_while_stmt()
        
        # Palabra clave: para
        if self.match(TokenType.PARA):
            return self.parse_for_stmt()
        
        # Palabra clave: funcion
        if self.match(TokenType.FUNCION):
            return self.parse_func_def()
        
        # Palabra clave: retorna
        if self.match(TokenType.RETORNA):
            return self.parse_return_stmt()
        
        # Palabra clave: rascar (break)
        if self.match(TokenType.RASCAR):
            self.advance()
            return BreakStmt()
        
        # Palabra clave: ronronear (continue)
        if self.match(TokenType.RONRONEAR):
            self.advance()
            return ContinueStmt()
        
        # Palabra clave: traer (print)
        if self.match(TokenType.TRAER):
            return self.parse_print_stmt()
        
        # Palabra clave: pedir (input)
        if self.match(TokenType.PEDIR):
            return self.parse_input_stmt()
        
        # Palabra clave: variable
        if self.match(TokenType.VARIABLE):
            return self.parse_variable_decl()
        
        # Palabra clave: gatito (class)
        if self.match(TokenType.GATITO):
            return self.parse_class_def()
        
        # Palabra clave: olfatear (import)
        if self.match(TokenType.OLFATEAR):
            return self.parse_import_stmt()
        
        # Bloque
        if self.match(TokenType.LBRACE):
            return self.parse_block()
        
        # Expresión o asignación
        return self.parse_expression_stmt()
    
    def parse_block(self) -> Block:
        """Parsea un bloque { ... }"""
        self.expect(TokenType.LBRACE)
        
        statements = []
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        self.expect(TokenType.RBRACE)
        return Block(statements)
    
    def parse_if_stmt(self) -> IfStmt:
        """Parsea sentencia si/sino"""
        self.expect(TokenType.SI)
        
        condition = self.parse_expression()
        then_body = self.parse_block() if self.match(TokenType.LBRACE) else self.parse_statement()
        
        elif_parts = []
        while self.match(TokenType.SINO):
            self.advance()
            
            if self.match(TokenType.SI):
                self.advance()
                elif_condition = self.parse_expression()
                elif_body = self.parse_block() if self.match(TokenType.LBRACE) else self.parse_statement()
                elif_parts.append((elif_condition, elif_body))
            else:
                # else
                else_body = self.parse_block() if self.match(TokenType.LBRACE) else self.parse_statement()
                return IfStmt(condition, then_body, elif_parts, else_body)
        
        return IfStmt(condition, then_body, elif_parts)
    
    def parse_while_stmt(self) -> WhileStmt:
        """Parsea bucle mientras"""
        self.expect(TokenType.MIENTRAS)
        
        condition = self.parse_expression()
        body = self.parse_block() if self.match(TokenType.LBRACE) else self.parse_statement()
        
        return WhileStmt(condition, body)
    
    def parse_for_stmt(self) -> ForStmt:
        """Parsea bucle para"""
        self.expect(TokenType.PARA)
        
        variable = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.EN)
        
        iterable = self.parse_expression()
        body = self.parse_block() if self.match(TokenType.LBRACE) else self.parse_statement()
        
        return ForStmt(variable, iterable, body)
    
    def parse_func_def(self) -> FuncDef:
        """Parsea definición de función"""
        self.expect(TokenType.FUNCION)
        
        name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        parameters = []
        defaults = {}
        
        while not self.match(TokenType.RPAREN):
            param_name = self.expect(TokenType.IDENTIFIER).value
            parameters.append(param_name)
            
            # Parámetro con valor por defecto
            if self.match(TokenType.ASSIGN):
                self.advance()
                defaults[param_name] = self.parse_primary()
            
            if not self.match(TokenType.RPAREN):
                self.expect(TokenType.COMMA)
        
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        
        return FuncDef(name, parameters, body, defaults)
    
    def parse_return_stmt(self) -> ReturnStmt:
        """Parsea sentencia retorna"""
        self.expect(TokenType.RETORNA)
        
        if self.match(TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
            return ReturnStmt(None)
        
        value = self.parse_expression()
        return ReturnStmt(value)
    
    def parse_print_stmt(self) -> PrintStmt:
        """Parsea sentencia traer (print)"""
        self.expect(TokenType.TRAER)
        
        expressions = []
        
        if not self.match(TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
            expressions.append(self.parse_expression())
            
            while self.match(TokenType.COMMA):
                self.advance()
                expressions.append(self.parse_expression())
        
        return PrintStmt(expressions)
    
    def parse_input_stmt(self) -> InputStmt:
        """Parsea sentencia pedir (input)"""
        self.expect(TokenType.PEDIR)
        
        prompt = None
        if not self.match(TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
            prompt = self.parse_expression()
        
        return InputStmt(prompt)
    
    def parse_variable_decl(self) -> VariableDecl:
        """Parsea declaración de variable"""
        self.expect(TokenType.VARIABLE)
        
        name = self.expect(TokenType.IDENTIFIER).value
        
        value = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.parse_expression()
        
        return VariableDecl(name, value)
    
    def parse_class_def(self) -> ClassDef:
        """Parsea definición de clase"""
        self.expect(TokenType.GATITO)
        
        name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LBRACE)
        
        methods = []
        while not self.match(TokenType.RBRACE):
            if self.match(TokenType.FUNCION):
                method = self.parse_func_def()
                methods.append(method)
            else:
                self.advance()
        
        self.expect(TokenType.RBRACE)
        
        return ClassDef(name, methods)
    
    def parse_import_stmt(self) -> ImportStmt:
        """Parsea sentencia olfatear (import)"""
        self.expect(TokenType.OLFATEAR)
        
        module = self.expect(TokenType.IDENTIFIER).value
        
        alias = None
        if self.match(TokenType.IDENTIFIER):
            if self.current().value == 'como':
                self.advance()
                alias = self.expect(TokenType.IDENTIFIER).value
        
        return ImportStmt(module, alias)
    
    def parse_expression_stmt(self) -> ASTNode:
        """Parsea una expresión como sentencia"""
        expr = self.parse_expression()
        
        # Ignorar punto y coma opcional
        self.consume(TokenType.SEMICOLON)
        
        return ExprStmt(expr)
    
    def parse_expression(self) -> ASTNode:
        """Parsea una expresión"""
        return self.parse_assignment()
    
    def parse_assignment(self) -> ASTNode:
        """Parsea asignación"""
        expr = self.parse_ternary()
        
        # Asignación múltiple (a, b = 1, 2)
        if isinstance(expr, Identifier) and self.match(TokenType.COMMA):
            targets = [expr.name]
            
            while self.match(TokenType.COMMA):
                self.advance()
                if self.match(TokenType.IDENTIFIER):
                    targets.append(self.advance().value)
            
            if self.match(TokenType.ASSIGN):
                self.advance()
                values = [self.parse_ternary()]
                
                while self.match(TokenType.COMMA):
                    self.advance()
                    values.append(self.parse_ternary())
                
                return MultiAssignment(targets, values)
        
        # Asignación simple
        if self.match(TokenType.ASSIGN):
            if not isinstance(expr, (Identifier, IndexExpr, MemberExpr)):
                self.error("Destino de asignación inválido")
            
            self.advance()
            value = self.parse_expression()
            
            if isinstance(expr, Identifier):
                return Assignment(expr.name, value)
            elif isinstance(expr, IndexExpr):
                return ExprStmt(BinaryOp(expr, '=', value))
            elif isinstance(expr, MemberExpr):
                return ExprStmt(BinaryOp(expr, '=', value))
        
        # Asignación compuesta (+=, -=, etc)
        elif self.match(TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
                       TokenType.MUL_ASSIGN, TokenType.DIV_ASSIGN):
            if not isinstance(expr, Identifier):
                self.error("Destino de asignación inválido")
            
            op_token = self.advance()
            value = self.parse_expression()
            
            op_map = {
                TokenType.PLUS_ASSIGN: '+',
                TokenType.MINUS_ASSIGN: '-',
                TokenType.MUL_ASSIGN: '*',
                TokenType.DIV_ASSIGN: '/',
            }
            
            return CompoundAssignment(expr.name, op_map[op_token.type], value)
        
        return expr
    
    def parse_ternary(self) -> ASTNode:
        """Parsea expresión ternaria"""
        expr = self.parse_or()
        
        if self.match(TokenType.SI):
            self.advance()
            true_expr = self.parse_or()
            self.expect(TokenType.SINO)
            false_expr = self.parse_ternary()
            
            return TernaryExpr(expr, true_expr, false_expr)
        
        return expr
    
    def parse_or(self) -> ASTNode:
        """Parsea OR lógico"""
        left = self.parse_and()
        
        while self.match(TokenType.OR):
            op = self.advance().value
            right = self.parse_and()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_and(self) -> ASTNode:
        """Parsea AND lógico"""
        left = self.parse_not()
        
        while self.match(TokenType.AND):
            op = self.advance().value
            right = self.parse_not()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_not(self) -> ASTNode:
        """Parsea NOT lógico"""
        if self.match(TokenType.NOT):
            op = self.advance().value
            operand = self.parse_not()
            return UnaryOp(op, operand)
        
        return self.parse_comparison()
    
    def parse_comparison(self) -> ASTNode:
        """Parsea comparaciones"""
        left = self.parse_additive()
        
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL,
                         TokenType.LESS, TokenType.GREATER,
                         TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parsea suma y resta"""
        left = self.parse_multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parsea multiplicación, división y módulo"""
        left = self.parse_power()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            right = self.parse_power()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_power(self) -> ASTNode:
        """Parsea potencia"""
        left = self.parse_unary()
        
        if self.match(TokenType.POWER):
            op = self.advance().value
            right = self.parse_power()  # Asociatividad a la derecha
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parsea operaciones unarias"""
        if self.match(TokenType.MINUS, TokenType.NOT):
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        """Parsea operaciones postfijas (llamadas, índices, miembros)"""
        expr = self.parse_primary()
        
        while True:
            if self.match(TokenType.LPAREN):
                # Llamada a función
                self.advance()
                arguments = []
                
                while not self.match(TokenType.RPAREN):
                    arguments.append(self.parse_expression())
                    if not self.match(TokenType.RPAREN):
                        self.expect(TokenType.COMMA)
                
                self.expect(TokenType.RPAREN)
                expr = CallExpr(expr, arguments)
            
            elif self.match(TokenType.LBRACKET):
                # Índice o slice
                self.advance()
                
                start = None
                end = None
                
                if not self.match(TokenType.COLON):
                    start = self.parse_expression()
                
                if self.match(TokenType.COLON):
                    self.advance()
                    if not self.match(TokenType.RBRACKET):
                        end = self.parse_expression()
                    
                    self.expect(TokenType.RBRACKET)
                    expr = SliceExpr(expr, start, end)
                else:
                    self.expect(TokenType.RBRACKET)
                    expr = IndexExpr(expr, start)
            
            elif self.match(TokenType.DOT):
                # Acceso a miembro
                self.advance()
                member = self.expect(TokenType.IDENTIFIER).value
                expr = MemberExpr(expr, member)
            
            else:
                break
        
        return expr
    
    def parse_primary(self) -> ASTNode:
        """Parsea expresiones primarias"""
        # Números
        if self.match(TokenType.NUMBER):
            value = self.advance().value
            return Literal(value)
        
        # Strings
        if self.match(TokenType.STRING):
            value = self.advance().value
            return Literal(value)
        
        # Booleanos
        if self.match(TokenType.VERDADERO, TokenType.FALSO):
            value = self.advance().value
            return Literal(value)
        
        # Null
        if self.match(TokenType.NULO):
            self.advance()
            return Literal(None)
        
        # Identificadores
        if self.match(TokenType.IDENTIFIER):
            name = self.advance().value
            return Identifier(name)
        
        # Listas
        if self.match(TokenType.LBRACKET):
            return self.parse_list_expr()
        
        # Diccionarios
        if self.match(TokenType.LBRACE):
            # Diferenciar entre bloque y diccionario
            saved_pos = self.pos
            self.advance()
            
            # Intenta parsear como diccionario
            is_dict = False
            if self.match(TokenType.IDENTIFIER) and self.peek(0).type == TokenType.COLON:
                is_dict = True
            
            self.pos = saved_pos
            
            if is_dict:
                return self.parse_dict_expr()
        
        # Expresiones entre paréntesis
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        # Función anónima
        if self.match(TokenType.FUNCION):
            return self.parse_lambda_expr()
        
        self.error(f"Expresión primaria inesperada: {self.current().value}")
    
    def parse_list_expr(self) -> ListExpr:
        """Parsea lista"""
        self.expect(TokenType.LBRACKET)
        
        elements = []
        
        while not self.match(TokenType.RBRACKET):
            elements.append(self.parse_expression())
            
            if not self.match(TokenType.RBRACKET):
                self.expect(TokenType.COMMA)
        
        self.expect(TokenType.RBRACKET)
        
        return ListExpr(elements)
    
    def parse_dict_expr(self) -> DictExpr:
        """Parsea diccionario"""
        self.expect(TokenType.LBRACE)
        
        pairs = []
        
        while not self.match(TokenType.RBRACE):
            key = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.COLON)
            value = self.parse_expression()
            
            pairs.append((key, value))
            
            if not self.match(TokenType.RBRACE):
                self.expect(TokenType.COMMA)
        
        self.expect(TokenType.RBRACE)
        
        return DictExpr(pairs)
    
    def parse_lambda_expr(self) -> LambdaExpr:
        """Parsea función anónima"""
        self.expect(TokenType.FUNCION)
        
        self.expect(TokenType.LPAREN)
        
        parameters = []
        defaults = {}
        
        while not self.match(TokenType.RPAREN):
            param_name = self.expect(TokenType.IDENTIFIER).value
            parameters.append(param_name)
            
            if self.match(TokenType.ASSIGN):
                self.advance()
                defaults[param_name] = self.parse_primary()
            
            if not self.match(TokenType.RPAREN):
                self.expect(TokenType.COMMA)
        
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        
        return LambdaExpr(parameters, body, defaults)


def parse(source: str) -> Program:
    """Función conveniente para lexear y parsear"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
