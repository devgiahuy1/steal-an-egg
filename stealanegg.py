import streamlit as st
import random
import time

st.set_page_config(page_title="Steal An Egg", page_icon="🥚", layout="centered")

# ====================== KHỞI TẠO ======================
if "speed" not in st.session_state:
    st.session_state.speed = 5000
    st.session_state.money = 0
    st.session_state.pets = []
    st.session_state.message = "Chào mừng đến Steal An Egg!"
    st.session_state.egg = None
    st.session_state.carrying = False
    st.session_state.location = "Base"

# ====================== DỮ LIỆU ======================
biomes = {
    "Forest": {"speed_need": 0, "eggs": ["Chicken Egg", "Dog Egg"], "reward": (1, 5)},
    "Lake": {"speed_need": 900, "eggs": ["Frog Egg", "Duck Egg"], "reward": (5, 15)},
    "Desert": {"speed_need": 10000, "eggs": ["Jerboa Egg", "Scorpion Egg"], "reward": (20, 50)},
    "Prehistoric": {"speed_need": 18000000, "eggs": ["T-Rex Egg"], "reward": (80000, 120000)},
}

# ====================== GIAO DIỆN ======================
st.title("🥚 Steal An Egg")
st.caption("Phiên bản mini bằng Streamlit")

col1, col2, col3 = st.columns(3)
col1.metric("⚡ Speed", f"{st.session_state.speed:,}")
col2.metric("💰 Money", f"${st.session_state.money:,}")
col3.metric("🐣 Số Pet", len(st.session_state.pets))

st.markdown(f"**Vị trí hiện tại:** `{st.session_state.location}`")
st.info(st.session_state.message)

st.divider()

# ====================== CHỨC NĂNG ======================
tab1, tab2, tab3 = st.tabs(["🏃 Hành động", "🗺️ Biomes", "🐣 Pets của bạn"])

with tab1:
    st.subheader("Hành động")

    # Tập luyện
    if st.button("🏋️ Tập Treadmill (+Speed)", use_container_width=True):
        gain = random.randint(200, 800)
        st.session_state.speed += gain
        st.session_state.message = f"Bạn tập treadmill và được +{gain} Speed!"
        st.rerun()

    # Quay về base
    if st.session_state.location != "Base":
        if st.button("🏠 Chạy về Base", use_container_width=True):
            if st.session_state.carrying:
                # Thành công mang trứng về
                egg_name = st.session_state.egg
                income = random.randint(*biomes[st.session_state.location]["reward"])
                st.session_state.pets.append({"name": egg_name, "income": income})
                st.session_state.money += income * 10
                st.session_state.message = f"Bạn đã mang {egg_name} về thành công! +${income*10}"
                st.session_state.egg = None
                st.session_state.carrying = False
            else:
                st.session_state.message = "Bạn đã về Base an toàn."
            st.session_state.location = "Base"
            st.rerun()

with tab2:
    st.subheader("Chọn Biome để cướp trứng")

    for name, info in biomes.items():
        can_go = st.session_state.speed >= info["speed_need"]
        label = f"{name} (Cần {info['speed_need']:,} Speed)"
        
        if can_go:
            if st.button(f"➡️ Đi đến {name}", key=name, use_container_width=True):
                st.session_state.location = name
                st.session_state.message = f"Bạn đã đến {name}. Hãy cướp trứng!"
                st.rerun()
        else:
            st.button(f"🔒 {label}", disabled=True, use_container_width=True)

    # Cướp trứng
    if st.session_state.location in biomes and not st.session_state.carrying:
        st.divider()
        if st.button("🥚 Cướp Trứng!", type="primary", use_container_width=True):
            egg = random.choice(biomes[st.session_state.location]["eggs"])
            st.session_state.egg = egg
            st.session_state.carrying = True
            st.session_state.message = f"Bạn đã nhặt được **{egg}**! Nhanh chạy về Base trước khi bị đuổi!"
            st.rerun()

    if st.session_state.carrying:
        st.warning(f"⚠️ Bạn đang cầm: **{st.session_state.egg}** — Hãy chạy về Base ngay!")

with tab3:
    st.subheader("Pets đang sở hữu")
    if not st.session_state.pets:
        st.write("Bạn chưa có pet nào.")
    else:
        total_income = 0
        for pet in st.session_state.pets:
            st.write(f"• {pet['name']} → **${pet['income']}/s**")
            total_income += pet["income"]
        st.success(f"Tổng thu nhập: **${total_income}/s**")

        if st.button("💵 Thu hoạch tiền từ Pets"):
            earn = total_income * random.randint(5, 15)
            st.session_state.money += earn
            st.session_state.message = f"Bạn thu hoạch được ${earn:,}!"
            st.rerun()

st.divider()
if st.button("🔄 Chơi lại từ đầu", type="secondary"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
