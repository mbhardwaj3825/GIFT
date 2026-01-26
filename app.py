# app.py
import streamlit as st
import json
import random
import time
from datetime import datetime
from pathlib import Path
import os

# ================= CONFIG =================
st.set_page_config(page_title="For My Anjuuu 💙", layout="wide")
PASSCODE = "Iloveyoucookie"

ROOT = Path(".")
DATA_DIR = ROOT / "data"
PHOTOS_DIR = DATA_DIR / "photos"

DATA_DIR.mkdir(exist_ok=True)
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

# ================= DEFAULT DATA =================
DEFAULT_SONGS = [
    {
        "title": "Those Eyes",
        "note": "Always reminds me of your eyes",
        "link": "https://music.youtube.com/watch?v=YPeHGoGhHxg"
    },
    {
        "title": "Teri Deewani",
        "note": "Vo to me hun hi 💙",
        "link": "https://music.youtube.com/watch?v=3R-q79a7n98"
    },
    {
        "title": "Humein Tumse Pyar Kitna",
        "note": "'Magar jee nahi sakte' got real",
        "link": "https://music.youtube.com/watch?v=aCoVNTLfcGU"
    },
    {
        "title": "Tera Mera Pyar Amar",
        "note": "Yahi to kehna hai tumse bas",
        "link": "https://music.youtube.com/watch?v=1DFCzfXL514"
    }
]

DEFAULT_TIMELINE = [
    {
        "type": "memory",
        "title": "My Birthday Party",
        "date": "2025-02-18",
        "desc": "When it all started 💙"
    }
]

# ================= HELPERS =================
def ensure_json(path, default):
    if not path.exists() or path.stat().st_size == 0:
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2))

def read_json(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return []

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

# ================= INIT FILES =================
ensure_json(DATA_DIR / "songs.json", DEFAULT_SONGS)
ensure_json(DATA_DIR / "notes.json", [])
ensure_json(DATA_DIR / "timeline.json", DEFAULT_TIMELINE)

# ================= AUTH =================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("A little world — just for you 🫀")
    code = st.text_input("Enter the secret passcode", type="password")
    if st.button("Unlock 💙"):
        if code == PASSCODE:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Wrong passcode")
    st.stop()

# ================= SIDEBAR =================
page = st.sidebar.radio(
    "Navigate",
    [
        "Home 🏠",
        "Today's Thought 💭",
        "Click if you miss me 💞",
        "Our Songs 🎶",
        "Spin the Wheel 💕",
        "50+ Reasons I Love You 💌",
        "Photos & Polaroids 📸",
        "Our Story Timeline 🕰️",
        "Settings ⚙️",
    ]
)

# ================= PAGES =================

if page == "Home 🏠":
    st.header("Welcome, my love 🫀")
    st.write("This space exists only for us.")

# ---------- TODAY'S THOUGHT ----------
elif page == "Today's Thought 💭":
    st.header("Today's Thought 💭")
    notes = read_json(DATA_DIR / "notes.json")

    with st.form("note_form"):
        author = st.selectbox("Who is writing?", ["Me", "Him"])
        text = st.text_area("Write your thought...")
        submit = st.form_submit_button("Save 💙")
        if submit and text.strip():
            notes.append({
                "author": author,
                "text": text,
                "date": datetime.now().isoformat()
            })
            write_json(DATA_DIR / "notes.json", notes)
            st.success("Saved")

    for n in reversed(notes):
        st.markdown(f"**{n['author']} — {n['date']}**")
        st.write(n["text"])
        st.markdown("---")

# ---------- MISS ME ----------
elif page == "Click if you miss me 💞":
    st.header("Click only if you miss me 💞")
    if st.button("Click 💙"):
        st.success("I miss you too 🫀")
        voice = DATA_DIR / "voice.mp3"
        if voice.exists():
            st.audio(str(voice))
        else:
            st.info("No voice note uploaded yet")

# ---------- SONGS ----------
elif page == "Our Songs 🎶":
    st.header("Our Songs 🎶")
    songs = read_json(DATA_DIR / "songs.json")
    for s in songs:
        st.subheader(s["title"])
        st.caption(s.get("note", ""))
        if s.get("link"):
            st.markdown(f"[Listen 🎧]({s['link']})")
        st.markdown("---")

# ---------- SPIN ----------
elif page == "Spin the Wheel 💕":
    st.header("Spin the Wheel 💕")
    options = [
        "A long hug 💞",
        "Movie together 🍿",
        "Ice cream date 🍦",
        "Surprise planned by you 💫",
        "A secret confession 😌"
    ]
    if st.button("Spin 🎡"):
        time.sleep(1)
        st.success(random.choice(options))

# ---------- REASONS ----------
elif page == "50+ Reasons I Love You 💌":
    st.header("Reasons I Love You 💌")
    reasons = [
        "Your smile", "Your eyes", "Your honesty", "Your care",
        "The way you listen", "The way you love"
    ]
    for i, r in enumerate(reasons, 1):
        st.write(f"{i}. {r}")

# ---------- PHOTOS ----------
elif page == "Photos & Polaroids 📸":
    st.header("Photos & Polaroids 📸")
    img = st.file_uploader("Upload image", type=["jpg", "png"])
    caption = st.text_input("Caption")
    if st.button("Save photo"):
        if img:
            name = f"{int(time.time())}_{img.name}"
            path = PHOTOS_DIR / name
            with open(path, "wb") as f:
                f.write(img.getbuffer())
            st.success("Saved 💙")

    for f in sorted(PHOTOS_DIR.glob("*"), reverse=True):
        st.image(str(f), use_container_width=True)

# ---------- TIMELINE ----------
elif page == "Our Story Timeline 🕰️":
    st.header("Our Story 🕰️")
    tl = read_json(DATA_DIR / "timeline.json")

    with st.form("memory"):
        title = st.text_input("Title")
        date = st.date_input("Date")
        desc = st.text_area("Description")
        if st.form_submit_button("Add"):
            tl.append({
                "type": "memory",
                "title": title,
                "date": str(date),
                "desc": desc
            })
            write_json(DATA_DIR / "timeline.json", tl)
            st.success("Saved")

    for m in tl:
        if m["type"] == "memory":
            st.subheader(f"{m['title']} — {m['date']}")
            st.write(m["desc"])
            st.markdown("---")

# ---------- SETTINGS ----------
elif page == "Settings ⚙️":
    st.header("Settings")
    audio = st.file_uploader("Upload voice note", type=["mp3"])
    if st.button("Save voice"):
        if audio:
            with open(DATA_DIR / "voice.mp3", "wb") as f:
                f.write(audio.getbuffer())
            st.success("Voice saved 💙")
