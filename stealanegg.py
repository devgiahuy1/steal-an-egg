import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Steal An Egg Helper",
    page_icon="🥚",
    layout="wide"
)

st.title("🥚 Steal An Egg Helper Tool")
st.caption("Công cụ hỗ trợ người chơi Steal An Egg trên Roblox")

# ====================== DATA ======================
biomes = {
    "Forest": {"speed": 0, "guardian": "Chicken"},
    "Lake": {"speed": 900, "guardian": "Swan"},
    "Desert": {"speed": 10000, "guardian": "Scorpion"},
    "Jungle": {"speed": 40000, "guardian": "Tiger"},
    "Snow": {"speed": 170000, "guardian": "Yeti"},
    "Volcano": {"speed": 700000, "guardian": "Cerberus"},
    "Abyss Ocean": {"speed": 2500000, "guardian": "Moby"},
    "Prehistoric": {"speed": 18000000, "guardian": "T-Rex"},
    "Cosmic": {"speed": 700000000, "guardian": "Cosmic Skeleton"},
    "Cherry Blossom": {"speed": 2500000000, "guardian": "Oni Tiger"},
    "Titan Temple": {"speed": 7000000000, "guardian": "Gorilla King"},
    "Angels & Demons": {"speed": 20000000000, "guardian": "ArchAngel / World Burner"},
}

pets = [
    {"name": "Chicken", "biome": "Forest", "rarity": "Common", "income": 1},
    {"name": "Frog", "biome": "Lake", "rarity": "Common", "income": 3},
    {"name": "Jerboa", "biome": "Desert", "rarity": "Common", "income": 8},
    {"name": "T-Rex", "biome": "Prehistoric", "rarity": "Legendary", "income": 89121},
    {"name": "Unicorn", "biome": "Cosmic", "rarity": "Divine", "income": 1000000000},
    {"name": "Kitsune", "biome": "Cherry Blossom", "rarity": "Divine", "income": 1800000000},
    {"name": "Nightflame", "biome": "Titan Temple", "rarity": "Divine", "income": 3000000000},
    {"name": "Spirit World Guardian", "biome": "Angels & Demons", "rarity": "Eternal", "income": 26000000000},
]

# ====================== SIDEBAR ======================
st.sidebar.header("⚙️ Cài đặt")
player_speed = st.sidebar.number_input("Speed hiện tại của bạn", min_value=0, value=10000, step=1000)

# ====================== TAB ======================
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Biomes", "🐣 Pets", "🧮 Máy tính thu nhập", "🎨 Tạo Prompt Ảnh"])

# ---------- TAB 1: BIOMES ----------
with tab1:
    st.subheader("Danh sách Biomes & Speed yêu cầu")

    biome_data = []
    for name, info in biomes.items():
        can_enter = "✅ Có thể vào" if player_speed >= info["speed"] else "❌ Chưa đủ Speed"
        biome_data.append({
            "Biome": name,
            "Speed cần": f"{info['speed']:,}",
            "Guardian": info["guardian"],
            "Trạng thái": can_enter
        })

    df_biome = pd.DataFrame(biome_data)
    st.dataframe(df_biome, use_container_width=True, hide_index=True)

# ---------- TAB 2: PETS ----------
with tab2:
    st.subheader("Một số Pets nổi bật")

    df_pets = pd.DataFrame(pets)
    df_pets["Income/s"] = df_pets["income"].apply(lambda x: f"${x:,}")
    st.dataframe(df_pets[["name", "biome", "rarity", "Income/s"]], use_container_width=True, hide_index=True)

# ---------- TAB 3: CALCULATOR ----------
with tab3:
    st.subheader("Máy tính thu nhập từ Pets")

    selected_pets = st.multiselect(
        "Chọn pets bạn đang sở hữu",
        options=[p["name"] for p in pets],
        default=["T-Rex"]
    )

    total_income = 0
    for pet in pets:
        if pet["name"] in selected_pets:
            total_income += pet["income"]

    st.metric("Tổng thu nhập mỗi giây", f"${total_income:,}")
    st.metric("Thu nhập mỗi giờ", f"${total_income * 3600:,}")
    st.metric("Thu nhập mỗi ngày", f"${total_income * 86400:,}")

# ---------- TAB 4: PROMPT GENERATOR ----------
with tab4:
    st.subheader("Tạo Prompt ảnh Steal An Egg")

    egg_name = st.text_input("Tên trứng / Pet", value="TREX EGG")
    income_text = st.text_input("Giá trị thu nhập", value="$89,121Sp/s")
    character_desc = st.text_input("Mô tả nhân vật", value="Roblox avatar with orange hair, blue hoodie")
    background = st.selectbox("Background", ["Desert", "Forest", "Volcano", "Cosmic", "Snow"])

    if st.button("Tạo Prompt", type="primary"):
        prompt = f"""A vibrant Roblox-style 3D cartoon scene from the game "Steal An Egg", bright {background.lower()} biome background. On the left, a large blocky dinosaur looking surprised with red exclamation marks. On the right, a {character_desc}, dramatically lifting a giant shiny egg covered in golden hexagonal scales above their head. Bold colorful text above says "{egg_name}" in rainbow gradient letters, with a red arrow pointing to the egg, and glowing green text "{income_text}". Bright lighting, high contrast, clean Roblox aesthetic, exaggerated proportions, fun and energetic composition, thumbnail style."""
        
        st.code(prompt, language="text")
        st.success("Đã tạo prompt! Copy và dán vào AI tạo ảnh.")

st.markdown("---")
st.caption("Tool không chính thức • Dữ liệu mang tính tham khảo")
