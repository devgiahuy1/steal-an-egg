"""Steal An Egg 3D
Chay: streamlit run app.py
Can file steal_an_egg.html cung thu muc.
"""
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

HERE = Path(__file__).resolve().parent
GAME_PATH = HERE / "steal_an_egg.html"

st.set_page_config(
    page_title="Steal An Egg 3D",
    page_icon="🥚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:#0b1220}
.block-container{padding:0.2rem!important;max-width:100%!important}
#MainMenu,footer,header{visibility:hidden}
</style>
""", unsafe_allow_html=True)

if not GAME_PATH.exists():
    st.error("Không tìm thấy steal_an_egg.html")
    st.stop()

html = GAME_PATH.read_text(encoding="utf-8")
components.html(html, height=860, scrolling=False)
