# app.py
import streamlit as st
import json
import random
import time
from datetime import datetime
from pathlib import Path

# ---------- CONFIG ----------
st.set_page_config(page_title="For My Anjuuu 💙", page_icon="🫀", layout="wide")
PASSCODE = "Iloveyouladuu"

# ---------- SESSION STATE ----------
if "auth" not in st.session_state:
    st.session_state.auth = False
if "pass_input" not in st.session_state:
    st.session_state.pass_input = ""

# ---------- DATA FOLDERS ----------
DATA_DIR = Path("data")
PHOTOS_DIR = DATA_DIR / "photos"
DATA_DIR.mkdir(exist_ok=True)
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

def ensure_json(name, default):
    p = DATA_DIR / name
    if not p.exists():
        p.write_text(json.dumps(default, ensure_ascii=False, indent=2))

ensure_json("notes.json", [])
ensure_json("songs.json", [])
ensure_json("timeline.json", [])

# ---------- GLOBAL CSS (romantic blue background + subtle hearts pattern) ----------
st.markdown(
    """
    <style>
    :root {
      --accent1: #66aaff;
      --accent2: #3b7df0;
      --card-bg: rgba(255,255,255,0.08);
      --text: #eaf4ff;
      --muted: rgba(234,244,255,0.8);
    }
    html, body, .stApp, .main {
      height: 100%;
    }
    .stApp {
      background: linear-gradient(135deg, #d9ecff 0%, #a8d1ff 40%, #6699ff 100%);
      background-attachment: fixed;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      color: var(--text);
      overflow-x: hidden;
    }
    /* subtle hearts pattern overlay */
    .heart-bg {
      background-image: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.03) 2px, transparent 2px),
                        radial-gradient(circle at 80% 80%, rgba(255,255,255,0.03) 2px, transparent 2px);
      background-size: 100px 100px;
      position: fixed; inset: 0; z-index: -1; opacity: 0.6;
      pointer-events: none;
    }

    .card {
      background: var(--card-bg);
      border-radius: 14px;
      padding: 18px;
      margin-bottom: 14px;
      box-shadow: 0 6px 30px rgba(3,10,30,0.25);
      border: 1px solid rgba(255,255,255,0.06);
    }

    h1,h2,h3 { color: var(--text); margin-bottom: 6px; }
    .small-muted { color: var(--muted); font-size: 14px; }
    .polaroid {
      background: #fff; padding:12px 12px 18px; display:inline-block; margin:10px; border-radius:8px;
      box-shadow:0 8px 30px rgba(2,8,30,0.15); transform: rotate(-1deg)
    }
    .polaroid img { width:220px; height:160px; object-fit:cover; border-radius:6px; display:block; margin-bottom:8px;}
    .polaroid .caption { color:#0e2340; font-weight:600; font-size:14px; text-align:center; }

    /* wheel styles */
    .wheel-wrap { display:flex; flex-direction:column; align-items:center; }
    .pointer {
      width:0; height:0; border-left:18px solid transparent; border-right:18px solid transparent;
      border-bottom:28px solid #0b3a86; margin-bottom:8px; transform: translateY(8px);
    }
    .wheel {
      width: 320px; height:320px; border-radius:50%; position: relative; overflow:hidden;
      box-shadow: 0 10px 40px rgba(0,0,0,0.2); border: 8px solid rgba(255,255,255,0.06);
      transform: rotate(0deg);
    }
    .wheel .slice {
      position:absolute; left:50%; top:50%; transform-origin:0% 0%;
      width:50%; height:50%;
      display:flex; align-items:center; justify-content:flex-end; padding-right:10px;
      color:white; font-weight:700; text-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }
    .slice span { transform: skewY(-30deg) rotate(0deg); display:block; width:160px; text-align:right; padding-right:12px; font-size:14px;}
    </style>
    <div class='heart-bg'></div>
    """,
    unsafe_allow_html=True,
)

# ---------- PASSCODE / LOCK SCREEN ----------
def show_passcode_screen():
    st.markdown("<div style='max-width:720px;margin:30px auto;'>", unsafe_allow_html=True)
    st.markdown("<div class='card' style='text-align:center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='margin-top:12px'>A little world — just for you 🫀</h1>", unsafe_allow_html=True)
    st.markdown("<p class='small-muted'>Enter our secret passcode to open this private space</p>", unsafe_allow_html=True)
    st.session_state.pass_input = st.text_input("Passcode", type="password", key="pass")
    if st.button("Unlock 💙"):
        if st.session_state.pass_input == PASSCODE:
            st.session_state.auth = True
            st.success("Unlocked — welcome 💙")
            time.sleep(0.6)
            st.experimental_rerun()
        else:
            st.error("That's not the correct code. Try again 💫")
    st.markdown("</div></div>", unsafe_allow_html=True)

if not st.session_state.auth:
    show_passcode_screen()
    st.stop()

# ---------- MAIN LAYOUT ----------
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
if page == "Home 🏠":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("Welcome, my love 🫀")
    st.write("This little space is crafted with love. Use the menu to explore — everything here is private and only for us.")
    st.markdown("</div>", unsafe_allow_html=True)

# Today's Thought (simple diary with optional lock)
elif page == "Today's Thought 💭":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("💭 Today's Thought")
    st.write("Leave a short note for me (or read past ones). You can add an optional entry password to hide sensitive notes.")
    notes_path = DATA_DIR / "notes.json"
    notes = json.loads(notes_path.read_text()) if notes_path.exists() else []
    with st.form("note_form"):
        author = st.selectbox("Who is writing?", ["Me", "Him"])
        content = st.text_area("Write your thought...", height=140)
        lock = st.text_input("Optional entry-password (keeps it private)", type="password")
        submitted = st.form_submit_button("Save Thought 💌")
        if submitted and content.strip():
            notes.append({"author": author, "text": content.strip(), "date": datetime.now().isoformat(), "locked": bool(lock.strip()), "pwd": lock.strip()})
            notes_path.write_text(json.dumps(notes, ensure_ascii=False, indent=2))
            st.success("Saved 💙")
    st.write("---")
    st.subheader("Past thoughts")
    for entry in reversed(notes):
        if entry.get("locked"):
            st.markdown(f"**{entry['author']}** — {entry['date']}")
            if st.button(f"Reveal (locked) — enter password", key=f"rev_{entry['date']}"):
                pw = st.text_input("Enter password", key=f"pw_{entry['date']}", type="password")
                if pw == entry.get("pwd"):
                    st.info(entry["text"])
                else:
                    st.warning("Wrong password")
        else:
            st.markdown(f"**{entry['author']}** — {entry['date']}")
            st.write(entry["text"])
    st.markdown("</div>", unsafe_allow_html=True)

# Click if you miss me
elif page == "Click if you miss me 💞":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Click only if you miss me 💞")
    st.write("A little surprise — only click if you really miss me.")
    if st.button("Click only if you miss me 😘"):
        st.success("I miss you more than words — can't wait to be with you. 💙")
        audio = DATA_DIR / "voice.mp3"
        if audio.exists():
            st.audio(str(audio))
        else:
            st.info("No voice note uploaded yet. Add one in Settings.")
    st.markdown("</div>", unsafe_allow_html=True)

# Our Songs (placeholder)
elif page == "Our Songs 🎶":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Our Songs 🎶")
    songs_path = DATA_DIR / "songs.json"
    songs = json.loads(songs_path.read_text()) if songs_path.exists() else []
    if songs:
        for s in songs:
            st.markdown(f"**{s.get('title','Untitled')}** — <span class='small-muted'>{s.get('note','')}</span>", unsafe_allow_html=True)
            if s.get("link"):
                st.markdown(f"[Listen]({s.get('link')})")
            st.markdown("---")
    else:
        st.write("No songs added yet. You can add songs in Settings (title/link/note).")
    st.markdown("</div>", unsafe_allow_html=True)

# Spin the wheel - animated
elif page == "Spin the Wheel 💕":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Spin the Wheel of Love 🎡")
    st.write("Click Spin — watch it turn and wait a few seconds for the result!")

    options = [
        "You get a tight hug 🤗",
        "Movie night 🍿",
        "You owe me ice cream 🍦",
        "You pick dessert 🍰",
        "A forehead kiss 💋",
        "One long cuddle session 💞",
        "I’ll cook your favorite meal 🍛",
        "You get a surprise gift 🎁"
    ]

    n = len(options)
    # visual labels for wheel (we'll use first n labels)
    labels = options[:n]

    # Render pointer and wheel container placeholder
    st.markdown("<div style='display:flex; flex-direction:column; align-items:center;'>", unsafe_allow_html=True)
    st.markdown("<div class='pointer'></div>", unsafe_allow_html=True)

    # When Spin clicked, pick random index and compute rotation angle so that the chosen wedge ends up at the pointer (top)
    if st.button("Spin 🎡"):
        chosen_idx = random.randrange(n)
        # spins for dramatic effect
        spins = random.randint(4, 7)
        seg = 360 / n
        # center angle of chosen segment (0deg slice center at 0 + seg/2 etc.)
        center_angle = chosen_idx * seg + seg / 2
        # We want to rotate so that center_angle goes to top(0deg). So rotation = spins*360 + (360 - center_angle) + small random offset
        offset = random.uniform(-seg/4, seg/4)
        rotation_deg = spins * 360 + (360 - center_angle) + offset

        # create unique wheel id
        uid = random.randint(100000, 999999)
        wheel_id = f"wheel_{uid}"

        # Build wheel HTML with slices positioned (skew trick)
        slice_html = ""
        colors = ["#3b82f6", "#60a5fa"]  # alternate blues
        for i, lab in enumerate(labels):
            rot = i * seg
            color = colors[i % len(colors)]
            # each slice absolute rotated by rot deg; skewY to create wedge shape visually
            slice_html += f"<div class='slice' style='transform: rotate({rot}deg) translate(-50%, -100%);'><span style='background:{color}; padding:18px 8px;'>{lab}</span></div>"

        wheel_html = f"""
        <div style='width:340px; height:340px; display:flex; align-items:center; justify-content:center;'>
          <div id="{wheel_id}" class='wheel' style='transform: rotate(0deg);'>
            {slice_html}
          </div>
        </div>
        <script>
        (function(){{
            const wheel = document.getElementById("{wheel_id}");
            // small delay to ensure element inserted, then animate
            setTimeout(function(){{
                wheel.style.transition = 'transform 4s cubic-bezier(0.33, 1, 0.68, 1)';
                wheel.style.transform = 'rotate({rotation_deg}deg)';
            }}, 100);
        }})();
        </script>
        """
        # show the wheel animation
        st.markdown(wheel_html, unsafe_allow_html=True)
        # wait for the animation to finish on the python side before showing result
        time.sleep(4.4)
        st.success(f"Result: {options[chosen_idx]}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # initial idle wheel (not spun yet) - show static wheel with labels
        uid = random.randint(100000, 999999)
        wheel_id = f"wheel_static_{uid}"
        slice_html = ""
        seg = 360 / n
        colors = ["#3b82f6", "#60a5fa"]
        for i, lab in enumerate(labels):
            rot = i * seg
            color = colors[i % len(colors)]
            slice_html += f"<div class='slice' style='transform: rotate({rot}deg) translate(-50%, -100%);'><span style='background:{color}; padding:18px 8px;'>{lab}</span></div>"
        wheel_static = f"""
        <div style='width:340px; height:340px; display:flex; align-items:center; justify-content:center;'>
          <div id="{wheel_id}" class='wheel' style='transform: rotate(0deg);'>
            {slice_html}
          </div>
        </div>
        """
        st.markdown(wheel_static, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close wrapper
    st.markdown("</div>", unsafe_allow_html=True)

# Reasons page (all shown)
elif page == "Reasons I Love You 💌":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Reasons I Love You 💌")
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
        st.markdown(f"**Reason {i}:** {r}")
    st.markdown("</div>", unsafe_allow_html=True)

# Photos & Polaroids
elif page == "Photos & Polaroids 📸":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Photos & Polaroids 📸")
    st.write("Upload photos and captions; they'll be shown as polaroid cards.")
    uploaded = st.file_uploader("Upload a photo (jpg/png)", type=["jpg","jpeg","png"])
    caption = st.text_input("Caption for this photo")
    if st.button("Save photo"):
        if uploaded:
            fname = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded.name}"
            with open(PHOTOS_DIR / fname, "wb") as f:
                f.write(uploaded.getbuffer())
            # register in timeline.json
            tpath = DATA_DIR / "timeline.json"
            tl = json.loads(tpath.read_text()) if tpath.exists() and tpath.read_text().strip() else []
            tl.append({"type":"photo","file": str(PHOTOS_DIR / fname), "caption": caption, "date": datetime.now().isoformat()})
            tpath.write_text(json.dumps(tl, ensure_ascii=False, indent=2))
            st.success("Photo saved as Polaroid 💙")
        else:
            st.warning("Please choose a photo first.")
    # Show gallery
    tpath = DATA_DIR / "timeline.json"
    tl = json.loads(tpath.read_text()) if tpath.exists() and tpath.read_text().strip() else []
    photos = [e for e in tl if e.get("type")=="photo"]
    if photos:
        cols = st.columns(3)
        for i, p in enumerate(reversed(photos)):
            try:
                with cols[i % 3]:
                    st.markdown(f"<div class='polaroid'><img src='{p['file']}' /><div class='caption'>{p.get('caption','')}</div></div>", unsafe_allow_html=True)
            except Exception:
                pass
    st.markdown("</div>", unsafe_allow_html=True)

# Timeline
elif page == "Our Story Timeline 🕰️":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Our Story Timeline 🕰️")
    tpath = DATA_DIR / "timeline.json"
    tl = json.loads(tpath.read_text()) if tpath.exists() and tpath.read_text().strip() else []
    with st.form("mem"):
        title = st.text_input("Title")
        date = st.date_input("Date")
        desc = st.text_area("Short description")
        submit = st.form_submit_button("Add memory")
        if submit:
            tl.append({"type":"memory","title":title,"date":str(date),"desc":desc})
            tpath.write_text(json.dumps(tl, ensure_ascii=False, indent=2))
            st.success("Memory saved 💙")
    memories = [m for m in tl if m.get("type")=="memory"]
    for m in sorted(memories, key=lambda x: x.get("date",""), reverse=True):
        st.subheader(f"{m.get('title')} — {m.get('date')}")
        st.write(m.get("desc"))
        st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

# Settings
elif page == "Settings ⚙️":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Settings & Uploads ⚙️")
    st.write("Upload the 'miss me' voice note, add songs, or clear saved data.")
    # voice upload
    audio = st.file_uploader("Upload voice clip (mp3/wav) for 'miss me'", type=["mp3","wav"])
    if st.button("Upload voice clip"):
        if audio:
            with open(DATA_DIR / "voice.mp3", "wb") as f:
                f.write(audio.getbuffer())
            st.success("Voice clip uploaded 💙")
        else:
            st.warning("Choose a file first.")
    # songs add
    st.markdown("----")
    st.subheader("Add a song")
    s_title = st.text_input("Song title")
    s_link = st.text_input("Link (spotify/youtube) - optional")
    s_note = st.text_area("Why it matters (short note)")
    if st.button("Add song"):
        sp = DATA_DIR / "songs.json"
        songs = json.loads(sp.read_text()) if sp.exists() and sp.read_text().strip() else []
        songs.append({"title": s_title, "link": s_link, "note": s_note})
        sp.write_text(json.dumps(songs, ensure_ascii=False, indent=2))
        st.success("Song added 💙")
    # clear data
    st.markdown("----")
    if st.button("Clear all saved data (photos, notes, timeline, songs)"):
        # careful: permanently clears runtime files for this deployment
        for fname in ["notes.json","songs.json","timeline.json"]:
            (DATA_DIR / fname).write_text("[]")
        for f in PHOTOS_DIR.glob("*"):
            try:
                f.unlink()
            except Exception:
                pass
        st.success("Cleared saved data on this instance.")
    st.markdown("</div>", unsafe_allow_html=True)
