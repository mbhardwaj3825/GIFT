import streamlit as st
import random
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="For My Anjuuu 💙", page_icon="💙", layout="centered")

# --- CSS STYLING ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    background-attachment: fixed;
    color: white;
    font-family: 'Poppins', sans-serif;
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
[data-testid="stSidebar"] {background: rgba(255,255,255,0.1);}
h1, h2, h3, h4 {
    text-align: center;
    color: #dbeafe;
}
.big-heart {
    font-size: 50px;
    text-align: center;
    animation: beat 1.2s infinite;
}
@keyframes beat {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.3); }
}
.polaroid {
  background: white;
  color: black;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 2px 4px 10px rgba(0,0,0,0.2);
  text-align: center;
  width: 250px;
  margin: 10px auto;
}
.wheel {
  width: 200px;
  height: 200px;
  border: 8px solid #dbeafe;
  border-radius: 50%;
  margin: 20px auto;
  background: radial-gradient(circle at center, #93c5fd 0%, #1e3a8a 100%);
  animation: spin 3s linear infinite;
}
@keyframes spin {
  0% {transform: rotate(0deg);}
  100% {transform: rotate(360deg);}
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- PASSCODE ---
CORRECT_PASSCODE = "myblueanjubear"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def show_passcode_page():
    st.markdown("<h1>💙 For My Anjuuu 💙</h1>", unsafe_allow_html=True)
    st.markdown('<div class="big-heart">💙</div>', unsafe_allow_html=True)
    st.write("Enter the secret passcode to unlock your surprise 💫")

    passcode = st.text_input("Enter Passcode", type="password")

    if st.button("Unlock 💌"):
        if passcode == CORRECT_PASSCODE:
            st.session_state.authenticated = True
            st.success("Access Granted! 💙")
            st.session_state.page = "home"
            st.experimental_set_query_params(page="home")
        else:
            st.error("Oops! That’s not the right passcode 😢")

if not st.session_state.authenticated:
    show_passcode_page()
    st.stop()

# --- MAIN CONTENT ---
st.sidebar.title("💙 Navigation")
page = st.sidebar.radio("Go to", ["Home 🏠", "50 Reasons I Love You 💌", "Photos & Polaroids 📸"])

# --- HOME PAGE ---
if page == "Home 🏠":
    st.markdown("<h1>💙 For My Anjuuu 💙</h1>", unsafe_allow_html=True)
    st.markdown('<div class="big-heart">💙</div>', unsafe_allow_html=True)
    st.write("""
    This little corner of the internet is just for you, my love.  
    A space full of memories, smiles, and reasons why you’re my everything 💫
    """)

# --- REASONS PAGE ---
elif page == "50 Reasons I Love You 💌":
    st.markdown("<h1>💙 50 Reasons Why I Love You 💙</h1>", unsafe_allow_html=True)
    st.markdown('<div class="wheel"></div>', unsafe_allow_html=True)
    st.write("✨ The wheel spins and reveals a reason every second...")

    reasons = [
        "I love your personality", "I love your smile", "I love your hairs", "I love your smell",
        "I love your jollyness", "I love your maturity", "I love your childishness",
        "I love the way you balance", "I love your futuristic vision",
        "I love the way I am happy around you", "I love the way I am safe around you",
        "I love that you communicate", "I love that you try to solve",
        "I love that you are emotionally available", "I love your humour", "I love your eyes",
        "I love the way you listen", "I love that you remember details",
        "I love the sense of security you give", "I love your confidence", "I love your nature",
        "I love the small gestures", "I love your intelligence",
        "I love your positive approach towards life", "I love your dressing sense",
        "I love that you never think of giving up", "I love how you respect others",
        "I love your humanity", "I love how you understand", "I love that for you family matters",
        "I love that you think of 'your' people so selflessly", "I love that cry",
        "I love your anger", "I love your dance", "I love your general knowledge",
        "I love that you love", "I love that you believe in God", "I love that you learn",
        "I love how you manage", "I love that you are foodie", "I love your courage",
        "I love your boundaries", "I love your control", "I love your thoughtfulness",
        "I love how you complete me", "I love the way you say 'meri laduuu'",
        "I love the way you teach me", "I love the priority you give",
        "I love the support you give", "I love how you make me laugh",
        "I love the way you love me", "I love our friendship", "And most importantly, I love you 💙"
    ]

    for reason in reasons:
        time.sleep(1)
        st.markdown(f"<div class='polaroid'><p>{reason}</p></div>", unsafe_allow_html=True)

# --- PHOTOS PAGE ---
elif page == "Photos & Polaroids 📸":
    st.markdown("<h1>📸 Our Polaroid Wall 💙</h1>", unsafe_allow_html=True)
    st.write("Upload our pictures, and they’ll appear like little memories on the wall 💫")

    uploaded_files = st.file_uploader("Upload photos", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

    if uploaded_files:
        cols = st.columns(3)
        i = 0
        for file in uploaded_files:
            with cols[i % 3]:
                st.image(file, use_container_width=True, caption="💙 Our Memory 💙")
            i += 1
