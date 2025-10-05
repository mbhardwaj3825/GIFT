# app.py
import streamlit as st
import json, os, random
from datetime import datetime, date
from pathlib import Path

# ---------- BASIC CONFIG ----------
st.set_page_config(page_title="For My Anjuuu 💙", page_icon="🫀", layout="wide")

PASSCODE = "Iloveyouladuu"

# ---------- AUTH ----------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # Entry screen
    st.markdown(
        """
        <style>
        .title { font-size:42px; font-weight:600; color:#e6f0ff; text-shadow: 0 2px 8px rgba(0,0,0,0.25); text-align:center; margin-top:60px; }
        .subtitle { font-size:18px; color:#d6eaff; text-align:center; margin-bottom: 24px; }
        input { background: rgba(255,255,255,0.06); border-radius: 10px; padding:10px; color: #e6f7ff; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='title'>A little world — just for you 🫀</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Enter the secret passcode to unlock our private space</div>", unsafe_allow_html=True)

    # Floating hearts CSS/HTML
    st.markdown(
        """
        <style>
        .heart { position: fixed; width: 28px; height: 28px; background: radial-gradient(circle at 30% 30%, #a8d1ff 0%, #5aa0ff 40%, #2b7be6 100%); transform: rotate(-45deg); border-radius:6px; box-shadow: 0 6px 18px rgba(43,123,230,0.25); }
        .heart:before, .heart:after { content: ""; position: absolute; width: 28px; height: 28px; background: radial-gradient(circle at 30% 30%, #a8d1ff 0%, #5aa0ff 40%, #2b7be6 100%); border-radius: 50%; }
        .heart:before { top:-14px; left:0; } .heart:after { left:14px; top:0; }
        @keyframes floaty { 0% { transform: translateY(0) rotate(-10deg); opacity:0.8; } 50% { transform: translateY(-20px) rotate(10deg); opacity:1; } 100% { transform: translateY(0) rotate(-10deg); opacity:0.8; } }
        .h1 { animation: floaty 5s ease-in-out infinite; left:10%; top:10%; }
        .h2 { animation: floaty 6s ease-in-out infinite; left:80%; top:30%; width:22px; height:22px; }
        .h3 { animation: floaty 7s ease-in-out infinite; left:50%; top:5%; width:20px; height:20px; }
        .anat { position: fixed; right:6%; top:18%; width:46px; height:46px; opacity:0.95; transform: rotate(0deg); animation: floaty 7s ease-in-out infinite; }
        </style>
        <div class="heart h1"></div>
        <div class="heart h2"></div>
        <div class="heart h3"></div>
        <svg class="anat" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
          <path fill="#7fb7ff" d="M256 464s-216-136-216-248c0-85 65-136 128-136 43 0 88 33 88 33s45-33 88-33c63 0 128 51 128 136 0 112-216 248-216 248z"/>
        </svg>
        """,
        unsafe_allow_html=True,
    )

    code = st.text_input("Passcode", type="password")
    if st.button("Unlock 💙"):
        if code == PASSCODE:
            st.session_state.auth = True
            st.experimental_rerun()
        else:
            st.error("Wrong passcode 💫")
    st.stop()

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
ensure_json("reasons.json", [])
ensure_json("timeline.json", [])

def load_json(name):
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(name, data):
    with open(DATA_DIR / name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- CSS ----------
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg,#04133a 0%, #082a5f 45%, #0d3b7a 100%); color:#eaf4ff; font-family:-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial; }
    .card { background: rgba(255,255,255,0.03); border-radius:12px; padding:18px; margin-bottom:12px; box-shadow:0 6px 30px rgba(2,10,40,0.4); border:1px solid rgba(255,255,255,0.04);}
    h1,h2,h3 { color:#e9f6ff; }
    .polaroid { background:#fff; padding:12px 12px 20px 12px; display:inline-block; margin:10px; border-radius:8px; box-shadow:0 8px 30px rgba(2,8,30,0.45); transform:rotate(-1deg);}
    .polaroid img { width:220px; height:160px; object-fit:cover; border-radius:6px; display:block; margin-bottom:8px;}
    .polaroid .caption { color:#0e2340; font-weight:600; font-size:14px; text-align:center; }
    .stButton>button { background: linear-gradient(90deg,#66aaff,#3b7df0); color:white; border:none; padding:10px 14px; border-radius:10px; font-weight:600;}
    .small-muted { color:#cfe9ff; font-size:13px; opacity:0.9; }
    .section { padding:14px; margin-bottom:14px; border-radius:10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    notes = load_json("notes.json")
    with st.form("note_form"):
        author = st.selectbox("Who is writing?", ["Him", "Me"])
        text = st.text_area("Write your thought...", height=140)
        protect = st.text_input("Optional password (keeps it private)", type="password")
        submitted = st.form_submit_button("Save Thought 💌")
        if submitted and text.strip():
            entry = {"author": author, "text": text.strip(), "date": datetime.now().isoformat(), "lock": bool(protect.strip()), "mask": protect.strip() if protect.strip() else ""}
            notes.append(entry)
            save_json("notes.json", notes)
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

# Our Songs
elif page == "Our Songs 🎶":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Our Songs 🎶")
    songs = load_json("songs.json")
    if songs:
        for s in songs:
            st.markdown(f"**{s.get('title','Untitled')}** — <span class='small-muted'>{s.get('note','')}</span>", unsafe_allow_html=True)
            if s.get("link"): st.markdown(f"[Listen here]({s.get('link')})")
            st.markdown("---")
    else: st.info("No songs added yet.")
    st.markdown("</div>", unsafe_allow_html=True)

# Spin the Wheel
elif page == "Spin the Wheel 💕":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Spin the Wheel of Love 🎡")
    options = ["You get a tight hug 🤗","Movie night 🍿","You owe me ice cream 🍦","You pick dessert 🍰","A forehead kiss 💋","One long cuddle session 💞","I’ll cook your favorite meal 🍛"]
    if st.button("Spin the wheel 💫"):
        choice = random.choice(options)
        st.success(f"Result: **{choice}**")
        st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)

# Reasons I Love You
elif page == "Reasons I Love You 💌":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Reasons I Love You 💌")
    reasons = load_json("reasons.json")
    if not reasons: st.info("No reasons yet.")
    for i, r in enumerate(reasons, start=1):
        with st.expander(f"Reason {i} ❤️"): st.write(r)
    st.markdown("</div>", unsafe_allow_html=True)

# Photos & Polaroids
elif page == "Photos & Polaroids 📸":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Photos & Polaroids 📸")
    st.write("Upload photos to appear as cute Polaroids.")
    st.markdown("</div>", unsafe_allow_html=True)

# Timeline
elif page == "Our Story Timeline 🕰️":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Our Story Timeline 🕰️")
    st.write("Add important moments.")
    st.markdown("</div>", unsafe_allow_html=True)

# Settings
elif page == "Settings ⚙️":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Settings ⚙️")
    st.write("Upload voice note, backup data, or clear everything.")
    st.markdown("</div>", unsafe_allow_html=True)
