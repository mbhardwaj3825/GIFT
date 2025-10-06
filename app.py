import streamlit as st
import random
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="For My Anjuuu 💙", layout="centered")

# -------------------- CUSTOM STYLES --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #b3e5fc, #e1bee7, #bbdefb);
    background-attachment: fixed;
    background-size: cover;
    font-family: 'Poppins', sans-serif;
    color: #1e3a8a;
    overflow-x: hidden;
    position: relative;
}

/* faint animated hearts overlay */
body::before {
    content: "";
    background-image: url('https://i.imgur.com/Z1r5NnH.png');
    opacity: 0.15;
    background-repeat: repeat;
    background-size: 100px;
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    z-index: -1;
    animation: floatBg 20s linear infinite;
}
@keyframes floatBg {
    from {background-position: 0 0;}
    to {background-position: 0 200px;}
}

h1, h2, h3, h4 {
    text-align: center;
    color: #0f2167;
}

.card {
    background: rgba(255, 255, 255, 0.7);
    padding: 1.5rem;
    border-radius: 20px;
    margin: 1rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.stButton>button {
    background-color: #5fa8f7;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.6rem 1.4rem;
    font-size: 1rem;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #2563eb;
    transform: scale(1.05);
}

/* wheel */
.wheel-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}
#wheel {
    width: 260px;
    height: 260px;
    border-radius: 50%;
    border: 10px solid #2563eb;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(37,99,235,0.4);
    transition: transform 4s cubic-bezier(0.25, 0.1, 0.25, 1);
}
.segment {
    position: absolute;
    width: 50%;
    height: 50%;
    background-color: #60a5fa;
    transform-origin: 100% 100%;
    color: white;
    text-align: center;
    line-height: 130px;
    font-size: 14px;
}
.pointer {
    margin: 0 auto;
    width: 0; height: 0;
    border-left: 15px solid transparent;
    border-right: 15px solid transparent;
    border-bottom: 25px solid #1e3a8a;
    position: relative;
    top: -10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- LOGIN --------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def passcode_page():
    st.title("💌 For My Anjuuu 💙")
    st.write("Enter the secret code, my love 💫")
    code = st.text_input("🔒 Enter Passcode", type="password")
    if st.button("Unlock"):
        if code == "Iloveyouladuu":
            st.session_state.authenticated = True
            st.success("Welcome, my love 💙")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Oops! Wrong code 😔")

# -------------------- MAIN APP --------------------
def main_app():
    st.title("💞 For My Anjuuu 💞")
    st.write("Welcome to your special little world 💙")

    choice = st.radio("Choose what you want to see 💫",
                      ["Today's Thought", "Click Only If You Miss Me", "Our Songs", "Spin the Wheel of Love", "Reasons I Love You"])

    # ---------- TODAY’S THOUGHT ----------
    if choice == "Today's Thought":
        st.subheader("💭 Today's Thought")
        note = st.text_area("Write a note for me here 💌")
        if st.button("Save"):
            st.success("Saved with love 💙")

    # ---------- CLICK ONLY IF YOU MISS ME ----------
    elif choice == "Click Only If You Miss Me":
        st.subheader("💫 When you miss me 💫")
        if st.button("Reveal 💙"):
            st.markdown("<h4 style='text-align:center;'>“You’re my calm in the chaos, my favorite reason to smile.” 💞</h4>", unsafe_allow_html=True)

    # ---------- OUR SONGS ----------
    elif choice == "Our Songs":
        st.subheader("🎵 Our Songs 💙")
        songs = [
            ("Perfect — Ed Sheeran", "Because it’s literally us 💫"),
            ("Until I Found You — Stephen Sanchez", "Because that’s exactly how I feel."),
            ("Love Story — Taylor Swift", "Because we write our own story 💙")
        ]
        for title, reason in songs:
            st.markdown(f"<div class='card'><b>{title}</b><br><i>{reason}</i></div>", unsafe_allow_html=True)

    # ---------- SPIN THE WHEEL ----------
    elif choice == "Spin the Wheel of Love":
        st.subheader("🎡 Spin the Wheel of Love 💙")
        prizes = [
            "You get a hug 🤗",
            "Movie night 🎬",
            "You owe me ice cream 🍦",
            "Midnight call 💞",
            "A long drive date 🚗",
            "You get 10 kisses 😘"
        ]
        st.markdown("<div class='pointer'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='wheel-container'>
            <div id='wheel'>
                <div class='segment' style='transform: rotate(0deg) skewY(-30deg); background:#3b82f6;'>💙 Hug</div>
                <div class='segment' style='transform: rotate(60deg) skewY(-30deg); background:#60a5fa;'>🎬 Movie</div>
                <div class='segment' style='transform: rotate(120deg) skewY(-30deg); background:#3b82f6;'>🍦 Ice Cream</div>
                <div class='segment' style='transform: rotate(180deg) skewY(-30deg); background:#60a5fa;'>💞 Call</div>
                <div class='segment' style='transform: rotate(240deg) skewY(-30deg); background:#3b82f6;'>🚗 Drive</div>
                <div class='segment' style='transform: rotate(300deg) skewY(-30deg); background:#60a5fa;'>😘 Kisses</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Spin 🎡"):
            result = random.choice(prizes)
            st.markdown("""
            <style>
            #wheel { transform: rotate(1440deg); }
            </style>
            """, unsafe_allow_html=True)
            time.sleep(4)
            st.success(result)

    # ---------- REASONS I LOVE YOU ----------
    elif choice == "Reasons I Love You":
        st.subheader("💙 Reasons Why I Love You 💙")
        reasons = [
            "I love your personality","I love your smile","I love your hair","I love your smell",
            "I love your jolliness","I love your maturity","I love your childishness",
            "I love the way you balance","I love your futuristic vision","I love the way I am happy around you",
            "I love the way I am safe around you","I love that you communicate","I love that you try to solve things",
            "I love that you are emotionally available","I love your humour","I love your eyes","I love the way you listen",
            "I love that you remember details","I love the sense of security you give","I love your confidence",
            "I love your nature","I love the small gestures","I love your intelligence","I love your positive approach",
            "I love your dressing sense","I love that you never give up","I love how you respect others",
            "I love your humanity","I love how you understand","I love that family matters to you","I love your selflessness",
            "I love that you cry","I love your anger","I love your dance","I love your general knowledge",
            "I love that you love deeply","I love that you believe in God","I love that you learn","I love how you manage",
            "I love that you are foodie","I love your courage","I love your boundaries","I love your control",
            "I love your thoughtfulness","I love how you complete me","I love the way you say 'meri laduuu'",
            "I love the way you teach me","I love the priority you give","I love the support you give",
            "I love how you make me laugh","I love the way you love me","I love our friendship",
            "And most importantly, I love you 💙"
        ]
        for r in reasons:
            st.markdown(f"💖 {r}")

# -------------------- RUN --------------------
if not st.session_state.authenticated:
    passcode_page()
else:
    main_app()
