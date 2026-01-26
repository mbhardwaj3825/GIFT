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

# ================= DEFAULT CONTENT =================
DEFAULT_SONGS = [
    {
        "title": "Those eyes",
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

# ================= FILE HELPERS =================
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

# ================= INITIALIZE DATA =================
ensure_json(DATA_DIR / "songs.json", DEFAULT_SONGS)
ensure_json(DATA_DIR / "timeline.json", DEFAULT_TIMELINE)
ensure_json(DATA_DIR / "notes.json", [])

# ================= AUTH =================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("A little world — just for you 🫀")
    code = st.text_input("Enter passcode", type="password")
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
        "Our Songs 🎶",
        "Photos 📸",
        "Our Story 🕰️",
        "Settings ⚙️",
    ]
)

# ================= PAGES =================
if page == "Home 🏠":
    st.header("Welcome, my love 🫀")
    st.write("This space is private. It holds what we choose to remember.")

# ---------- SONGS ----------
elif page == "Our Songs 🎶":
    st.header("Our Songs 🎶")
    songs = read_json(DATA_DIR / "songs.json")

    for s in songs:
        st.subheader(s["title"])
        st.caption(s.get("note", ""))
        if s.get("link"):
            st.markdown(f"[Listen here]({s['link']})")
        st.markdown("---")

# ---------- PHOTOS ----------
elif page == "Photos 📸":
    st.header("Photos & Polaroids 📸")

    uploaded = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])
    caption = st.text_input("Caption")

    if st.button("Save photo"):
        if uploaded:
            name = f"{int(time.time())}_{uploaded.name}"
            path = PHOTOS_DIR / name
            with open(path, "wb") as f:
                f.write(uploaded.getbuffer())

            timeline = read_json(DATA_DIR / "timeline.json")
            timeline.append({
                "type": "photo",
                "file": str(path),
                "caption": caption,
                "date": datetime.now().isoformat()
            })
            write_json(DATA_DIR / "timeline.json", timeline)
            st.success("Saved 💙")
        else:
            st.warning("Upload a photo first")

    files = sorted(PHOTOS_DIR.glob("*"), reverse=True)
    for f in files:
        st.image(str(f), use_container_width=True)

# ---------- TIMELINE ----------
elif page == "Our Story 🕰️":
    st.header("Our Story 🕰️")
    timeline = read_json(DATA_DIR / "timeline.json")

    for t in timeline:
        if t["type"] == "memory":
            st.subheader(f"{t['title']} — {t['date']}")
            st.write(t["desc"])
            st.markdown("---")

# ---------- SETTINGS ----------
elif page == "Settings ⚙️":
    st.header("Settings")

    if st.button("Clear all data"):
        write_json(DATA_DIR / "songs.json", DEFAULT_SONGS)
        write_json(DATA_DIR / "timeline.json", DEFAULT_TIMELINE)
        write_json(DATA_DIR / "notes.json", [])
        for f in PHOTOS_DIR.glob("*"):
            f.unlink()
        st.success("Reset complete")
