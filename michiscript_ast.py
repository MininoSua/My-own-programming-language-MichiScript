"""
MichiScript AST (Abstract Syntax Tree)
Defines las estructuras del árbol de sintaxis abstracta
"""

from dataclasses import dataclass
from typing import List, Optional, Any, Dict
from abc import ABC, abstractmethod


class ASTNode(ABC):
    """Nodo base del árbol de sintaxis"""
    @abstractmethod
    def accept(self, visitor):
        pass


# Expresiones

@dataclass
class Literal(ASTNode):
    """Número, string, booleano, null"""
    value: Any
    
    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class Identifier(ASTNode):
    """Variable o identificador"""
    name: str
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)


@dataclass
class BinaryOp(ASTNode):
    """Operación binaria (a + b, a == b, etc)"""
    left: ASTNode
    operator: str
    right: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)


@dataclass
class UnaryOp(ASTNode):
    """Operación unaria (-a, !a, etc)"""
    operator: str
    operand: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)


@dataclass
class Assignment(ASTNode):
    """Asignación de variable (a = 5)"""
    target: str
    value: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)


@dataclass
class CompoundAssignment(ASTNode):
    """Asignación compuesta (a += 5)"""
    target: str
    operator: str
    value: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_compound_assignment(self)


@dataclass
class CallExpr(ASTNode):
    """Llamada a función (func(a, b))"""
    callee: ASTNode
    arguments: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_call_expr(self)


@dataclass
class ListExpr(ASTNode):
    """Lista ([1, 2, 3])"""
    elements: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_list_expr(self)


@dataclass
class DictExpr(ASTNode):
    """Diccionario ({a: 1, b: 2})"""
    pairs: List[tuple]  # Lista de (clave, valor)
    
    def accept(self, visitor):
        return visitor.visit_dict_expr(self)


@dataclass
class IndexExpr(ASTNode):
    """Acceso a índice (a[0])"""
    object: ASTNode
    index: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_index_expr(self)


@dataclass
class MemberExpr(ASTNode):
    """Acceso a miembro (a.b)"""
    object: ASTNode
    property: str
    
    def accept(self, visitor):
        return visitor.visit_member_expr(self)


@dataclass
class SliceExpr(ASTNode):
    """Rebanada ([inicio:fin])"""
    object: ASTNode
    start: Optional[ASTNode]
    end: Optional[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_slice_expr(self)


@dataclass
class TernaryExpr(ASTNode):
    """Expresión ternaria (a si b sino c)"""
    condition: ASTNode
    true_expr: ASTNode
    false_expr: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_ternary_expr(self)


@dataclass
class LambdaExpr(ASTNode):
    """Función anónima (funcion(x) { retorna x * 2 })"""
    parameters: List[str]
    body: ASTNode
    defaults: Dict[str, ASTNode] = None
    
    def __post_init__(self):
        if self.defaults is None:
            self.defaults = {}
    
    def accept(self, visitor):
        return visitor.visit_lambda_expr(self)


# Sentencias

@dataclass
class ExprStmt(ASTNode):
    """Expresión como sentencia"""
    expr: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_expr_stmt(self)


@dataclass
class Block(ASTNode):
    """Bloque de código { ... }"""
    statements: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_block(self)


@dataclass
class IfStmt(ASTNode):
    """Sentencia si/sino"""
    condition: ASTNode
    then_body: ASTNode
    elif_parts: List[tuple] = None  # Lista de (condición, cuerpo)
    else_body: Optional[ASTNode] = None
    
    def __post_init__(self):
        if self.elif_parts is None:
            self.elif_parts = []
    
    def accept(self, visitor):
        return visitor.visit_if_stmt(self)


@dataclass
class WhileStmt(ASTNode):
    """Bucle mientras"""
    condition: ASTNode
    body: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_while_stmt(self)


@dataclass
class ForStmt(ASTNode):
    """Bucle para"""
    variable: str
    iterable: ASTNode
    body: ASTNode
    
    def accept(self, visitor):
        return visitor.visit_for_stmt(self)


@dataclass
class FuncDef(ASTNode):
    """Definición de función"""
    name: str
    parameters: List[str]
    body: ASTNode
    defaults: Dict[str, ASTNode] = None
    
    def __post_init__(self):
        if self.defaults is None:
            self.defaults = {}
    
    def accept(self, visitor):
        return visitor.visit_func_def(self)


@dataclass
class ReturnStmt(ASTNode):
    """Sentencia retorna"""
    value: Optional[ASTNode] = None
    
    def accept(self, visitor):
        return visitor.visit_return_stmt(self)


@dataclass
class BreakStmt(ASTNode):
    """Sentencia rascar (break)"""
    
    def accept(self, visitor):
        return visitor.visit_break_stmt(self)


@dataclass
class ContinueStmt(ASTNode):
    """Sentencia ronronear (continue)"""
    
    def accept(self, visitor):
        return visitor.visit_continue_stmt(self)


@dataclass
class PrintStmt(ASTNode):
    """Sentencia traer (print)"""
    expressions: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_print_stmt(self)


@dataclass
class InputStmt(ASTNode):
    """Sentencia pedir (input)"""
    prompt: Optional[ASTNode] = None
    
    def accept(self, visitor):
        return visitor.visit_input_stmt(self)


@dataclass
class VariableDecl(ASTNode):
    """Declaración de variable"""
    name: str
    value: Optional[ASTNode] = None
    
    def accept(self, visitor):
        return visitor.visit_variable_decl(self)


@dataclass
class MultiAssignment(ASTNode):
    """Asignación múltiple (a, b, c = 1, 2, 3)"""
    targets: List[str]
    values: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_multi_assignment(self)


@dataclass
class ClassDef(ASTNode):
    """Definición de clase"""
    name: str
    methods: List[FuncDef]
    
    def accept(self, visitor):
        return visitor.visit_class_def(self)


@dataclass
class ImportStmt(ASTNode):
    """Sentencia olfatear (import)"""
    module: str
    alias: Optional[str] = None
    
    def accept(self, visitor):
        return visitor.visit_import_stmt(self)


@dataclass
class Program(ASTNode):
    """Programa completo"""
    statements: List[ASTNode]
    
    def accept(self, visitor):
        return visitor.visit_program(self)
