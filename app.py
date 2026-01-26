# app.py
import streamlit as st
import json
import random
import time
from datetime import datetime
from pathlib import Path
import os

# ====== PERMANENT DATA STORAGE ======
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

    "photos_and_polaroids": [
        {"url": "WhatsApp Image 2025-10-06 at 04.28.10.jpeg", "caption": "Menifesting this for life💙"},
        {"url": "WhatsApp Image 2025-10-06 at 04.28.09.jpeg", "caption": "Look how happy i am with you😁"},
        {"url": "WhatsApp Image 2025-10-06 at 04.43.16.jpeg", "caption": "Ghibli making us more cute🥹"},
        {"url": "WhatsApp Image 2025-10-06 at 15.06.43.jpeg", "caption": "Our first picture"},
        {"url": "WhatsApp Image 2025-10-06 at 15.06.42.jpeg", "caption": "The moon is beautiful,isn't?🥰"}
    ],

    "click_if_you_miss_me": [
        {"title": "Voice Note 1", "url": "13 Sept, 6.09 pm​.mp3", "desc": "When you miss me,just remember this"},
    ],

    "Our_story_timeline": [
        {"date": "2025-02-18", "thought": "When it all started", "Title": "My birthday party"}
    ],
}

if "app_data" not in st.session_state:
    st.session_state.app_data = default_data

# ---------- CONFIG ----------
st.set_page_config(page_title="For My Anjuuu 💙", layout="wide")
PASSCODE = "Iloveyoucookie"

# ---------- DATA FOLDERS ----------
ROOT = Path(".")
DATA_DIR = ROOT / "data"
PHOTOS_DIR = DATA_DIR / "photos"
DATA_DIR.mkdir(exist_ok=True)
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

def ensure_json(name, default):
    path = DATA_DIR / name
    if not path.exists() or path.stat().st_size == 0:
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2))

ensure_json("notes.json", [])
ensure_json("songs.json", [])
ensure_json("timeline.json", [])

def read_json(name):
    p = DATA_DIR / name
    try:
        return json.loads(p.read_text())
    except Exception:
        return []

def write_json(name, data):
    (DATA_DIR / name).write_text(json.dumps(data, ensure_ascii=False, indent=2))

# ---------- CSS / ROMANTIC BACKGROUND ----------
st.markdown(
    """
    <style>
    :root {
      --accent1: #66aaff;
      --accent2: #3b7df0;
      --card-bg: rgba(255,255,255,0.78);
      --text: #0b2b57;
    }
    html, body, .stApp, .main { height: 100%; }
    .stApp {
      background: linear-gradient(135deg, #b3e5fc 0%, #d6c8f8 45%, #bfe0ff 100%);
      background-attachment: fixed;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
      color: var(--text);
      overflow-x: hidden;
    }
    body::before {
      content: "";
      background-image: url('https://i.imgur.com/Z1r5NnH.png');
      background-repeat: repeat;
      background-size: 100px;
      opacity: 0.12;
      position: fixed;
      inset: 0;
      z-index: -1;
      animation: floatBg 18s linear infinite;
    }
    @keyframes floatBg { from {background-position: 0 0;} to {background-position: 0 200px;} }
    .card { background: var(--card-bg); padding: 18px; border-radius: 14px; margin-bottom: 14px; box-shadow: 0 8px 30px rgba(10,20,50,0.08); border: 1px solid rgba(0,0,0,0.04); }
    h1,h2,h3 { color: var(--text); margin-bottom:6px; }
    .small-muted { color: rgba(11,43,87,0.7); }
    .stButton>button { background: linear-gradient(90deg,var(--accent1),var(--accent2)); color:white; border:none; padding:10px 14px; border-radius:10px; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- AUTH ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "passcode_input" not in st.session_state:
    st.session_state.passcode_input = ""

def show_passcode():
    st.markdown("<div style='max-width:820px;margin:28px auto;'>", unsafe_allow_html=True)
    st.markdown("<div class='card' style='text-align:center;'>", unsafe_allow_html=True)
    st.markdown("<h1>A little world — just for you 🫀</h1>", unsafe_allow_html=True)
    st.markdown("<p class='small-muted'>Enter the secret passcode to open our private space</p>", unsafe_allow_html=True)
    st.session_state.passcode_input = st.text_input("Passcode", type="password", key="pass")
    if st.button("Unlock 💙"):
        if st.session_state.passcode_input == PASSCODE:
            st.session_state.authenticated = True
            st.success("Unlocked — welcome 💙")
            time.sleep(0.5)
            st.rerun()  # ✅ Fixed line (was st.experimental_rerun)
        else:
            st.error("That's not the correct passcode. Try again 💫")
    st.markdown("</div></div>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    show_passcode()
    st.stop()

# ---------- SIDEBAR NAV ----------
st.sidebar.title("💫 Navigate")
page = st.sidebar.radio("", [
    "Home 🏠",
    "Today's Thought 💭",
    "Click if you miss me 💞",
    "Our Songs 🎶",
    "Spin the Wheel 💕",
    "50+ Reasons I Love You 💌",
    "Photos & Polaroids 📸",
    "Our Story Timeline 🕰️",
    "Settings ⚙️"
])

# ---------- PAGES ----------

if page == "Home 🏠":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("Welcome, my love 🫀")
    st.write("This little corner was made with care — add memories, songs, and notes. It's private and just for us.")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Today's Thought 💭":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("💭 Today's Thought")
    notes = read_json("notes.json")
    with st.form("note_form"):
        author = st.selectbox("Who is writing?", ["Me", "Him"])
        text = st.text_area("Write your thought...", height=140)
        lock = st.text_input("Optional entry-password (keeps it private)", type="password")
        submitted = st.form_submit_button("Save Thought 💌")
        if submitted and text.strip():
            notes.append({"author": author, "text": text.strip(), "date": datetime.now().isoformat(), "locked": bool(lock.strip()), "pwd": lock.strip()})
            write_json("notes.json", notes)
            st.success("Saved 💙")
    st.write("---")
    for entry in reversed(notes):
        if entry.get("locked"):
            st.markdown(f"**{entry['author']}** — {entry['date']}")
            key = f"rev_{entry['date']}"
            if st.button("Reveal (locked) — enter password", key=key):
                pw = st.text_input("Enter password to reveal", key=f"pw_{key}", type="password")
                if pw == entry.get("pwd"):
                    st.info(entry["text"])
                else:
                    st.warning("Wrong password")
        else:
            st.markdown(f"**{entry['author']}** — {entry['date']}")
            st.write(entry["text"])
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Click if you miss me 💞":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Click only if you miss me 💞")
    st.write("A little surprise — voice note or message.")
    if st.button("Click only if you miss me 😘"):
        st.success("I miss you so much — counting the moments until I see you again. 🫀")
        voice_path = DATA_DIR / "voice.mp3"
        if voice_path.exists():
            st.audio(str(voice_path))
        else:
            st.info("No voice note uploaded yet. Upload one in Settings.")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Our Songs 🎶":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Our Songs 🎶")
    songs = read_json("songs.json")
    if not songs:
        st.info("No songs added yet. Add songs in Settings.")
    else:
        for s in songs:
            st.markdown(f"**{s.get('title','Untitled')}** — <span class='small-muted'>{s.get('note','')}</span>", unsafe_allow_html=True)
            if s.get("link"):
                st.markdown(f"[Listen]({s.get('link')})")
            st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)
    
elif page == "Spin the Wheel 💕":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("🎡 Spin the Wheel of Love 💕")
    st.write("Spin the wheel and see what romantic surprise awaits 💙")

    outcomes = [
        "You get a long warm hug 💞",
        "Movie together 🍿",
        "You owe me ice cream 🍦",
        "Surprise date planned by you 💫",
        "A truth i can't lie about",
        "You have to kiss secretly in front of everyone 😚",
        "You upload a story of mee",
        "You have to say 'I love you' 5 times in different ways💙",
        "I get to pick the next movie 🎬",
        "A dare i can't deny"
    ]

    # CSS for spinning animation
    st.markdown("""
        <style>
        .wheel {
            width: 220px;
            height: 220px;
            border-radius: 50%;
            border: 8px solid #3b7df0;
            margin: 40px auto;
            background: conic-gradient(
                #b3e5fc 0deg 36deg,
                #d6c8f8 36deg 72deg,
                #bfe0ff 72deg 108deg,
                #b3e5fc 108deg 144deg,
                #d6c8f8 144deg 180deg,
                #bfe0ff 180deg 216deg,
                #b3e5fc 216deg 252deg,
                #d6c8f8 252deg 288deg,
                #bfe0ff 288deg 324deg,
                #b3e5fc 324deg 360deg
            );
            position: relative;
            animation: none;
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(3600deg); }
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("Spin the Wheel 🎡"):
        with st.spinner("Spinning... 💞"):
            st.markdown('<div class="wheel" style="animation: spin 2s ease-out;"></div>', unsafe_allow_html=True)
            time.sleep(2)
            result = random.choice(outcomes)
            st.success(f"💫 {result}")
    else:
        st.markdown('<div class="wheel"></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


elif page == "50+ Reasons I Love You 💌":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Reasons I Love You 💌")
    reasons = [
        "I love your personality", "I love your smile", "I love your hairs", "I love your smell",
        "I love your jollyness", "I love your maturity", "I love your childishness",
        "I love the way you balance", "I love your futuristic vision", "I love the way I am happy around you",
        "I love the way I am safe around you", "I love that you communicate", "I love that you try to solve",
        "I love that you are emotionally available", "I love your humour", "I love your eyes",
        "I love the way you listen", "I love that you remember details", "I love the sense of security you give",
        "I love your confidence", "I love your nature", "I love the small gestures", "I love your intelligence",
        "I love your positive approach towards life", "I love your dressing sense", "I love that you never think of giving up",
        "I love how you respect others", "I love your humanity", "I love how you understand", "I love that family matters",
        "I love that you think of 'your' people so selflessly", "I love that you cry", "I love your anger", "I love your dance",
        "I love your general knowledge", "I love that you love", "I love that you believe in God", "I love that you learn",
        "I love how you manage", "I love that you are foodie", "I love your courage", "I love your boundaries", "I love your control",
        "I love your thoughtfulness", "I love how you complete me", "I love the way you say 'meri laduuu'", "I love the way you teach me",
        "I love the priority you give", "I love the support you give", "I love how you make me laugh", "I love the way you love me",
        "I love our friendship", "I love that you have good presence of mind", "I love that you trust me", "I love that you don't get irritated by me", "I love that you give honest feedback about what you feel", "I love that i can talk about anything with you", "I love that you smile even when i act like idiot", "I love that you feel comfortable around me", "I love that you forgive my mistakes", "I love that you don't keep grudges", "I love that you make me feel special", "I love that i never get tired of talking to you", "I love that i am not you need,i am your choice", "I love that world seems a nice place around you", "You are the best thing that has happened to me", "I could write all these reasons because it was YOU", "And most importantly, I love you 💙"
    ]
    for i, r in enumerate(reasons, 1):
        st.markdown(f"**{i}. {r}**")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Photos & Polaroids 📸":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Photos & Polaroids 📸")
    uploaded = st.file_uploader("Upload a photo (jpg/png)", type=["jpg","jpeg","png"])
    caption = st.text_input("Caption for this photo")
    if st.button("Save photo"):
        if uploaded is not None:
            fname = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded.name}"
            target = PHOTOS_DIR / fname
            with open(target, "wb") as f:
                f.write(uploaded.getbuffer())
            tl = read_json("timeline.json")
            tl.append({"type":"photo","file": str(target), "caption": caption, "date": datetime.now().isoformat()})
            write_json("timeline.json", tl)
            st.success("Photo saved as Polaroid 💙")
        else:
            st.warning("Please choose an image first.")

    files = sorted(PHOTOS_DIR.glob("*"), key=os.path.getmtime, reverse=True)
    if files:
        cols = st.columns(3)
        for i, fpath in enumerate(files):
            with cols[i % 3]:
                try:
                    st.image(str(fpath), use_container_width=True)
                    tl = read_json("timeline.json")
                    cap = next((t.get("caption","") for t in tl if t.get("file") == str(fpath)), "")
                    if cap:
                        st.caption(cap)
                except Exception:
                    pass
    else:
        st.info("No photos yet — upload one above.")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Our Story Timeline 🕰️":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Our Story Timeline 🕰️")
    tl = read_json("timeline.json")
    with st.form("mem_form"):
        title = st.text_input("Title")
        date_val = st.date_input("Date")
        desc = st.text_area("Description")
        submit = st.form_submit_button("Add memory")
        if submit:
            tl.append({"type":"memory","title": title, "date": str(date_val), "desc": desc})
            write_json("timeline.json", tl)
            st.success("Memory saved 💙")
    memories = [t for t in tl if t.get("type") == "memory"]
    for m in sorted(memories, key=lambda x: x.get("date",""), reverse=True):
        st.subheader(f"{m.get('title')} — {m.get('date')}")
        st.write(m.get("desc"))
        st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Settings ⚙️":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Settings & Uploads ⚙️")
    st.write("Upload voice note, add songs, or clear saved data.")

    audio = st.file_uploader("Upload voice clip (mp3/wav) for 'miss me'", type=["mp3","wav"])
    if st.button("Upload voice clip"):
        if audio:
            with open(DATA_DIR / "voice.mp3", "wb") as f:
                f.write(audio.getbuffer())
            st.success("Voice clip uploaded 💙")
        else:
            st.warning("Choose a file first.")

    st.markdown("---")
    st.subheader("Add a song")
    s_title = st.text_input("Song title")
    s_link = st.text_input("Link (optional)")
    s_note = st.text_area("Why it matters (short note)")
    if st.button("Add song"):
        songs = read_json("songs.json")
        songs.append({"title": s_title, "link": s_link, "note": s_note})
        write_json("songs.json", songs)
        st.success("Song added 💙")

    st.markdown("---")
    if st.button("Clear all saved data (photos, notes, timeline, songs)"):
        write_json("notes.json", [])
        write_json("songs.json", [])
        write_json("timeline.json", [])
        for f in PHOTOS_DIR.glob("*"):
            try:
                f.unlink()
            except Exception:
                pass
        st.success("Cleared saved data for this deployment.")
    st.markdown("</div>", unsafe_allow_html=True)

