import streamlit as st
from user import AdolescentUser
from quest_engine import load_quests, get_current_quest
from reflection import apply_reflection

# --- Session State (keeps user alive across pages) ---
if "user" not in st.session_state:
    st.session_state.user = None
if "quests" not in st.session_state:
    st.session_state.quests = load_quests()
if "page" not in st.session_state:
    st.session_state.page = "login"

# --- Login Page ---
if st.session_state.page == "login":
    st.title("⚔️ Skill-UP")
    st.subheader("Begin your journey")
    username = st.text_input("Enter your name:")
    if st.button("Start") and username:
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

    st.title(f"📖 Quest")
    st.write(quest["text"])
    st.write("---")

    for option in quest["options"]:
        if st.button(option["text"]):
            user.adjust_skill(option["skill"], option["impact"])
            user.set_quest(option["next_id"])
            st.rerun()
            # --- Reflection Page ---
elif st.session_state.page == "reflection":
    user = st.session_state.user
    st.title("📝 Daily Reflection")
    st.write("Tell us about your day:")
    reflection_text = st.text_area("What happened today?")

    if st.button("Submit Reflection") and reflection_text:
        with st.spinner("Analysing your reflection..."):
            result = apply_reflection(user, reflection_text)
        st.success(f"Your **{result['skill']}** skill was updated!")
        if st.button("See My Skills"):
            st.session_state.page = "skills"
            st.rerun()
            # --- Skills Page ---
elif st.session_state.page == "skills":
    import matplotlib.pyplot as plt
    import numpy as np

    user = st.session_state.user
    st.title(f"🏆 {user.username}'s Skills")

    skills = list(user.skills.keys())
    values = list(user.skills.values())

    # Radar chart setup
    N = len(skills)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='mediumpurple', alpha=0.4)
    ax.plot(angles, values, color='mediumpurple', linewidth=2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(skills, size=7)
    ax.set_ylim(0, 1)
    ax.set_facecolor("#0e0e0e")
    fig.patch.set_facecolor("#0e0e0e")
    ax.tick_params(colors='white')

    st.pyplot(fig)

    if st.button("Play Again"):
        st.session_state.user.current_quest_id = "prologue_01"
        st.session_state.page = "quest"
        st.rerun()