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

# Only create empty files for content we will fill later
ensure_json("notes.json", [])
ensure_json("songs.json", [])
ensure_json("timeline.json", [])

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

# ---------- PASSCODE PAGE ----------
def passcode_page():
    st.markdown("<h1 style='text-align:center; margin-top:60px;'>A little world — just for you 🫀</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; margin-bottom:24px;'>Enter the secret passcode to unlock our private space</h4>", unsafe_allow_html=True)
    st.session_state.passcode_input = st.text_input("Passcode", type="password")
    if st.button("Unlock 💙"):
        if st.session_state.passcode_input == PASSCODE:
            st.session_state.auth = True
            st.experimental_rerun()
        else:
            st.error("Wrong passcode 💫")

# ---------- MAIN APP ----------
if not st.session_state.auth:
    passcode_page()
    st.stop()

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

# Our Songs
elif page == "Our Songs 🎶":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Our Songs 🎶")
    st.write("No songs added yet. Add them later in Settings.")
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
    # Your 54 Reasons directly added
    reasons = [
        "I love your personality","I love your smile","I love your hairs","I love your smell","I love your jollyness",
        "I love your maturity","I love your childishness","I love the way you balance","I love your futuristic vision",
        "I love the way I am happy around you","I love the way I am safe around you","I love that you communicate",
        "I love that you try to solve","I love that you are emotionally available","I love your humour","I love your eyes",
        "I love the way you listen","I love that you remember details","I love the sense of security you give",
        "I love your confidence","I love your nature","I love the small gestures","I love your intelligence",
        "I love your positive approach towards life","I love your dressing sense","I love that you never think of giving up",
        "I love how you respect others","I love your humanity","I love how you understand","I love that for you family matters",
        "I love that you think of 'your' people so selflessly","I love that you cry","I love your anger","I love your dance",
        "I love your general knowledge","I love that you love","I love that you believe in God","I love that you learn",
        "I love how you manage","I love that you are foodie","I love your courage","I love your boundaries","I love your control",
        "I love your thoughtfulness","I love how you complete me","I love the way you say 'meri laduuu'","I love the way you teach me",
        "I love the priority you give","I love the support you give","I love how you make me laugh","I love the way you love me",
        "I love our friendship","Most importantly I love youu"
    ]
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
