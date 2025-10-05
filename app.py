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

# ---------- CSS + FLOATING HEARTS ----------
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

/* Floating blue hearts animation */
@keyframes floatHearts {
    0% {transform: translateY(0) scale(1); opacity:1;}
    100% {transform: translateY(-600px) scale(1.5); opacity:0;}
}
.heart {
    position: absolute;
    font-size: 24px;
    color: #66aaff;
    animation-name: floatHearts;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}
</style>

<!-- Hearts floating -->
<div class="heart" style="left:5%; animation-duration:3s;">💙</div>
<div class="heart" style="left:20%; animation-duration:4s;">💙</div>
<div class="heart" style="left:35%; animation-duration:5s;">💙</div>
<div class="heart" style="left:50%; animation-duration:4s;">💙</div>
<div class="heart" style="left:65%; animation-duration:3s;">💙</div>
<div class="heart" style="left:80%; animation-duration:5s;">💙</div>
<div class="heart" style="left:90%; animation-duration:4s;">💙</div>
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
# Home
if page == "Home 🏠":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("Welcome, my love 🫀")
    st.write("This little space is made by Mansi — for you. Explore, add, and cherish.")
    st.write("Use the menu on the left. Everything here is private and just for us.")
    st.markdown("</div>", unsafe_allow_html=True)

# Today's Thought
elif page == "Today's Thought 💭":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("💭 Today's Thought")
    st.write("Leave a note or read old thoughts. It's like a secret diary.")
    notes_file = DATA_DIR / "notes.json"
    notes = json.loads(notes_file.read_text()) if notes_file.exists() else []
    with st.form("note_form"):
        author = st.selectbox("Who is writing?", ["Him", "Me"])
        text = st.text_area("Write your thought...", height=140)
        protect = st.text_input("Optional password (keeps it private)", type="password")
        submitted = st.form_submit_button("Save Thought 💌")
        if submitted and text.strip():
            entry = {"author": author, "text": text.strip(), "date": datetime.now().isoformat(), "lock": bool(protect.strip()), "mask": protect.strip() if protect.strip() else ""}
            notes.append(entry)
            notes_file.write_text(json.dumps(notes, ensure_ascii=False, indent=2))
            st.success("Saved 💙")
    st.markdown("</div>", unsafe_allow_html=True)

# Click if you miss me
elif page == "Click if you miss me 💞":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Click only if you miss me 💞")
    st.write("A tiny surprise — voice note or message.")
    if st.button("Click only if you miss me 😘"):
        st.success("I miss you so much. Counting moments until I see you again. Always yours. 🫀")
        audio_path = Path("data/voice.mp3")
        if audio_path.exists(): st.audio(str(audio_path))
        else: st.info("No voice note uploaded yet. You can upload one in Settings.")
    st.markdown("</div>", unsafe_allow_html=True)

# Remaining pages like Songs, Spin the Wheel, Reasons, Photos, Timeline, Settings remain the same
# (Include all previous page code here, keeping floating hearts working)
