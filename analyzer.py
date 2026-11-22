"""Expression parsing and fact declaration for the expert engine."""

import sympy as sp
from rules import Operacion


def parse_expression(raw_text: str):
    """Parse common calculator notation into a SymPy expression."""
    normalized = raw_text.strip().replace("^", "**")
    normalized = normalized.replace("ln(", "log(")
    x = sp.Symbol("x")
    return sp.sympify(normalized, locals={"x": x, "e": sp.E, "pi": sp.pi})


def analizar_funcion(engine, texto):
    """Declare detected operations, run the rules, and return the derivative."""
    x = sp.Symbol("x")
    expr = parse_expression(texto)

    if expr.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
        raise ValueError("La expresión contiene una división por cero o un valor infinito.")

    for node in sp.preorder_traversal(expr):
        kind = type(node).__name__

        if node.is_Number:
            if node == expr:
                engine.declare(Operacion(tipo="Constante", valor=float(node)))
            continue

        if kind == "Pow" and node.args[1].is_Number and node.args[1] < 0:
            engine.declare(Operacion(tipo="Div"))

        if kind == "Add":
            engine.declare(Operacion(tipo="Add"))
        elif kind == "Mul":
            has_constant = any(arg.is_Number for arg in node.args)
            engine.declare(Operacion(tipo="Mul", tiene_constante=has_constant))
        elif kind == "Pow":
            if node.args[0] == x:
                engine.declare(Operacion(tipo="Pow", base="x", exp=node.args[1]))
        elif node.func in (sp.sin, sp.cos, sp.tan, sp.exp):
            engine.declare(Operacion(tipo=node.func.__name__, arg=str(node.args[0])))
        elif node.func == sp.log:
            if len(node.args) > 1:
                engine.declare(Operacion(
                    tipo="log_base_n",
                    base=str(node.args[1]),
                    arg=str(node.args[0]),
                ))
            else:
                engine.declare(Operacion(tipo="log", arg=str(node.args[0])))
        elif node.is_Symbol:
            engine.declare(Operacion(tipo="Identidad"))

    engine.run()
    return expr, sp.diff(expr, x)
