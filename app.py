import streamlit as st
import base64
import re
from user import AdolescentUser
from quest_engine import load_quests, get_current_quest
from reflection import apply_reflection

# --- Security Helpers ---
def sanitize_username(username):
    # Only allow letters, numbers, spaces, hyphens — no scripts or injections
    return re.sub(r'[^a-zA-Z0-9 \-_]', '', username).strip()[:20]

def rate_limit_reflection():
    # Prevent spam — max 10 reflections per session
    count = st.session_state.get("reflection_count", 0)
    if count >= 10:
        st.error("⚠️ Maximum reflections reached for this session.")
        st.stop()
    st.session_state["reflection_count"] = count + 1

def check_input_length(text, max_chars=500):
    # Prevent extremely long inputs being sent to AI
    return text[:max_chars]

def block_suspicious_input(text):
    # Block prompt injection attempts
    banned = ["ignore previous", "system prompt", "jailbreak", "forget instructions", "act as"]
    text_lower = text.lower()
    return any(b in text_lower for b in banned)

def get_encoded_image(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

def apply_pixel_style():
    text_color = "#0d0d1a" if not st.session_state.get("dark_mode", True) else "white"
    box_bg = "rgba(240,240,255,0.85)" if not st.session_state.get("dark_mode", True) else "rgba(26,26,46,0.85)"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    html, body, .stApp {{
        font-family: 'Press Start 2P', monospace !important;
        color: {text_color} !important;
    }}

    h1 {{
        font-family: 'Press Start 2P', monospace !important;
        color: #cc44ff !important;
        font-size: 20px !important;
        text-shadow: 3px 3px #4a0e8f;
        margin-bottom: 20px !important;
    }}

    p, div, label, span {{
        font-family: 'Press Start 2P', monospace !important;
        color: {text_color} !important;
        font-size: 10px !important;
        line-height: 2 !important;
    }}

    .quest-box {{
        background-color: {box_bg};
        border: 3px solid #cc44ff;
        padding: 20px 25px;
        margin: 15px 0px 25px 0px;
        font-family: 'Press Start 2P', monospace;
        font-size: 10px;
        color: {text_color};
        line-height: 2;
        box-shadow: 4px 4px #4a0e8f;
    }}

    .skill-tag {{
        display: inline-block;
        background-color: #4a0e8f;
        color: #ffdd57 !important;
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        padding: 4px 10px;
        margin-bottom: 15px;
        border: 1px solid #ffdd57;
    }}

    .stButton button {{
        background-color: {box_bg} !important;
        border: 3px solid #cc44ff !important;
        border-radius: 0px !important;
        color: {text_color} !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 9px !important;
        padding: 12px 20px !important;
        width: 100% !important;
        text-align: left !important;
        box-shadow: 3px 3px #4a0e8f !important;
        margin-bottom: 8px !important;
        transition: all 0.1s !important;
    }}

    .stButton button:hover {{
        background-color: #4a0e8f !important;
        border-color: #ffdd57 !important;
        color: #ffdd57 !important;
        box-shadow: 3px 3px #ffdd57 !important;
    }}

    .stTextInput input, .stTextArea textarea {{
        background-color: {box_bg} !important;
        color: {text_color} !important;
        border: 2px solid #cc44ff !important;
        border-radius: 0px !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 9px !important;
    }}

    #MainMenu {{visibility: visible;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    .block-container {{
        padding-top: 40px !important;
        max-width: 750px !important;
        position: relative;
        z-index: 1;
    }}
    </style>
    """, unsafe_allow_html=True)

def set_background():
    if st.session_state.dark_mode:
        base = get_encoded_image("assets/dark_1.png")
        layer2 = get_encoded_image("assets/dark_2.png")
        layer3 = get_encoded_image("assets/dark_3.png")
        layer4 = None
        bg_color = "#0d0d1a"
    else:
        base = get_encoded_image("assets/light_1.png")
        layer2 = get_encoded_image("assets/light_2.png")
        layer3 = get_encoded_image("assets/light_3.png")
        layer4 = get_encoded_image("assets/light_4.png")
        bg_color = "#e8e8ff"

    if not base:
        return

    layers_css = ""

    if layer2:
        layers_css += f"""
        .bg-layer2 {{
            position: fixed; top: 0; left: 0;
            width: 200%; height: 100%;
            background-image: url("data:image/png;base64,{layer2}");
            background-repeat: repeat-x;
            background-size: auto 100%;
            animation: scrollLayer2 60s linear infinite;
            z-index: 0; opacity: 0.9;
        }}
        @keyframes scrollLayer2 {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}
        """

    if layer3:
        layers_css += f"""
        .bg-layer3 {{
            position: fixed; top: 0; left: 0;
            width: 200%; height: 100%;
            background-image: url("data:image/png;base64,{layer3}");
            background-repeat: repeat-x;
            background-size: auto 100%;
            animation: scrollLayer3 40s linear infinite;
            z-index: 0; opacity: 0.8;
        }}
        @keyframes scrollLayer3 {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}
        """

    if layer4:
        layers_css += f"""
        .bg-layer4 {{
            position: fixed; top: 0; left: 0;
            width: 200%; height: 100%;
            background-image: url("data:image/png;base64,{layer4}");
            background-repeat: repeat-x;
            background-size: auto 100%;
            animation: scrollLayer4 25s linear infinite;
            z-index: 0; opacity: 0.7;
        }}
        @keyframes scrollLayer4 {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}
        """

    mode_key = "dark" if st.session_state.dark_mode else "light"

    st.markdown(f"""
    <style>
    /* mode: {mode_key} */
    .stApp {{
        background-image: url("data:image/png;base64,{base}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-color: {bg_color};
    }}
    {layers_css}
    </style>
    <!-- mode: {mode_key} -->
    {"<div class='bg-layer2'></div>" if layer2 else ""}
    {"<div class='bg-layer3'></div>" if layer3 else ""}
    {"<div class='bg-layer4'></div>" if layer4 else ""}
    """, unsafe_allow_html=True)

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
if "reflection_count" not in st.session_state:
    st.session_state.reflection_count = 0

apply_pixel_style()
set_background()
st.session_state["bg_render_key"] = "dark" if st.session_state.dark_mode else "light"

# --- Sidebar ---
if st.session_state.user is not None:
    with st.sidebar:
        st.write(f"👤 {st.session_state.user.username}")
        st.write(f"⚡ Level {st.session_state.user.level} | {st.session_state.user.xp} XP")
        st.write("---")
        mode_label = "☀️ Light Mode" if st.session_state.dark_mode else "🌙 Dark Mode"
        if st.button(mode_label):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.session_state.bg_index = 0
            st.rerun()

# --- Login Page ---
if st.session_state.page == "login":
    st.markdown("<h1>⚔️ SKILL-UP</h1>", unsafe_allow_html=True)
    st.markdown('<div class="quest-box">Welcome, adventurer. Your journey to master the 12 life skills begins now.</div>', unsafe_allow_html=True)
    username = st.text_input("Enter your name:", max_chars=20)
    if st.button("▶ START GAME") and username:
        clean_username = sanitize_username(username)
        if not clean_username:
            st.error("⚠️ Please enter a valid name (letters and numbers only).")
        else:
            st.session_state.user = AdolescentUser(clean_username)
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
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("<h1>📖 QUEST</h1>", unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="text-align:right; font-family: Press Start 2P; font-size:9px; color:#ffdd57; padding-top:20px;">⚡ {user.xp} XP<br>LVL {user.level}</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="skill-tag">QUEST {st.session_state.quest_number}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="quest-box">💬 &nbsp; {quest["text"]}</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#cc44ff; font-size:9px;">▼ CHOOSE YOUR ACTION</p>', unsafe_allow_html=True)

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

    reflection_text = st.text_area("Write your reflection here...", max_chars=500)

    if st.button("▶ SUBMIT") and reflection_text:
        if block_suspicious_input(reflection_text):
            st.error("⚠️ Invalid input detected. Please write about your day normally.")
        elif "reflection_result" not in st.session_state:
            rate_limit_reflection()
            clean_text = check_input_length(reflection_text)
            result = apply_reflection(user, clean_text)
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