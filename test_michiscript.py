"""
Pruebas unitarias para MichiScript
"""

import sys
import unittest
from io import StringIO
from michiscript_lexer import Lexer, TokenType
from michiscript_parser import parse
from michiscript_evaluator import Evaluator


class TestLexer(unittest.TestCase):
    """Pruebas del lexer"""
    
    def test_numbers(self):
        lexer = Lexer("42 3.14 0")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].value, 3.14)
    
    def test_strings(self):
        lexer = Lexer('"hola" \'mundo\'')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "hola")
        self.assertEqual(tokens[1].type, TokenType.STRING)
        self.assertEqual(tokens[1].value, "mundo")
    
    def test_keywords(self):
        lexer = Lexer("si sino mientras para funcion retorna")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.SI)
        self.assertEqual(tokens[1].type, TokenType.SINO)
        self.assertEqual(tokens[2].type, TokenType.MIENTRAS)
        self.assertEqual(tokens[3].type, TokenType.PARA)
        self.assertEqual(tokens[4].type, TokenType.FUNCION)
        self.assertEqual(tokens[5].type, TokenType.RETORNA)
    
    def test_operators(self):
        lexer = Lexer("+ - * / % ^ == != < > <= >=")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.PLUS)
        self.assertEqual(tokens[1].type, TokenType.MINUS)
        self.assertEqual(tokens[2].type, TokenType.MULTIPLY)
        self.assertEqual(tokens[3].type, TokenType.DIVIDE)


class TestParser(unittest.TestCase):
    """Pruebas del parser"""
    
    def test_parse_literals(self):
        ast = parse("42")
        self.assertIsNotNone(ast)
    
    def test_parse_binary_op(self):
        ast = parse("5 + 3")
        self.assertIsNotNone(ast)
    
    def test_parse_variable_assignment(self):
        ast = parse("x = 10")
        self.assertIsNotNone(ast)
    
    def test_parse_function_def(self):
        ast = parse("""
funcion sumar(a, b) {
    retorna a + b
}
        """)
        self.assertIsNotNone(ast)
    
    def test_parse_if_statement(self):
        ast = parse("""
si x > 5 {
    traer "Mayor que 5"
} sino {
    traer "Menor o igual a 5"
}
        """)
        self.assertIsNotNone(ast)
    
    def test_parse_while_loop(self):
        ast = parse("""
mientras x < 10 {
    x = x + 1
}
        """)
        self.assertIsNotNone(ast)
    
    def test_parse_for_loop(self):
        ast = parse("""
para i en rango(5) {
    traer i
}
        """)
        self.assertIsNotNone(ast)
    
    def test_parse_list(self):
        ast = parse("[1, 2, 3, 4, 5]")
        self.assertIsNotNone(ast)
    
    def test_parse_dict(self):
        ast = parse("{nombre: 'Michi', edad: 5}")
        self.assertIsNotNone(ast)


class TestEvaluator(unittest.TestCase):
    """Pruebas del evaluador"""
    
    def setUp(self):
        self.evaluator = Evaluator()
        self.original_stdout = sys.stdout
    
    def tearDown(self):
        sys.stdout = self.original_stdout
    
    def execute(self, source: str):
        """Ejecuta código y captura la salida"""
        sys.stdout = StringIO()
        try:
            ast = parse(source)
            self.evaluator.evaluate(ast)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = self.original_stdout
        return output
    
    def test_arithmetic(self):
        ast = parse("5 + 3 * 2")
        result = self.evaluator.evaluate(ast)
        # 5 + (3 * 2) = 11
    
    def test_assignment(self):
        ast = parse("""
x = 10
y = x + 5
        """)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('x'), 10)
        self.assertEqual(self.evaluator.current_env.get('y'), 15)
    
    def test_function_definition(self):
        source = """
funcion sumar(a, b) {
    retorna a + b
}
resultado = sumar(3, 4)
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('resultado'), 7)
    
    def test_print(self):
        output = self.execute('traer "Hola Michis"')
        self.assertEqual(output.strip(), "Hola Michis")
    
    def test_if_statement(self):
        source = """
x = 10
si x > 5 {
    resultado = "Mayor"
} sino {
    resultado = "Menor"
}
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('resultado'), "Mayor")
    
    def test_while_loop(self):
        source = """
x = 0
mientras x < 5 {
    x = x + 1
}
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('x'), 5)
    
    def test_for_loop(self):
        source = """
suma = 0
para i en rango(5) {
    suma = suma + i
}
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('suma'), 10)
    
    def test_list_operations(self):
        source = """
numeros = [1, 2, 3, 4, 5]
primer = numeros[0]
ultimo = numeros[-1]
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('primer'), 1)
        self.assertEqual(self.evaluator.current_env.get('ultimo'), 5)
    
    def test_dict_operations(self):
        source = """
gato = {nombre: "Michi", edad: 5}
nombre = gato["nombre"]
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('nombre'), "Michi")
    
    def test_builtin_functions(self):
        source = """
x = abs(-10)
y = max(3, 7)
z = min(3, 7)
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('x'), 10)
        self.assertEqual(self.evaluator.current_env.get('y'), 7)
        self.assertEqual(self.evaluator.current_env.get('z'), 3)
    
    def test_string_operations(self):
        source = """
x = "hola"
y = x + " mundo"
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('y'), "hola mundo")
    
    def test_type_conversion(self):
        source = """
x = numero("42")
y = texto(42)
z = booleano(1)
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('x'), 42)
        self.assertEqual(self.evaluator.current_env.get('y'), "42")
        self.assertEqual(self.evaluator.current_env.get('z'), True)
    
    def test_lambda(self):
        source = """
cuadrado = funcion(x) {
    retorna x * x
}
resultado = cuadrado(5)
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('resultado'), 25)
    
    def test_recursion(self):
        source = """
funcion factorial(n) {
    si n <= 1 {
        retorna 1
    } sino {
        retorna n * factorial(n - 1)
    }
}
resultado = factorial(5)
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('resultado'), 120)
    
    def test_multiple_assignment(self):
        source = """
a, b, c = 1, 2, 3
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('a'), 1)
        self.assertEqual(self.evaluator.current_env.get('b'), 2)
        self.assertEqual(self.evaluator.current_env.get('c'), 3)
    
    def test_compound_assignment(self):
        source = """
x = 10
x += 5
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('x'), 15)
    
    def test_break_continue(self):
        source = """
suma = 0
para i en rango(10) {
    si i == 5 {
        rascar
    }
    suma = suma + i
}
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('suma'), 10)


class TestIntegration(unittest.TestCase):
    """Pruebas de integración"""
    
    def setUp(self):
        self.evaluator = Evaluator()
        self.original_stdout = sys.stdout
    
    def tearDown(self):
        sys.stdout = self.original_stdout
    
    def execute(self, source: str):
        """Ejecuta código"""
        sys.stdout = StringIO()
        try:
            ast = parse(source)
            self.evaluator.evaluate(ast)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = self.original_stdout
        return output
    
    def test_fibonacci(self):
        source = """
funcion fib(n) {
    si n <= 1 {
        retorna n
    }
    retorna fib(n - 1) + fib(n - 2)
}
resultado = fib(10)
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('resultado'), 55)
    
    def test_list_processing(self):
        source = """
numeros = [1, 2, 3, 4, 5]
suma = 0
para n en numeros {
    suma = suma + n
}
promedio = suma / longitud(numeros)
        """
        ast = parse(source)
        self.evaluator.evaluate(ast)
        self.assertEqual(self.evaluator.current_env.get('suma'), 15)
        self.assertEqual(self.evaluator.current_env.get('promedio'), 3.0)


if __name__ == '__main__':
    unittest.main()
