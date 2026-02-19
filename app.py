import streamlit as st
import base64
from user import AdolescentUser
from quest_engine import load_quests, get_current_quest
from reflection import apply_reflection

def apply_pixel_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    html, body, .stApp {
        background-color: #0d0d1a !important;
        font-family: 'Press Start 2P', monospace !important;
        color: white !important;
    }

    h1 {
        font-family: 'Press Start 2P', monospace !important;
        color: #cc44ff !important;
        font-size: 20px !important;
        text-shadow: 3px 3px #4a0e8f;
        margin-bottom: 20px !important;
    }

    p, div, label, span {
        font-family: 'Press Start 2P', monospace !important;
        color: white !important;
        font-size: 10px !important;
        line-height: 2 !important;
    }

    .quest-box {
        background-color: #1a1a2e;
        border: 3px solid #cc44ff;
        padding: 20px 25px;
        margin: 15px 0px 25px 0px;
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        color: white;
        line-height: 2;
        box-shadow: 4px 4px #4a0e8f;
    }

    .skill-tag {
        display: inline-block;
        background-color: #4a0e8f;
        color: #ffdd57 !important;
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        padding: 4px 10px;
        margin-bottom: 15px;
        border: 1px solid #ffdd57;
    }

    .stButton button {
        background-color: #1a1a2e !important;
        border: 3px solid #cc44ff !important;
        border-radius: 0px !important;
        color: white !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 9px !important;
        padding: 12px 20px !important;
        width: 100% !important;
        text-align: left !important;
        box-shadow: 3px 3px #4a0e8f !important;
        margin-bottom: 8px !important;
        transition: all 0.1s !important;
    }

    .stButton button:hover {
        background-color: #4a0e8f !important;
        border-color: #ffdd57 !important;
        color: #ffdd57 !important;
        box-shadow: 3px 3px #ffdd57 !important;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: #1a1a2e !important;
        color: white !important;
        border: 2px solid #cc44ff !important;
        border-radius: 0px !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 9px !important;
    }

    .stSuccess > div {
        background-color: #1a1a2e !important;
        border: 2px solid #cc44ff !important;
        border-radius: 0px !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 9px !important;
        color: white !important;
    }

    .progress-bar {
        background-color: #1a1a2e;
        border: 2px solid #cc44ff;
        height: 16px;
        width: 100%;
        margin-bottom: 20px;
    }

    .progress-fill {
        background-color: #cc44ff;
        height: 100%;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 40px !important;
        max-width: 750px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def set_background():
    mode = "dark" if st.session_state.dark_mode else "light"
    max_index = 3 if st.session_state.dark_mode else 4
    index = (st.session_state.bg_index % max_index) + 1
    image_path = f"assets/{mode}_{index}.png"

    try:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        bg_color = "#0d0d1a" if st.session_state.dark_mode else "#f0f0ff"

        st.markdown(f"""
        <style>
        @keyframes scrollBg {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: repeat-x;
            background-color: {bg_color};
            animation: scrollBg 30s ease infinite;
        }}
        </style>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Background image not found: {image_path}")

# --- Session State ---
if "user" not in st.session_state:
    st.session_state.user = None
if "quests" not in st.session_state:
    st.session_state.quests = load_quests()
if "page" not in st.session_state:
    st.session_state.page = "login"
if "quest_number" not in st.session_state:
    st.session_state.quest_number = 1
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "bg_index" not in st.session_state:
    st.session_state.bg_index = 0

if st.session_state.user is not None:
    with st.sidebar:
        st.write(f"👤 {st.session_state.user.username}")
        st.write(f"⚡ Level {st.session_state.user.level} | {st.session_state.user.xp} XP")
        st.write("---")

        # Dark/Light mode toggle
        mode_label = "☀️ Light Mode" if st.session_state.dark_mode else "🌙 Dark Mode"
        if st.button(mode_label):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.session_state.bg_index = 0
            st.rerun()

        # Background cycling
        if st.button("🎨 Change Background"):
            max_bg = 3 if st.session_state.dark_mode else 4
            st.session_state.bg_index = (st.session_state.bg_index + 1) % max_bg
            st.rerun()
            
apply_pixel_style()
set_background()      

if st.session_state.user is not None:

    with st.sidebar:
        st.markdown(f"👤 {st.session_state.user.username}")
        st.markdown(f"⚡ {st.session_state.user.xp} XP")
        st.markdown(f"🏆 LVL {st.session_state.user.level}")

# --- Login Page ---
if st.session_state.page == "login":
    st.markdown("<h1>⚔️ SKILL-UP</h1>", unsafe_allow_html=True)
    st.markdown('<div class="quest-box">Welcome, adventurer. Your journey to master the 12 life skills begins now.</div>', unsafe_allow_html=True)
    username = st.text_input("Enter your name:")
    if st.button("▶ START GAME") and username:
        st.session_state.user = AdolescentUser(username)
        st.session_state.page = "quest"
        st.rerun()

# --- Quest Page ---
elif st.session_state.page == "quest":
    user = st.session_state.user
    quests = st.session_state.quests
    quest = get_current_quest(quests, user.current_quest_id)

    if quest is None or user.current_quest_id == "end":
        st.session_state.page = "reflection"
        st.rerun()
    else:
        # Header row
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("<h1>📖 QUEST</h1>", unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="text-align:right; font-family: Press Start 2P; font-size:9px; color:#ffdd57; padding-top:20px;">⚡ {user.xp} XP<br>LVL {user.level}</div>', unsafe_allow_html=True)

        # Quest number tag
        st.markdown(f'<div class="skill-tag">QUEST {st.session_state.quest_number}</div>', unsafe_allow_html=True)

        # Dialogue box
        st.markdown(f'<div class="quest-box">💬 &nbsp; {quest["text"]}</div>', unsafe_allow_html=True)

        # Choice label
        st.markdown('<p style="color:#cc44ff; font-size:9px;">▼ CHOOSE YOUR ACTION</p>', unsafe_allow_html=True)

        # Choice buttons
        for i, option in enumerate(quest["options"]):
            if st.button(f"{'🅐' if i == 0 else '🅑'}  {option['text']}", key=f"opt_{i}"):
                user.adjust_skill(option["skill"], option["impact"])
                user.add_xp(10)
                user.set_quest(option["next_id"])
                st.session_state.quest_number += 1
                st.rerun()

# --- Reflection Page ---
elif st.session_state.page == "reflection":
    user = st.session_state.user
    st.markdown("<h1>📝 REFLECTION</h1>", unsafe_allow_html=True)
    st.markdown('<div class="quest-box">💬 &nbsp; You have completed today\'s quests. Take a moment to reflect on your day. What happened? How did you handle it?</div>', unsafe_allow_html=True)

    reflection_text = st.text_area("Write your reflection here...")

    if st.button("▶ SUBMIT") and reflection_text:
        if "reflection_result" not in st.session_state:
            result = apply_reflection(user, reflection_text)
            st.session_state.reflection_result = result

    if "reflection_result" in st.session_state:
        result = st.session_state.reflection_result
        st.success(f"✨ Your {result['skill']} skill was updated!")
        if st.button("▶ SEE MY SKILLS"):
            del st.session_state.reflection_result
            st.session_state.page = "skills"
            st.rerun()

# --- Skills Page ---
elif st.session_state.page == "skills":
    import matplotlib.pyplot as plt
    import numpy as np

    user = st.session_state.user
    st.markdown(f"<h1>🏆 {user.username.upper()}</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="skill-tag">⚡ LEVEL {user.level}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="skill-tag">✨ {user.xp} XP</div>', unsafe_allow_html=True)

    skills = list(user.skills.keys())
    values = list(user.skills.values())

    N = len(skills)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='#cc44ff', alpha=0.4)
    ax.plot(angles, values, color='#cc44ff', linewidth=2)
    ax.scatter(angles[:-1], values[:-1], color='#ffdd57', s=50, zorder=5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(skills, size=7, color='white')
    ax.set_ylim(0, 1)
    ax.set_facecolor("#0d0d1a")
    fig.patch.set_facecolor("#0d0d1a")
    ax.tick_params(colors='white')
    for ring in [0.2, 0.4, 0.6, 0.8, 1.0]:
        ax.plot(angles, [ring] * (N + 1), color="#2a2a4a", linewidth=0.8, linestyle="--")
    ax.grid(False)
    ax.spines['polar'].set_visible(False)

    st.pyplot(fig)

    if st.button("▶ PLAY AGAIN"):
        st.session_state.user.current_quest_id = "prologue_01"
        st.session_state.quest_number = 1
        st.session_state.page = "quest"
        st.rerun()