import streamlit as st
import random
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="For My Anjuuu 💙", layout="centered")

# ---------- CUSTOM STYLES ----------
page_bg = """
<style>
body {
    background: linear-gradient(135deg, #c2e9fb, #a1c4fd);
    background-attachment: fixed;
    font-family: 'Poppins', sans-serif;
    color: #1e3a8a;
}
h1, h2, h3 {
    text-align: center;
    color: #1e3a8a;
}
.block-container {
    padding-top: 2rem;
}
.stButton>button {
    background-color: #60a5fa;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 0.5rem 1.5rem;
    font-size: 1rem;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #2563eb;
    transform: scale(1.05);
}
.card {
    background: rgba(255, 255, 255, 0.7);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}
.heart-bg {
    background-image: url('https://i.imgur.com/5y7Yl5r.png');
    background-size: 100px;
    background-repeat: repeat;
    opacity: 0.1;
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    z-index: -1;
}
</style>
<div class='heart-bg'></div>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ---------- PASSCODE PAGE ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def passcode_page():
    st.title("💌 For My Anjuuu 💙")
    st.write("Enter the secret code, my love 💫")
    passcode = st.text_input("🔒 Enter Passcode", type="password")
    if st.button("Unlock"):
        if passcode == "Iloveyouladuu":
            st.session_state.authenticated = True
            st.success("Welcome, my love 💙")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Oops! That’s not the right code 😔")

# ---------- MAIN APP CONTENT ----------
def main_app():
    st.title("💞 For My Anjuuu 💞")
    st.write("Welcome to your special place, love 💙")

    menu = st.radio(
        "Choose what you want to open 💫",
        ["Today's Thought", "Click Only If You Miss Me", "Our Songs", "Spin the Wheel of Love", "Reasons I Love You"]
    )

    # --- Today’s Thought ---
    if menu == "Today's Thought":
        st.subheader("💭 Today's Thought")
        thought = st.text_area("Write your note here (for him 💙):")
        if st.button("Save Thought"):
            st.success("Saved successfully! 💌")

    # --- Click Only If You Miss Me ---
    elif menu == "Click Only If You Miss Me":
        st.subheader("💫 A Little Surprise 💫")
        if st.button("Reveal 💙"):
            st.write("“You’re my calm in the chaos, my favorite reason to smile.” 💞")

    # --- Our Songs ---
    elif menu == "Our Songs":
        st.subheader("🎵 Our Songs Playlist 💙")
        songs = [
            ("Perfect - Ed Sheeran", "Because it’s literally us 💫"),
            ("Until I Found You - Stephen Sanchez", "Because that’s exactly how I feel."),
            ("Love Story - Taylor Swift", "Because we write our own story 💙")
        ]
        for title, reason in songs:
            with st.container():
                st.markdown(f"**{title}** — *{reason}*")

    # --- Spin the Wheel of Love ---
    elif menu == "Spin the Wheel of Love":
        st.subheader("🎡 Spin the Wheel of Love 💙")
        options = [
            "You get a hug! 🤗", "Movie night! 🎬", "You owe me ice cream 🍦",
            "Midnight call 💞", "A long drive date 🚗", "You get 10 kisses 😘"
        ]
        if st.button("Spin 🎡"):
            with st.spinner("Spinning..."):
                time.sleep(2)
            result = random.choice(options)
            st.success(result)

    # --- Reasons I Love You ---
    elif menu == "Reasons I Love You":
        st.subheader("💙 Reasons Why I Love You 💙")
        reasons = [
            "I love your personality",
            "I love your smile",
            "I love your hair",
            "I love your smell",
            "I love your jolliness",
            "I love your maturity",
            "I love your childishness",
            "I love the way you balance",
            "I love your futuristic vision",
            "I love the way I am happy around you",
            "I love the way I am safe around you",
            "I love that you communicate",
            "I love that you try to solve things",
            "I love that you are emotionally available",
            "I love your humour",
            "I love your eyes",
            "I love the way you listen",
            "I love that you remember details",
            "I love the sense of security you give",
            "I love your confidence",
            "I love your nature",
            "I love the small gestures",
            "I love your intelligence",
            "I love your positive approach towards life",
            "I love your dressing sense",
            "I love that you never give up",
            "I love how you respect others",
            "I love your humanity",
            "I love how you understand",
            "I love that family matters to you",
            "I love your selflessness",
            "I love that you cry",
            "I love your anger",
            "I love your dance",
            "I love your general knowledge",
            "I love that you love deeply",
            "I love that you believe in God",
            "I love that you learn",
            "I love how you manage",
            "I love that you are foodie",
            "I love your courage",
            "I love your boundaries",
            "I love your control",
            "I love your thoughtfulness",
            "I love how you complete me",
            "I love the way you say 'meri laduuu'",
            "I love the way you teach me",
            "I love the priority you give",
            "I love the support you give",
            "I love how you make me laugh",
            "I love the way you love me",
            "I love our friendship",
            "And most importantly, I love you 💙"
        ]
        for r in reasons:
            st.markdown(f"💖 {r}")

# ---------- RUN ----------
if not st.session_state.authenticated:
    passcode_page()
else:
    main_app()
