# app.py
import streamlit as st
import json, random
from datetime import datetime
from pathlib import Path

# ---------- BASIC CONFIG ----------
st.set_page_config(page_title="For My Anjuuu 💙", page_icon="🫀", layout="wide")

PASSCODE = "Iloveyouladuu"

# ---------- SESSION STATE ----------
if "auth" not in st.session_state:
    st.session_state.auth = False
if "passcode_input" not in st.session_state:
    st.session_state.passcode_input = ""

# ---------- DATA & FOLDERS ----------
DATA_DIR = Path("data")
PHOTOS_DIR = DATA_DIR / "photos"
DATA_DIR.mkdir(exist_ok=True)
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

def ensure_json(filename, default):
    p = DATA_DIR / filename
    if not p.exists():
        with open(p, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=2)

ensure_json("notes.json", [])
ensure_json("songs.json", [])
ensure_json("timeline.json", [])

# ---------- CSS + BEAUTIFUL FLOATING HEARTS ----------
st.markdown("""
<style>
.stApp { background: linear-gradient(180deg,#04133a 0%, #082a5f 45%, #0d3b7a 100%); color:#eaf4ff; font-family:-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial; overflow-x:hidden;}
.card { background: rgba(255,255,255,0.03); border-radius:12px; padding:18px; margin-bottom:12px; box-shadow:0 6px 30px rgba(2,10,40,0.4); border:1px solid rgba(255,255,255,0.04);}
h1,h2,h3 { color:#e9f6ff; }
.polaroid { background:#fff; padding:12px 12px 20px 12px; display:inline-block; margin:10px; border-radius:8px; box-shadow:0 8px 30px rgba(2,8,30,0.45); transform:rotate(-1deg);}
.polaroid img { width:220px; height:160px; object-fit:cover; border-radius:6px; display:block; margin-bottom:8px;}
.polaroid .caption { color:#0e2340; font-weight:600; font-size:14px; text-align:center; }
.stButton>button { background: linear-gradient(90deg,#66aaff,#3b7df0); color:white; border:none; padding:10px 14px; border-radius:10px; font-weight:600;}
.small-muted { color:#cfe9ff; font-size:13px; opacity:0.9; }
.section { padding:14px; margin-bottom:14px; border-radius:10px; }

/* Beautiful floating blue hearts */
@keyframes floatUp {
    0% {transform: translateY(0) rotate(0deg); opacity:1;}
    100% {transform: translateY(-800px) rotate(360deg); opacity:0;}
}
.floating-heart {
    position: absolute;
    background-color: #66aaff;
    clip-path: polygon(50% 0%, 61% 12%, 75% 12%, 88% 25%, 88% 38%, 75% 50%, 50% 80%, 25% 50%, 12% 38%, 12% 25%, 25% 12%, 39% 12%);
    border-radius:5px;
    pointer-events:none;
    animation-name: floatUp;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}
</style>

<script>
function createHeart(){
    let heart = document.createElement("div");
    heart.className = "floating-heart";
    heart.style.left = Math.random() * window.innerWidth + "px";
    let size = 10 + Math.random()*20;
    heart.style.width = size + "px";
    heart.style.height = size + "px";
    heart.style.top = window.innerHeight + "px";
    heart.style.animationDuration = 3 + Math.random()*4 + "s";
    document.body.appendChild(heart);
    setTimeout(()=>{heart.remove()}, 7000);
}
setInterval(createHeart, 400);
</script>
""", unsafe_allow_html=True)

# ---------- PASSCODE PAGE ----------
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; margin-top:60px;'>A little world — just for you 🫀</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; margin-bottom:24px;'>Enter the secret passcode to unlock our private space</h4>", unsafe_allow_html=True)
    st.session_state.passcode_input = st.text_input("Passcode", type="password")
    
    if st.button("Unlock 💙"):
        if st.session_state.passcode_input == PASSCODE:
            st.session_state.auth = True
            st.experimental_rerun()  # Safe inside button click
        else:
            st.error("Wrong passcode 💫")
    st.stop()  # stop rendering the rest of the app until correct

# ---------- NAVIGATION ----------
st.sidebar.title("💫 Navigate")
page = st.sidebar.radio("", [
    "Home 🏠",
    "Today's Thought 💭",
    "Click if you miss me 💞",
    "Our Songs 🎶",
    "Spin the Wheel 💕",
    "Reasons I Love You 💌",
    "Photos & Polaroids 📸",
    "Our Story Timeline 🕰️",
    "Settings ⚙️"
])

# ---------- PAGES ----------
# (The rest of your pages remain the same as previous code, including all 54 reasons,
#  Today's Thought, Click if you miss me, Spin the Wheel, Photos, Timeline, Settings)

