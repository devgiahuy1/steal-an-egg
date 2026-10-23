"""
Steal An Egg - Streamlit (logic chinh)
HTML 3D chi la giao dien phu.
Chay: streamlit run app.py
"""
from __future__ import annotations

import random
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Steal An Egg",
    page_icon="🥚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] { background: #0b1220; }
.block-container { padding-top: 1rem !important; max-width: 1100px !important; }
#MainMenu, footer, header { visibility: hidden; }
.stMetric { background: #1e293b; border: 1px solid #38bdf8; border-radius: 12px; padding: 8px; }
div[data-testid="stMetricValue"] { color: #e0f2fe !important; }
</style>
""",
    unsafe_allow_html=True,
)

BIOMES = [
    {"id": "forest", "name": "Forest", "speed": 0, "egg": "Chicken Egg", "income": 8, "rarity": "common", "guardian": "Chicken"},
    {"id": "lake", "name": "Lake", "speed": 900, "egg": "Frog Egg", "income": 35, "rarity": "uncommon", "guardian": "Swan"},
    {"id": "desert", "name": "Desert", "speed": 10_000, "egg": "Jerboa Egg", "income": 120, "rarity": "rare", "guardian": "Scorpion"},
    {"id": "ocean", "name": "Abyss Ocean", "speed": 2_500_000, "egg": "Whale Egg", "income": 4_200, "rarity": "legendary", "guardian": "Whale"},
    {"id": "volcano", "name": "Volcano", "speed": 700_000, "egg": "Cerberus Egg", "income": 8_500, "rarity": "legendary", "guardian": "Cerberus"},
    {"id": "prehistoric", "name": "Prehistoric", "speed": 18_000_000, "egg": "T-Rex Egg", "income": 89_121, "rarity": "legendary", "guardian": "T-Rex"},
    {"id": "temple", "name": "Titan Temple", "speed": 7_000_000_000, "egg": "Gorilla Egg", "income": 120_000_000, "rarity": "divine", "guardian": "Gorilla"},
    {"id": "cherry", "name": "Cherry Blossom", "speed": 2_500_000_000, "egg": "Kitsune Egg", "income": 85_000_000, "rarity": "divine", "guardian": "Kitsune"},
    {"id": "angels", "name": "Angels & Demons", "speed": 20_000_000_000, "egg": "ArchAngel Egg", "income": 500_000_000, "rarity": "divine", "guardian": "ArchAngel"},
]

RARITY_COLOR = {
    "common": "⬜",
    "uncommon": "🟩",
    "rare": "🟦",
    "legendary": "🟧",
    "divine": "🟪",
}


def init_state():
    defaults = {
        "speed": 5_000,
        "money": 0,
        "pets": [],
        "carrying": None,
        "location": "Base",
        "log": ["Chào mừng đến Steal An Egg!"],
        "show_3d": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def add_log(msg: str):
    st.session_state.log = ([msg] + st.session_state.log)[:12]


def fmt(n) -> str:
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


init_state()


def do_treadmill():
    gain = random.randint(200, 800)
    if st.session_state.speed < 50_000:
        gain += random.randint(100, 400)
    st.session_state.speed += gain
    add_log(f"🏋️ Treadmill +{fmt(gain)} Speed")


def go_base():
    st.session_state.location = "Base"
    add_log("🏠 Đã về Base")


def go_biome(biome: dict):
    need = biome["speed"]
    if st.session_state.speed < need:
        add_log(f"❌ Cần {fmt(need)} Speed để vào {biome['name']}")
        return
    st.session_state.location = biome["name"]
    add_log(f"📍 Đã tới {biome['name']} (Guardian: {biome['guardian']})")


def steal_egg():
    if st.session_state.carrying:
        add_log("⚠️ Đang cầm trứng rồi! Hãy ấp trong chuồng ở Base")
        return
    loc = st.session_state.location
    if loc == "Base":
        add_log("⚠️ Ở Base không có trứng. Hãy vào biome!")
        return
    biome = next((b for b in BIOMES if b["name"] == loc), None)
    if not biome:
        add_log("⚠️ Biome không hợp lệ")
        return
    if st.session_state.speed < biome["speed"]:
        add_log(f"❌ Cần {fmt(biome['speed'])} Speed")
        return

    catch_chance = min(0.45, 0.08 + BIOMES.index(biome) * 0.04)
    if random.random() < catch_chance:
        add_log(f"💀 {biome['guardian']} bắt được bạn! Mất trứng")
        return

    st.session_state.carrying = {
        "name": biome["egg"],
        "income": biome["income"],
        "rarity": biome["rarity"],
        "biome": biome["name"],
    }
    add_log(f"🥚 Cướp thành công {biome['egg']}! Chạy về Base → Ấp trứng")


def hatch_egg():
    if not st.session_state.carrying:
        add_log("⚠️ Không cầm trứng nào")
        return
    if st.session_state.location != "Base":
        add_log("⚠️ Phải về Base để ấp trong chuồng!")
        return
    egg = st.session_state.carrying
    pet_name = egg["name"].replace(" Egg", "")
    reward = int(egg["income"] * 6)
    st.session_state.pets.append(
        {"name": pet_name, "income": egg["income"], "rarity": egg["rarity"]}
    )
    st.session_state.money += reward
    st.session_state.carrying = None
    add_log(f"✨ Ấp thành công {egg['name']} → pet {pet_name} · +${fmt(reward)}")


def collect_income():
    if not st.session_state.pets:
        add_log("⚠️ Chưa có pet")
        return
    total = sum(p["income"] for p in st.session_state.pets)
    gain = max(1, int(total * random.uniform(0.3, 0.7)))
    st.session_state.money += gain
    add_log(f"💰 Thu hoạch từ pets +${fmt(gain)}")


st.title("🥚 Steal An Egg")
st.caption("Logic chạy bằng Python Streamlit · HTML 3D chỉ là giao diện phụ")

c1, c2, c3, c4 = st.columns(4)
c1.metric("⚡ Speed", fmt(st.session_state.speed))
c2.metric("💰 Money", f"${fmt(st.session_state.money)}")
c3.metric("🐣 Pets", str(len(st.session_state.pets)))
c4.metric("📍 Location", st.session_state.location)

if st.session_state.carrying:
    egg = st.session_state.carrying
    st.info(f"🥚 Đang cầm: **{egg['name']}** ({egg['rarity']}) — về Base rồi bấm **Ấp trứng**")

st.divider()
st.subheader("Hành động")
a1, a2, a3, a4 = st.columns(4)
with a1:
    if st.button("🏋️ Treadmill", use_container_width=True):
        do_treadmill()
        st.rerun()
with a2:
    if st.button("🏠 Về Base", use_container_width=True):
        go_base()
        st.rerun()
with a3:
    if st.button("🥚 Cướp trứng", use_container_width=True):
        steal_egg()
        st.rerun()
with a4:
    if st.button("🪺 Ấp trứng", use_container_width=True):
        hatch_egg()
        st.rerun()

b1, b2 = st.columns(2)
with b1:
    if st.button("💰 Thu hoạch pet", use_container_width=True):
        collect_income()
        st.rerun()
with b2:
    st.session_state.show_3d = st.toggle("Hiện giao diện 3D (HTML)", value=st.session_state.show_3d)

st.divider()
st.subheader("Chọn biome")
cols = st.columns(3)
for i, biome in enumerate(BIOMES):
    with cols[i % 3]:
        locked = st.session_state.speed < biome["speed"]
        label = f"{'🔒 ' if locked else ''}{biome['name']}"
        help_txt = f"Cần {fmt(biome['speed'])} Speed · {biome['egg']} · ${fmt(biome['income'])}/s"
        if st.button(label, key=f"bio_{biome['id']}", use_container_width=True, help=help_txt, disabled=locked):
            go_biome(biome)
            st.rerun()

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Pets")
    if not st.session_state.pets:
        st.write("Chưa có pet. Cướp trứng → về Base → Ấp.")
    else:
        total = sum(p["income"] for p in st.session_state.pets)
        for p in st.session_state.pets:
            icon = RARITY_COLOR.get(p["rarity"], "⬜")
            st.write(f"{icon} **{p['name']}** — ${fmt(p['income'])}/s")
        st.success(f"Tổng thu nhập: ${fmt(total)}/s")

with right:
    st.subheader("Nhật ký")
    for line in st.session_state.log:
        st.write("· " + line)

if st.session_state.show_3d:
    st.divider()
    st.subheader("Giao diện 3D (phụ)")
    st.caption("Nếu bị lỗi trên điện thoại thì tắt toggle — chơi bằng nút Streamlit vẫn được.")
    game_path = Path(__file__).resolve().parent / "steal_an_egg.html"
    if game_path.exists():
        components.html(game_path.read_text(encoding="utf-8"), height=520, scrolling=False)
    else:
        st.warning("Không tìm thấy steal_an_egg.html")
