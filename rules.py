"""Rule-based explanation engine for symbolic differentiation."""

# Compatibility shim required by Experta's older dependency stack.
import collections
if not hasattr(collections, "Mapping"):
    import collections.abc
    collections.Mapping = collections.abc.Mapping

from experta import *


class Operacion(Fact):
    """A mathematical operation detected in the input expression."""
    pass


class DerivadorExperto(KnowledgeEngine):
    @Rule(Operacion(tipo="Add"))
    def regla_suma(self):
        print("\n[RECURSIVA] Regla de linealidad: d/dx[f(x) ± g(x)]")
        print("Lógica: derivar cada término por separado.")

    @Rule(Operacion(tipo="Mul", tiene_constante=True))
    def regla_constante_por_f(self):
        print("\n[RECURSIVA] Factor constante: d/dx[c · f(x)]")
        print("Lógica: conservar la constante y derivar la función.")

    @Rule(Operacion(tipo="Mul", tiene_constante=False))
    def regla_producto(self):
        print("\n[RECURSIVA] Regla del producto: d/dx[u · v]")
        print("Lógica: u' · v + u · v'.")

    @Rule(Operacion(tipo="Div"))
    def regla_cociente(self):
        print("\n[RECURSIVA] Regla del cociente: d/dx[u / v]")
        print("Lógica: (u' · v - u · v') / v².")

    @Rule(Operacion(tipo="sin", arg=MATCH.u))
    def regla_sin(self, u):
        print(f"\n[RECURSIVA] Derivada del seno: d/dx[sin({u})]")
        print(f"Lógica: cos({u}) · d/dx({u}).")

    @Rule(Operacion(tipo="cos", arg=MATCH.u))
    def regla_cos(self, u):
        print(f"\n[RECURSIVA] Derivada del coseno: d/dx[cos({u})]")
        print(f"Lógica: -sin({u}) · d/dx({u}).")

    @Rule(Operacion(tipo="tan", arg=MATCH.u))
    def regla_tan(self, u):
        print(f"\n[RECURSIVA] Derivada de la tangente: d/dx[tan({u})]")
        print(f"Lógica: sec²({u}) · d/dx({u}).")

    @Rule(Operacion(tipo="exp", arg=MATCH.u))
    def regla_exp(self, u):
        print(f"\n[RECURSIVA] Derivada exponencial: d/dx[e^({u})]")
        print(f"Lógica: e^({u}) · d/dx({u}).")

    @Rule(Operacion(tipo="log", arg=MATCH.u))
    def regla_ln(self, u):
        print(f"\n[RECURSIVA] Logaritmo natural: d/dx[ln({u})]")
        print(f"Lógica: (1 / {u}) · d/dx({u}).")

    @Rule(Operacion(tipo="log_base_n", base=MATCH.a, arg=MATCH.u))
    def regla_log_base_n(self, a, u):
        print(f"\n[RECURSIVA] Logaritmo en base {a}: d/dx[log_{a}({u})]")
        print(f"Lógica: d/dx({u}) / ({u} · ln({a})).")

    @Rule(Operacion(tipo="Pow", base="x", exp=MATCH.n))
    def regla_potencia(self, n):
        n_val = float(n)
        if n_val == 0:
            print("\n[ATÓMICA] Potencia cero: d/dx(x⁰) = 0.")
        else:
            print(f"\n[ATÓMICA] Regla de la potencia: d/dx(x^{n}) = {n} · x^({n_val - 1:g}).")

    @Rule(Operacion(tipo="Identidad"))
    def regla_x(self):
        print("\n[ATÓMICA] Identidad: d/dx(x) = 1.")

    @Rule(Operacion(tipo="Constante", valor=MATCH.v))
    def regla_constante(self, v):
        print(f"\n[ATÓMICA] Constante ({v}): su derivada es 0.")
