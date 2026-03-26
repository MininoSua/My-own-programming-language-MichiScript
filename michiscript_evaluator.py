"""
MichiScript Evaluator (Intérprete)
Ejecuta el AST
"""

import sys
import math
import random
from typing import Any, Dict, List, Optional
from michiscript_ast import *


class ReturnException(Exception):
    """Excepción para manejar returns"""
    def __init__(self, value):
        self.value = value


class BreakException(Exception):
    """Excepción para manejar breaks"""
    pass


class ContinueException(Exception):
    """Excepción para manejar continues"""
    pass


class MichiFunction:
    """Representa una función definida por el usuario"""
    
    def __init__(self, name: str, parameters: List[str], body: ASTNode, closure: 'Environment', defaults: Dict):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure = closure
        self.defaults = defaults
    
    def __repr__(self):
        return f"<funcion {self.name}>"


class MichiClass:
    """Representa una clase definida por el usuario"""
    
    def __init__(self, name: str, methods: Dict[str, MichiFunction]):
        self.name = name
        self.methods = methods
    
    def __repr__(self):
        return f"<clase {self.name}>"


class MichiInstance:
    """Representa una instancia de clase"""
    
    def __init__(self, klass: MichiClass):
        self.klass = klass
        self.attributes = {}
    
    def __repr__(self):
        return f"<instancia de {self.klass.name}>"


class Environment:
    """Entorno de variables"""
    
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.variables: Dict[str, Any] = {}
    
    def define(self, name: str, value: Any):
        """Define una variable en el entorno actual"""
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        """Obtiene una variable (busca en el entorno y en los padres)"""
        if name in self.variables:
            return self.variables[name]
        
        if self.parent:
            return self.parent.get(name)
        
        raise NameError(f"Gato no definido: {name}")
    
    def set(self, name: str, value: Any):
        """Asigna a una variable (busca en el entorno y en los padres)"""
        if name in self.variables:
            self.variables[name] = value
            return
        
        if self.parent:
            self.parent.set(name, value)
            return
        
        # Si no existe, crear en el entorno actual
        self.variables[name] = value
    
    def set_local(self, name: str, value: Any):
        """Asigna a una variable en el entorno local"""
        self.variables[name] = value


class Evaluator:
    """Evaluador/Intérprete de MichiScript"""
    
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
        self._setup_builtins()
    
    def _setup_builtins(self):
        """Configura funciones integradas"""
        # Funciones de conversión
        self.global_env.define('numero', self._builtin_numero)
        self.global_env.define('texto', self._builtin_texto)
        self.global_env.define('booleano', self._builtin_booleano)
        self.global_env.define('lista', self._builtin_lista)
        
        # Funciones matemáticas
        self.global_env.define('abs', lambda x: abs(x))
        self.global_env.define('max', lambda *args: max(args))
        self.global_env.define('min', lambda *args: min(args))
        self.global_env.define('redondear', lambda x, decimales=0: round(x, decimales))
        self.global_env.define('piso', math.floor)
        self.global_env.define('techo', math.ceil)
        self.global_env.define('potencia', lambda x, y: x ** y)
        self.global_env.define('raiz_cuadrada', math.sqrt)
        self.global_env.define('raiz', math.sqrt)
        
        # Funciones de secuencias
        self.global_env.define('longitud', self._builtin_longitud)
        self.global_env.define('rango', self._builtin_rango)
        self.global_env.define('suma', lambda seq: sum(seq))
        self.global_env.define('promedio', self._builtin_promedio)
        self.global_env.define('contar', self._builtin_contar)
        
        # Funciones de tipo
        self.global_env.define('tipo', self._builtin_tipo)
        self.global_env.define('es_numero', lambda x: isinstance(x, (int, float)) and not isinstance(x, bool))
        self.global_env.define('es_texto', lambda x: isinstance(x, str))
        self.global_env.define('es_lista', lambda x: isinstance(x, list))
        self.global_env.define('es_diccionario', lambda x: isinstance(x, dict))
        self.global_env.define('es_booleano', lambda x: isinstance(x, bool))
        self.global_env.define('es_nulo', lambda x: x is None)
        
        # Funciones especiales
        self.global_env.define('aleatorio', random.random)
        self.global_env.define('aleatorio_entero', random.randint)
        self.global_env.define('aleatorio_elemento', random.choice)
        self.global_env.define('espera', __import__('time').sleep)
        
        # E/S
        self.global_env.define('pedir_si_no', self._builtin_pedir_si_no)
        self.global_env.define('pedir_numero', self._builtin_pedir_numero)
        self.global_env.define('formatear', self._builtin_formatear)
        self.global_env.define('ejecutar_linea', self._builtin_ejecutar_linea)
    
    # Funciones integradas
    
    def _builtin_numero(self, value):
        """Convierte a número"""
        if isinstance(value, bool):
            return 1 if value else 0
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    raise TypeError(f"No se puede convertir '{value}' a número")
        if isinstance(value, (int, float)):
            return value
        raise TypeError(f"No se puede convertir {type(value).__name__} a número")
    
    def _builtin_texto(self, value):
        """Convierte a texto"""
        if value is None:
            return "nulo"
        if isinstance(value, bool):
            return "verdadero" if value else "falso"
        if isinstance(value, list):
            return "[" + ", ".join(self._builtin_texto(x) for x in value) + "]"
        if isinstance(value, dict):
            items = [f"{k}: {self._builtin_texto(v)}" for k, v in value.items()]
            return "{" + ", ".join(items) + "}"
        return str(value)
    
    def _builtin_booleano(self, value):
        """Convierte a booleano"""
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, (list, dict)):
            return len(value) > 0
        return True
    
    def _builtin_lista(self, value):
        """Convierte a lista"""
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return list(value)
        if isinstance(value, dict):
            return list(value.items())
        raise TypeError(f"No se puede convertir {type(value).__name__} a lista")
    
    def _builtin_longitud(self, value):
        """Obtiene la longitud"""
        if hasattr(value, '__len__'):
            return len(value)
        raise TypeError(f"No se puede obtener longitud de {type(value).__name__}")
    
    def _builtin_rango(self, *args):
        """Crea un rango"""
        if len(args) == 1:
            return list(range(int(args[0])))
        elif len(args) == 2:
            return list(range(int(args[0]), int(args[1])))
        elif len(args) == 3:
            return list(range(int(args[0]), int(args[1]), int(args[2])))
        raise TypeError("rango() requiere 1 a 3 argumentos")
    
    def _builtin_promedio(self, seq):
        """Calcula el promedio"""
        if not seq:
            return 0
        return sum(seq) / len(seq)
    
    def _builtin_contar(self, seq, value):
        """Cuenta ocurrencias"""
        if isinstance(seq, str):
            return seq.count(value)
        return sum(1 for x in seq if x == value)
    
    def _builtin_tipo(self, value):
        """Obtiene el tipo de un valor"""
        if value is None:
            return "nulo"
        if isinstance(value, bool):
            return "booleano"
        if isinstance(value, int):
            return "numero"
        if isinstance(value, float):
            return "numero"
        if isinstance(value, str):
            return "texto"
        if isinstance(value, list):
            return "lista"
        if isinstance(value, dict):
            return "diccionario"
        if isinstance(value, MichiFunction):
            return "funcion"
        if isinstance(value, MichiClass):
            return "clase"
        if isinstance(value, MichiInstance):
            return "instancia"
        return "desconocido"
    
    def _builtin_pedir_si_no(self, prompt):
        """Lee una respuesta sí/no"""
        while True:
            response = input(self._builtin_texto(prompt) + " ").lower()
            if response in ('si', 'sí', 's', 'y', 'yes'):
                return True
            elif response in ('no', 'n'):
                return False
    
    def _builtin_pedir_numero(self, prompt):
        """Lee un número del usuario"""
        while True:
            try:
                value = input(self._builtin_texto(prompt))
                return self._builtin_numero(value)
            except (ValueError, TypeError):
                print("Por favor, ingresa un número válido")
    
    def _builtin_formatear(self, template, values):
        """Formatea una cadena"""
        result = template
        for i, value in enumerate(values):
            result = result.replace(f"{{{i}}}", self._builtin_texto(value))
        return result
    
    def _builtin_ejecutar_linea(self, code):
        """Ejecuta código dinámico"""
        from michiscript_parser import parse
        ast = parse(code)
        return self.evaluate(ast)
    
    # Métodos de evaluación
    
    def evaluate(self, node: ASTNode) -> Any:
        """Evalúa un nodo AST"""
        return node.accept(self)
    
    # Visitor methods
    
    def visit_program(self, node: Program) -> Any:
        result = None
        for stmt in node.statements:
            result = self.evaluate(stmt)
        return result
    
    def visit_literal(self, node: Literal) -> Any:
        return node.value
    
    def visit_identifier(self, node: Identifier) -> Any:
        return self.current_env.get(node.name)
    
    def visit_binary_op(self, node: BinaryOp) -> Any:
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        
        op = node.operator
        
        # Operadores aritméticos
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise ZeroDivisionError("No se puede dividir entre cero gatunos")
            return left / right
        elif op == '%':
            return left % right
        elif op == '^':
            return left ** right
        
        # Operadores de comparación
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        
        # Operadores lógicos
        elif op == '&&':
            return left and right
        elif op == '||':
            return left or right
        
        else:
            raise RuntimeError(f"Operador desconocido: {op}")
    
    def visit_unary_op(self, node: UnaryOp) -> Any:
        operand = self.evaluate(node.operand)
        
        if node.operator == '-':
            return -operand
        elif node.operator == '!':
            return not self._builtin_booleano(operand)
        else:
            raise RuntimeError(f"Operador unario desconocido: {node.operator}")
    
    def visit_assignment(self, node: Assignment) -> Any:
        value = self.evaluate(node.value)
        self.current_env.set(node.target, value)
        return value
    
    def visit_compound_assignment(self, node: CompoundAssignment) -> Any:
        current = self.current_env.get(node.target)
        value = self.evaluate(node.value)
        
        if node.operator == '+':
            result = current + value
        elif node.operator == '-':
            result = current - value
        elif node.operator == '*':
            result = current * value
        elif node.operator == '/':
            result = current / value
        else:
            raise RuntimeError(f"Operador compuesto desconocido: {node.operator}")
        
        self.current_env.set(node.target, result)
        return result
    
    def visit_call_expr(self, node: CallExpr) -> Any:
        callee = self.evaluate(node.callee)
        arguments = [self.evaluate(arg) for arg in node.arguments]
        
        # Función integrada
        if callable(callee) and not isinstance(callee, MichiFunction):
            return callee(*arguments)
        
        # Función del usuario
        if isinstance(callee, MichiFunction):
            return self._call_function(callee, arguments)
        
        # Clase (constructor)
        if isinstance(callee, MichiClass):
            return self._call_class(callee, arguments)
        
        raise TypeError(f"No se puede llamar a {type(callee).__name__}")
    
    def _call_function(self, func: MichiFunction, arguments: List[Any]) -> Any:
        """Llama a una función del usuario"""
        # Crear nuevo entorno
        call_env = Environment(func.closure)
        
        # Asignar parámetros
        for i, param in enumerate(func.parameters):
            if i < len(arguments):
                call_env.define(param, arguments[i])
            elif param in func.defaults:
                default_value = self.evaluate(func.defaults[param])
                call_env.define(param, default_value)
            else:
                raise TypeError(f"Parámetro faltante: {param}")
        
        # Ejecutar función
        prev_env = self.current_env
        self.current_env = call_env
        
        try:
            self.evaluate(func.body)
            result = None
        except ReturnException as e:
            result = e.value
        finally:
            self.current_env = prev_env
        
        return result
    
    def _call_class(self, klass: MichiClass, arguments: List[Any]) -> MichiInstance:
        """Llama a un constructor de clase"""
        instance = MichiInstance(klass)
        
        # Llamar a __inicializar si existe
        if '__inicializar' in klass.methods:
            init_method = klass.methods['__inicializar']
            
            # Crear ambiente con 'esto' = instance
            call_env = Environment(init_method.closure)
            call_env.define('esto', instance)
            
            # Asignar parámetros
            for i, param in enumerate(init_method.parameters):
                if i < len(arguments):
                    call_env.define(param, arguments[i])
                elif param in init_method.defaults:
                    default_value = self.evaluate(init_method.defaults[param])
                    call_env.define(param, default_value)
            
            # Ejecutar inicializador
            prev_env = self.current_env
            self.current_env = call_env
            
            try:
                self.evaluate(init_method.body)
                # Transferir atributos de 'esto' a instance
                if 'esto' in call_env.variables:
                    esto = call_env.variables['esto']
                    if isinstance(esto, MichiInstance):
                        instance = esto
            finally:
                self.current_env = prev_env
        
        return instance
    
    def visit_list_expr(self, node: ListExpr) -> List[Any]:
        return [self.evaluate(elem) for elem in node.elements]
    
    def visit_dict_expr(self, node: DictExpr) -> Dict[str, Any]:
        result = {}
        for key, value_expr in node.pairs:
            result[key] = self.evaluate(value_expr)
        return result
    
    def visit_index_expr(self, node: IndexExpr) -> Any:
        obj = self.evaluate(node.object)
        index = self.evaluate(node.index)
        
        try:
            return obj[index]
        except (KeyError, IndexError, TypeError) as e:
            raise IndexError(f"Índice inválido: {index}")
    
    def visit_member_expr(self, node: MemberExpr) -> Any:
        obj = self.evaluate(node.object)
        
        # Diccionario
        if isinstance(obj, dict):
            return obj.get(node.property)
        
        # Instancia
        if isinstance(obj, MichiInstance):
            if node.property in obj.attributes:
                return obj.attributes[node.property]
            if node.property in obj.klass.methods:
                # Retornar método vinculado
                method = obj.klass.methods[node.property]
                def bound_method(*args):
                    return self._call_method(obj, method, args)
                return bound_method
        
        # Métodos de lista
        if isinstance(obj, list):
            return getattr(obj, node.property, None)
        
        # Métodos de string
        if isinstance(obj, str):
            if node.property == 'mayuscula':
                return obj.upper
            elif node.property == 'minuscula':
                return obj.lower
            elif node.property == 'longitud':
                return len(obj)
        
        return None
    
    def _call_method(self, instance: MichiInstance, method: MichiFunction, arguments: List[Any]) -> Any:
        """Llama a un método vinculado"""
        call_env = Environment(method.closure)
        call_env.define('esto', instance)
        
        for i, param in enumerate(method.parameters):
            if i < len(arguments):
                call_env.define(param, arguments[i])
            elif param in method.defaults:
                default_value = self.evaluate(method.defaults[param])
                call_env.define(param, default_value)
        
        prev_env = self.current_env
        self.current_env = call_env
        
        try:
            self.evaluate(method.body)
            result = None
        except ReturnException as e:
            result = e.value
        finally:
            self.current_env = prev_env
        
        return result
    
    def visit_slice_expr(self, node: SliceExpr) -> Any:
        obj = self.evaluate(node.object)
        start = self.evaluate(node.start) if node.start else None
        end = self.evaluate(node.end) if node.end else None
        
        return obj[start:end]
    
    def visit_ternary_expr(self, node: TernaryExpr) -> Any:
        condition = self._builtin_booleano(self.evaluate(node.condition))
        
        if condition:
            return self.evaluate(node.true_expr)
        else:
            return self.evaluate(node.false_expr)
    
    def visit_lambda_expr(self, node: LambdaExpr) -> MichiFunction:
        return MichiFunction(
            "<lambda>",
            node.parameters,
            node.body,
            self.current_env,
            node.defaults
        )
    
    def visit_expr_stmt(self, node: ExprStmt) -> Any:
        return self.evaluate(node.expr)
    
    def visit_block(self, node: Block) -> Any:
        result = None
        for stmt in node.statements:
            result = self.evaluate(stmt)
        return result
    
    def visit_if_stmt(self, node: IfStmt) -> Any:
        condition = self._builtin_booleano(self.evaluate(node.condition))
        
        if condition:
            return self.evaluate(node.then_body)
        
        for elif_cond, elif_body in node.elif_parts:
            elif_condition = self._builtin_booleano(self.evaluate(elif_cond))
            if elif_condition:
                return self.evaluate(elif_body)
        
        if node.else_body:
            return self.evaluate(node.else_body)
        
        return None
    
    def visit_while_stmt(self, node: WhileStmt) -> Any:
        result = None
        
        try:
            while self._builtin_booleano(self.evaluate(node.condition)):
                try:
                    result = self.evaluate(node.body)
                except ContinueException:
                    continue
        except BreakException:
            pass
        
        return result
    
    def visit_for_stmt(self, node: ForStmt) -> Any:
        iterable = self.evaluate(node.iterable)
        result = None
        
        try:
            for value in iterable:
                self.current_env.set_local(node.variable, value)
                try:
                    result = self.evaluate(node.body)
                except ContinueException:
                    continue
        except BreakException:
            pass
        
        return result
    
    def visit_func_def(self, node: FuncDef) -> MichiFunction:
        func = MichiFunction(node.name, node.parameters, node.body, self.current_env, node.defaults)
        self.current_env.define(node.name, func)
        return func
    
    def visit_return_stmt(self, node: ReturnStmt) -> None:
        value = self.evaluate(node.value) if node.value else None
        raise ReturnException(value)
    
    def visit_break_stmt(self, node: BreakStmt) -> None:
        raise BreakException()
    
    def visit_continue_stmt(self, node: ContinueStmt) -> None:
        raise ContinueException()
    
    def visit_print_stmt(self, node: PrintStmt) -> None:
        values = [self.evaluate(expr) for expr in node.expressions]
        
        if not values:
            print()
        else:
            output = " ".join(self._builtin_texto(v) for v in values)
            print(output)
        
        return None
    
    def visit_input_stmt(self, node: InputStmt) -> str:
        if node.prompt:
            prompt = self._builtin_texto(self.evaluate(node.prompt))
        else:
            prompt = ""
        
        return input(prompt)
    
    def visit_variable_decl(self, node: VariableDecl) -> Any:
        value = self.evaluate(node.value) if node.value else None
        self.current_env.define(node.name, value)
        return value
    
    def visit_multi_assignment(self, node: MultiAssignment) -> Any:
        values = [self.evaluate(v) for v in node.values]
        
        for i, target in enumerate(node.targets):
            if i < len(values):
                self.current_env.set(target, values[i])
        
        return values
    
    def visit_class_def(self, node: ClassDef) -> MichiClass:
        methods = {}
        for method in node.methods:
            func = MichiFunction(
                method.name,
                method.parameters,
                method.body,
                self.current_env,
                method.defaults
            )
            methods[method.name] = func
        
        klass = MichiClass(node.name, methods)
        self.current_env.define(node.name, klass)
        return klass
    
    def visit_import_stmt(self, node: ImportStmt) -> None:
        # Implementación simplificada
        module_name = node.module
        alias = node.alias or module_name
        
        # Crear un módulo simulado
        module = type('Module', (), {})()
        
        if module_name == 'math':
            import math as math_module
            for name in dir(math_module):
                if not name.startswith('_'):
                    setattr(module, name, getattr(math_module, name))
        
        elif module_name == 'tiempo':
            import time
            import datetime
            module.ahora = lambda: str(datetime.datetime.now())
            module.año = lambda: datetime.datetime.now().year
            module.mes = lambda: datetime.datetime.now().month
            module.dia = lambda: datetime.datetime.now().day
            module.hora = lambda: datetime.datetime.now().hour
            module.minuto = lambda: datetime.datetime.now().minute
            module.segundo = lambda: datetime.datetime.now().second
        
        elif module_name == 'aleatorio':
            module.entero = random.randint
            module.flotante = random.random
            module.elemento = random.choice
        
        self.current_env.define(alias, module)
        return None
    
    def visit_string_method(self, obj: str, method: str, *args):
        """Maneja métodos de strings"""
        if method == 'mayuscula':
            return obj.upper()
        elif method == 'minuscula':
            return obj.lower()
        elif method == 'reemplazar':
            return obj.replace(args[0], args[1])
        elif method == 'dividir':
            return obj.split(args[0])
        elif method == 'contiene':
            return args[0] in obj
        elif method == 'comienza_con':
            return obj.startswith(args[0])
        elif method == 'termina_con':
            return obj.endswith(args[0])
        elif method == 'cortar':
            return obj[args[0]:args[1]]
        elif method == 'limpiar':
            return obj.strip()
        elif method == 'invertir':
            return obj[::-1]
        elif method == 'longitud':
            return len(obj)
        
        return None


def execute(source: str):
    """Función conveniente para ejecutar código MichiScript"""
    from michiscript_parser import parse
    
    try:
        ast = parse(source)
        evaluator = Evaluator()
        evaluator.evaluate(ast)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
