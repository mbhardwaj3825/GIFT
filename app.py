# app.py
import streamlit as st
import json, random, time, os, gspread
from pathlib import Path
from datetime import datetime
from google.oauth2.service_account import Credentials

# ---------- CONFIG ----------
st.set_page_config(page_title="For My Anjuuu 💙", layout="wide")
PASSCODE = "Iloveyoucookie"

# ---------- DATA FOLDERS ----------
ROOT = Path(".")
DATA_DIR = ROOT / "data"
PHOTOS_DIR = DATA_DIR / "photos"
DATA_DIR.mkdir(exist_ok=True)
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

# ---------- GOOGLE SHEETS SETUP ----------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_PATH = "gs_credentials.json"
SHEET_ID = "YOUR_GOOGLE_SHEET_ID_HERE"

def gs_client():
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
    return gspread.authorize(creds)

def read_sheet(tab):
    try:
        client = gs_client()
        sh = client.open_by_key(SHEET_ID)
        ws = sh.worksheet(tab)
        return ws.get_all_records()
    except Exception:
        return []

def write_sheet(tab, data, headers):
    try:
        client = gs_client()
        sh = client.open_by_key(SHEET_ID)
        ws = sh.worksheet(tab)
        ws.clear()
        ws.append_row(headers)
        for row in data:
            ws.append_row([row.get(h, "") for h in headers])
    except Exception:
        st.warning(f"Failed to sync {tab} with Google Sheets.")

# ---------- JSON backup functions ----------
def ensure_json(name, default):
    path = DATA_DIR / name
    if not path.exists() or path.stat().st_size == 0:
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2))

def read_json(name):
    p = DATA_DIR / name
    try:
        return json.loads(p.read_text())
    except Exception:
        return []

def write_json(name, data):
    (DATA_DIR / name).write_text(json.dumps(data, ensure_ascii=False, indent=2))

# Ensure files exist
ensure_json("notes.json", [])
ensure_json("songs.json", [])
ensure_json("timeline.json", [])

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
            st.experimental_rerun()
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

# ---------- LOAD DATA ----------
notes = read_json("notes.json")
songs = read_json("songs.json")
timeline = read_json("timeline.json")

# Try syncing from Google Sheets if available
gs_notes = read_sheet("thoughts")
if gs_notes:
    notes = gs_notes
    write_json("notes.json", notes)

gs_songs = read_sheet("songs")
if gs_songs:
    songs = gs_songs
    write_json("songs.json", songs)

gs_timeline = read_sheet("timeline")
if gs_timeline:
    timeline = gs_timeline
    write_json("timeline.json", timeline)

# ---------- PAGES ----------
if page == "Home 🏠":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("Welcome, my love 🫀")
    st.write("This little corner was made with care — add memories, songs, and notes. It's private and just for us.")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Today's Thought 💭":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("💭 Today's Thought")
    with st.form("note_form"):
        author = st.selectbox("Who is writing?", ["Me", "Him"])
        text = st.text_area("Write your thought...", height=140)
        lock = st.text_input("Optional entry-password (keeps it private)", type="password")
        submitted = st.form_submit_button("Save Thought 💌")
        if submitted and text.strip():
            notes.append({
                "author": author, "text": text.strip(),
                "date": datetime.now().isoformat(),
                "locked": bool(lock.strip()), "pwd": lock.strip()
            })
            write_json("notes.json", notes)
            write_sheet("thoughts", notes, ["author","text","date","locked","pwd"])
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
        voice_path = DATA_DIR / "voice.mp3"
        if voice_path.exists():
            st.audio(str(voice_path))
        else:
            st.info("No voice note uploaded yet. Upload one in Settings.")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Our Songs 🎶":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Our Songs 🎶")
    if not songs:
        st.info("No songs added yet. Add songs in Settings.")
    else:
        for s in songs:
            st.markdown(f"**{s.get('title','Untitled')}** — {s.get('note','')}")
            if s.get("link"):
                st.markdown(f"[Listen]({s.get('link')})")
            st.markdown("---")
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
        "I love our friendship", "And most importantly, I love you 💙"
    ]
    for i, r in enumerate(reasons, 1):
        st.markdown(f"**{i}. {r}**")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Settings ⚙️":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Settings & Uploads ⚙️")
    st.write("Upload voice note, add songs, or clear saved data.")

    # voice upload
    audio = st.file_uploader("Upload voice clip (mp3/wav) for 'miss me'", type=["mp3","wav"])
    if st.button("Upload voice clip"):
        if audio:
            with open(DATA_DIR / "voice.mp3", "wb") as f:
                f.write(audio.getbuffer())
            st.success("Voice clip uploaded 💙")
        else:
            st.warning("Choose a file first.")

    # add song
    st.markdown("---")
    st.subheader("Add a song")
    s_title = st.text_input("Song title")
    s_link = st.text_input("Link (optional)")
    s_note = st.text_area("Why it matters (short note)")
    if st.button("Add song"):
        songs.append({"title": s_title, "link": s_link, "note": s_note})
        write_json("songs.json", songs)
        write_sheet("songs", songs, ["title","note","link"])
        st.success("Song added 💙")

    # clear data
    st.markdown("---")
    if st.button("Clear all saved data"):
        write_json("notes.json", [])
        write_json("songs.json", [])
        write_json("timeline.json", [])
        for f in PHOTOS_DIR.glob("*"):
            try: f.unlink()
            except: pass
        st.success("Cleared all data 💙")
    st.markdown("</div>", unsafe_allow_html=True)
