"""Command-line entry point for the differentiation engine."""

from analyzer import analizar_funcion
from rules import DerivadorExperto


def menu():
    print("DERIVATION ATELIER · ZIPGIRL")
    print("Escribí una función en x o 'salir' para terminar.")
    while True:
        raw = input("\nFunción: ").strip()
        if raw.lower() == "salir":
            break
        try:
            engine = DerivadorExperto()
            engine.reset()
            expression, derivative = analizar_funcion(engine, raw)
            print(f"Derivada: {derivative}")
        except Exception as exc:
            print(f"No se pudo resolver la expresión: {exc}")


if __name__ == "__main__":
    menu()
