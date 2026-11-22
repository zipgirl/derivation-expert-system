import io
from contextlib import redirect_stdout

import streamlit as st
import sympy as sp

from analyzer import analizar_funcion
from rules import DerivadorExperto


st.set_page_config(
    page_title="Derivation Atelier | ZipGirl",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="expanded",
)

light_theme = st.session_state.get("light_theme", False)
palette = {
    "bg": "#f8f0f2" if light_theme else "#100d12",
    "bg_alt": "#f6e9ee" if light_theme else "#17121a",
    "glow": "#ead5df" if light_theme else "#392132",
    "panel": "#fff9fb" if light_theme else "#1a151d",
    "panel2": "#f2e2e8" if light_theme else "#211a24",
    "ink": "#261923" if light_theme else "#f7edf2",
    "muted": "#765f6c" if light_theme else "#b8aab5",
    "pink": "#9d456b" if light_theme else "#e6a9c2",
    "rose": "#a94c72" if light_theme else "#bd7897",
    "wine": "#6d263f" if light_theme else "#71384f",
    "line": "#dfc5d0" if light_theme else "#49303e",
    "input": "#fffafd" if light_theme else "#17121a",
    "code": "#f1e3e9" if light_theme else "#2b202b",
}
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root {{
  --app-bg: {palette["bg"]};
  --app-bg-alt: {palette["bg_alt"]};
  --app-glow: {palette["glow"]};
  --app-panel: {palette["panel"]};
  --app-panel-2: {palette["panel2"]};
  --app-ink: {palette["ink"]};
  --app-muted: {palette["muted"]};
  --app-pink: {palette["pink"]};
  --app-rose: {palette["rose"]};
  --app-wine: {palette["wine"]};
  --app-line: {palette["line"]};
  --app-input: {palette["input"]};
  --app-code: {palette["code"]};
}}
.stApp {{ background: radial-gradient(ellipse at 78% 0%, var(--app-glow) 0%, var(--app-bg-alt) 34%, var(--app-bg) 75%); color: var(--app-ink); }}
html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; color: var(--app-ink); }}
h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: var(--app-ink) !important; }}
.block-container {{ max-width: 1120px; padding-top: 2.4rem; padding-bottom: 4rem; }}
[data-testid="stSidebar"] {{ background: var(--app-panel); border-right: 1px solid var(--app-line); }}
[data-testid="stSidebar"] * {{ color: var(--app-ink); }}
.eyebrow {{ color: var(--app-pink); font: 500 11px 'DM Mono', monospace; letter-spacing: .22em; text-transform: uppercase; }}
.hero {{ padding: 2.2rem 0 1.5rem; border-bottom: 1px solid var(--app-line); margin-bottom: 2rem; }}
.hero h1 {{ font-size: clamp(2.7rem,6vw,5rem); line-height: 1.02; margin: .65rem 0; }}
.hero p {{ color: var(--app-muted); max-width: 650px; font-size: 1.05rem; }}
.ornament {{ color: var(--app-pink); letter-spacing: .55em; font-size: 13px; }}
.panel {{ background: linear-gradient(145deg,var(--app-panel-2),var(--app-panel)); border: 1px solid var(--app-line); border-radius: 16px; padding: 1.2rem 1.4rem; }}
.result {{ border: 1px solid var(--app-rose); background: linear-gradient(135deg,var(--app-panel-2),var(--app-panel)); border-radius: 16px; padding: 1.4rem 1.6rem; margin: 1rem 0; }}
.result-label {{ color: var(--app-pink); font: 500 11px 'DM Mono',monospace; letter-spacing: .16em; text-transform: uppercase; }}
div[data-testid="stTextInput"] input {{ background: var(--app-input); color: var(--app-ink); border: 1px solid var(--app-rose); border-radius: 10px; }}
.stButton>button, .stFormSubmitButton>button {{ background: linear-gradient(110deg,var(--app-rose),var(--app-wine)); color: white; border: 1px solid var(--app-pink); border-radius: 999px; padding: .65rem 1.4rem; font-weight: 600; }}
.stButton>button:hover, .stFormSubmitButton>button:hover {{ border-color: var(--app-pink); color: white; background: var(--app-wine); }}
div[data-testid="stAlert"] {{ border-radius: 12px; }}
hr {{ border-color: var(--app-line); }}
small, .muted {{ color: var(--app-muted); }}
code {{ color: var(--app-pink) !important; background: var(--app-code) !important; }}
.step {{ border-left: 2px solid var(--app-rose); padding: .25rem 0 .5rem 1rem; margin: .7rem 0; color: var(--app-ink); }}
footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="eyebrow">ZipGirl · Math Lab</div>', unsafe_allow_html=True)
    st.toggle("Tema claro", key="light_theme", help="Alterna entre la paleta clara y oscura.")
    st.markdown("## Guía de notación")
    st.markdown("""
    - **Potencias:** `x^3` o `x**3`
    - **Multiplicación:** `3*x`
    - **División:** `(x+1)/(x-2)`
    - **Trigonometría:** `sin(x)`, `cos(x)`, `tan(x)`
    - **Exponencial:** `exp(x)`
    - **Logaritmos:** `ln(x)`, `log(x, 2)`
    """)
    st.divider()
    st.markdown("### Ejemplos")
    examples = [
        "x^3 + 2*x^2 - 5*x + 1",
        "sin(x^2)",
        "(3*x + 1)/(x^2 + 4)",
        "exp(2*x) + ln(x)",
        "log(x, 2)",
    ]
    selected_example = st.selectbox("Elegí una función", ["Seleccionar..."] + examples)
    st.caption("El motor explica las reglas detectadas y SymPy calcula el resultado simbólico.")

st.markdown("""
<div class="hero">
  <div class="eyebrow">A RULE-BASED DIFFERENTIATION EXPERIENCE</div>
  <div class="ornament">✳ ───── ✧ ───── ✳</div>
  <h1>Derivation<br><em>Atelier.</em></h1>
  <p>Un sistema experto para explorar derivadas simbólicas. Ingresá una función y descubrí qué reglas matemáticas intervienen en su resolución.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="eyebrow">01 / INPUT</div>', unsafe_allow_html=True)
with st.form("derivative_form"):
    default_value = selected_example if selected_example != "Seleccionar..." else "(-x^2) * (x^-1 - 5)"
    function_text = st.text_input("Función de x", value=default_value, placeholder="Por ejemplo: sin(x^2) + 3*x")
    submitted = st.form_submit_button("✳ Analizar y derivar", use_container_width=False)

if submitted:
    if not function_text.strip():
        st.warning("Ingresá una función para comenzar.")
    else:
        try:
            engine = DerivadorExperto()
            engine.reset()
            captured = io.StringIO()
            with redirect_stdout(captured):
                expression, derivative = analizar_funcion(engine, function_text)

            steps = [line.strip() for line in captured.getvalue().splitlines() if line.strip()]
            st.session_state["expression"] = expression
            st.session_state["derivative"] = derivative
            st.session_state["steps"] = steps
            st.session_state["simplified"] = None
        except Exception as exc:
            st.error(f"No pudimos interpretar esa función: {exc}")

if "derivative" in st.session_state:
    st.markdown("---")
    st.markdown('<div class="eyebrow">02 / EXPERT REASONING</div>', unsafe_allow_html=True)
    st.subheader("El razonamiento del motor")
    recursive = [s for s in st.session_state.get("steps", []) if "[RECURSIVA]" in s]
    atomic = [s for s in st.session_state.get("steps", []) if "[ATÓMICA]" in s]
    if not recursive and not atomic:
        st.info("La expresión no activó reglas explicativas específicas, pero el resultado simbólico está disponible.")
    for step in recursive + atomic:
        clean = step.replace("[RECURSIVA]", "").replace("[ATÓMICA]", "").strip()
        st.markdown(f'<div class="step">{clean}</div>', unsafe_allow_html=True)

    st.markdown('<div class="eyebrow">03 / DERIVATIVE</div>', unsafe_allow_html=True)
    st.markdown('<div class="result"><div class="result-label">Resultado sin simplificar</div></div>', unsafe_allow_html=True)
    st.latex(sp.latex(st.session_state["derivative"]))

    if st.button("✧ Simplificar resultado"):
        st.session_state["simplified"] = sp.simplify(st.session_state["derivative"])
    if st.session_state.get("simplified") is not None:
        st.markdown('<div class="result"><div class="result-label">Forma simplificada</div></div>', unsafe_allow_html=True)
        st.latex(sp.latex(st.session_state["simplified"]))

st.markdown("---")
st.markdown('<div class="ornament">✳ &nbsp; ✧ &nbsp; ✳</div>', unsafe_allow_html=True)
st.caption("DERIVATION ATELIER · ZipGirl · Python / Experta / SymPy / Streamlit")
