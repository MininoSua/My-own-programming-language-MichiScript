#!/usr/bin/env python3
"""
MichiScript - Intérprete CLI
Ejecuta archivos .michis o modo interactivo REPL
"""

import sys
import os
from pathlib import Path
from michiscript_lexer import Lexer
from michiscript_parser import Parser
from michiscript_evaluator import Evaluator


class MichiScriptREPL:
    """REPL (Read-Eval-Print-Loop) para MichiScript"""
    
    def __init__(self):
        self.evaluator = Evaluator()
        self.version = "1.0.0"
    
    def print_banner(self):
        """Imprime el banner de bienvenida"""
        print("""
╔══════════════════════════════════════════╗
║       MichiScript v1.0.0 - REPL          ║
║     Bienvenido al mundo de los michis 🐱 ║
╚══════════════════════════════════════════╝

Escribe 'ayuda' para ver los comandos disponibles.
Escribe 'salir' para terminar.
        """)
    
    def print_help(self):
        """Imprime la ayuda"""
        help_text = """
Comandos disponibles:
  ayuda          - Muestra esta ayuda
  salir/exit     - Termina el programa
  limpiar        - Limpia la pantalla
  variables      - Muestra variables definidas
  funciones      - Muestra funciones definidas
  
Ejemplos:
  traer "¡Hola Michis!"
  x = 5 + 3
  si x > 5 { traer "Es mayor" }
  
Para más información, visita: https://github.com/michiscript/
        """
        print(help_text)
    
    def execute_line(self, line: str) -> bool:
        """Ejecuta una línea de código"""
        line = line.strip()
        
        if not line:
            return True
        
        # Comandos especiales
        if line == 'ayuda':
            self.print_help()
            return True
        elif line == 'salir' or line == 'exit':
            print("¡Adiós! 🐱")
            return False
        elif line == 'limpiar':
            os.system('clear' if os.name == 'posix' else 'cls')
            return True
        elif line == 'variables':
            self._print_variables()
            return True
        elif line == 'funciones':
            self._print_functions()
            return True
        
        # Ejecutar código
        try:
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            self.evaluator.evaluate(ast)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return True
    
    def _print_variables(self):
        """Imprime las variables definidas"""
        print("\nVariables definidas:")
        for name, value in self.evaluator.current_env.variables.items():
            if not name.startswith('_'):
                print(f"  {name} = {self.evaluator._builtin_texto(value)}")
        print()
    
    def _print_functions(self):
        """Imprime las funciones definidas"""
        print("\nFunciones definidas:")
        for name, value in self.evaluator.current_env.variables.items():
            if hasattr(value, '__call__') and not name.startswith('_'):
                print(f"  {name}()")
        print()
    
    def run_repl(self):
        """Inicia el REPL"""
        self.print_banner()
        
        while True:
            try:
                line = input("michis> ")
                if not self.execute_line(line):
                    break
            except KeyboardInterrupt:
                print("\n\n¡Adiós! 🐱")
                break
            except EOFError:
                print("\n\n¡Adiós! 🐱")
                break
    
    def run_file(self, filename: str):
        """Ejecuta un archivo .michis"""
        try:
            path = Path(filename)
            
            if not path.exists():
                print(f"Error: El archivo '{filename}' no existe")
                sys.exit(1)
            
            with open(path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            self.evaluator.evaluate(ast)
        
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


def main():
    """Función principal"""
    if len(sys.argv) > 1:
        # Ejecutar archivo
        filename = sys.argv[1]
        repl = MichiScriptREPL()
        repl.run_file(filename)
    else:
        # REPL interactivo
        repl = MichiScriptREPL()
        repl.run_repl()


if __name__ == '__main__':
    main()
