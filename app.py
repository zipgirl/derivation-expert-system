import io
from contextlib import redirect_stdout

import streamlit as st
import sympy as sp

from analyzer import analizar_funcion
from rules import DerivadorExperto


st.set_page_config(
    page_title="Derivation Atelier | Zipgirl",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root { --ink:#100d12; --panel:#1a151d; --panel2:#211a24; --pink:#e6a9c2; --rose:#bd7897; --wine:#71384f; --muted:#b8aab5; }
.stApp { background: radial-gradient(ellipse at 78% 0%, #392132 0%, #17121a 34%, #100d12 75%); color:#f7edf2; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
h1,h2,h3 { font-family:'Playfair Display',serif !important; color:#fff2f7 !important; }
.block-container { max-width:1120px; padding-top:2.4rem; padding-bottom:4rem; }
[data-testid="stSidebar"] { background:#151018; border-right:1px solid #49303e; }
[data-testid="stSidebar"] * { color:#eadde5; }
.eyebrow { color:#e6a9c2; font:500 11px 'DM Mono',monospace; letter-spacing:.22em; text-transform:uppercase; }
.hero { padding:2.2rem 0 1.5rem; border-bottom:1px solid #49303e; margin-bottom:2rem; }
.hero h1 { font-size:clamp(2.7rem,6vw,5rem); line-height:1.02; margin:.65rem 0; }
.hero p { color:#c9b8c3; max-width:650px; font-size:1.05rem; }
.ornament { color:#e6a9c2; letter-spacing:.55em; font-size:13px; }
.panel { background:linear-gradient(145deg,rgba(39,29,41,.96),rgba(24,19,27,.96)); border:1px solid #523849; border-radius:16px; padding:1.2rem 1.4rem; }
.result { border:1px solid #9c5d7b; background:linear-gradient(135deg,#2d1c2a,#1a151d); border-radius:16px; padding:1.4rem 1.6rem; margin:1rem 0; }
.result-label { color:#e6a9c2; font:500 11px 'DM Mono',monospace; letter-spacing:.16em; text-transform:uppercase; }
div[data-testid="stTextInput"] input { background:#17121a; color:#fff2f7; border:1px solid #654459; border-radius:10px; }
.stButton>button, .stFormSubmitButton>button { background:linear-gradient(110deg,#a85f80,#71384f); color:white; border:1px solid #d28eac; border-radius:999px; padding:.65rem 1.4rem; font-weight:600; }
.stButton>button:hover, .stFormSubmitButton>button:hover { border-color:#f0c0d4; color:white; background:#8d4b69; }
div[data-testid="stAlert"] { border-radius:12px; }
hr { border-color:#49303e; }
small, .muted { color:#b8aab5; }
code { color:#f1b9d0 !important; background:#2b202b !important; }
.step { border-left:2px solid #bd7897; padding:.25rem 0 .5rem 1rem; margin:.7rem 0; color:#e9dce4; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="eyebrow">ZIPGIRL · MATH LAB</div>', unsafe_allow_html=True)
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
st.caption("DERIVATION ATELIER · ZIPGIRL · Python / Experta / SymPy / Streamlit")
