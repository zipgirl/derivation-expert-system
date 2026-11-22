# Derivation Atelier

<p align="center">
  <strong>A Zipgirl project · Rule-based symbolic differentiation</strong>
</p>

Derivation Atelier is an interactive expert system that explores symbolic derivatives and presents the mathematical rules detected along the way. It combines a rule-based inference engine with symbolic computation in a dark, editorial Streamlit interface.

## Features

- Explainable rule engine built with **Experta**.
- Symbolic parsing and differentiation powered by **SymPy**.
- Interactive web interface built with **Streamlit**.
- Explanations for linearity, constant factors, product and quotient rules, powers, trigonometric functions, exponentials and logarithms.
- Optional simplification of the resulting expression.
- Command-line entry point for terminal use.

## Tech stack

- Python 3.10+
- Experta
- SymPy
- Streamlit

## Run locally

1. Clone this repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Launch the interface:

   ```bash
   streamlit run app.py
   ```

For the terminal interface, run `python main.py`.

## Input examples

| Function | Input |
| --- | --- |
| Polynomial | `x^3 + 2*x^2 - 5*x + 1` |
| Chain rule | `sin(x^2)` |
| Quotient | `(3*x + 1)/(x^2 + 4)` |
| Exponential and logarithm | `exp(2*x) + ln(x)` |
| Logarithm with base | `log(x, 2)` |

Use explicit multiplication, such as `3*x`.

## Project structure

```text
.
├── analyzer.py   # Expression parsing and rule declarations
├── app.py        # Streamlit interface
├── main.py       # Terminal interface
├── rules.py      # Experta inference rules
└── requirements.txt
```

---

Made with care by **Zipgirl**.
