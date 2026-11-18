import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Kalkulator Streamlit",
    page_icon="🧮",
    layout="centered"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #FAF4E6;
        color: #1E1E1E;
    }
    /* Layar Tampilan Kalkulator */
    .calc-display {
        background-color: #1E1E1E;
        color: #FFFFFF;
        font-family: 'Courier New', Courier, monospace;
        font-size: 42px;
        font-weight: bold;
        text-align: right;
        padding: 22px;
        border-radius: 14px;
        margin-bottom: 18px;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.6);
        overflow-x: auto;
    }
    .calc-subdisplay {
        font-size: 16px;
        color: #FF7A2F;
        text-align: right;
        margin-bottom: 5px;
        min-height: 22px;
    }
    /* Memperbesar Tombol & Teks di Dalamnya */
    div[data-testid="stButton"] button {
        width: 100% !important;
        min-height: 68px !important;
        border-radius: 12px !important;
        border: 1px solid #E5DEC9 !important;
        background-color: #FFFFFF !important;
        color: #1E1E1E !important;
        box-shadow: 0 3px 6px rgba(0,0,0,0.08) !important;
        transition: all 0.15s ease !important;
    }
    div[data-testid="stButton"] button p {
        font-size: 24px !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #FF7A2F !important;
        color: #FFFFFF !important;
        border-color: #FF7A2F !important;
        transform: translateY(-2px);
    }
    /* Warna khusus untuk tombol Primary (tombol '=' dan 'C') */
    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #FF7A2F !important;
        color: #FFFFFF !important;
        border-color: #FF7A2F !important;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        background-color: #E0631B !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🧮 KALKULATOR PRO</h1>", unsafe_allow_html=True)

# --- INISIALISASI STATE ---
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "last_expr" not in st.session_state:
    st.session_state.last_expr = ""
if "history" not in st.session_state:
    st.session_state.history = []

# --- FUNGSI LOGIKA KALKULATOR ---
def press(val):
    st.session_state.expression += str(val)

def clear():
    st.session_state.expression = ""
    st.session_state.last_expr = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def calculate():
    try:
        expr = st.session_state.expression
        clean_expr = expr.replace("×", "*").replace("÷", "/").replace("%", "/100")
        result = eval(clean_expr)
        
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        else:
            result = round(result, 8)
            
        st.session_state.last_expr = f"{expr} ="
        st.session_state.history.insert(0, f"{expr} = {result}")
        st.session_state.expression = str(result)
    except ZeroDivisionError:
        st.session_state.last_expr = "Error"
        st.session_state.expression = "Tidak bisa dibagi 0"
    except Exception:
        st.session_state.last_expr = "Error"
        st.session_state.expression = "Format Salah"

# --- TAMPILAN LAYAR ---
display_text = st.session_state.expression if st.session_state.expression != "" else "0"
st.markdown(f"""
<div class="calc-display">
    <div class="calc-subdisplay">{st.session_state.last_expr}</div>
    {display_text}
</div>
""", unsafe_allow_html=True)

# --- GRID TOMBOL KALKULATOR ---
buttons = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "( )", "="]
]

for row in buttons:
    cols = st.columns(4)
    for idx, label in enumerate(row):
        with cols[idx]:
            if label == "C":
                st.button("C", key="btn_c", on_click=clear, use_container_width=True)
            elif label == "⌫":
                st.button("⌫", key="btn_back", on_click=backspace, use_container_width=True)
            elif label == "=":
                st.button("=", key="btn_eq", type="primary", on_click=calculate, use_container_width=True)
            elif label == "( )":
                def toggle_paren():
                    if st.session_state.expression.count("(") > st.session_state.expression.count(")"):
                        press(")")
                    else:
                        press("(")
                st.button("( )", key="btn_paren", on_click=toggle_paren, use_container_width=True)
            else:
                st.button(label, key=f"btn_{label}", on_click=press, args=(label,), use_container_width=True)

# --- RIWAYAT PERHITUNGAN ---
st.write("")
with st.expander("📜 Riwayat Perhitungan"):
    if st.session_state.history:
        for item in st.session_state.history[:10]:
            st.write(f"• `{item}`")
        if st.button("Hapus Riwayat", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.caption("Belum ada riwayat perhitungan.")