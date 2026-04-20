import streamlit as st
from groq import Groq
import re

# ---------------- CONFIG ----------------
st.set_page_config(layout="wide", page_title="Heart AI", page_icon="❤️")

# ---------------- API ----------------
API_KEY = "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"

client = Groq(api_key=API_KEY)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Page background */
body, .main, section.main {
    background-color: #0b1220;
}

/* Chat input container (outer bar) */
.stChatInput > div {
    background-color: #2b2b2b !important;   /* main color */
    border-radius: 30px;
    padding: 12px 18px;
    border: none !important;
    box-shadow: none !important;
}

/* Input field (MAKE SAME COLOR) */
.stChatInput input {
    background-color: #2b2b2b !important;   /* SAME as outer */
    border: none !important;
    outline: none !important;
    color: #e5e7eb !important;
    font-size: 15px;
}

/* Placeholder */
.stChatInput input::placeholder {
    color: #9ca3af !important;
}

/* Remove ALL inner differences */
.stChatInput * {
    box-shadow: none !important;
}

/* Send button */
.stChatInput button {
    background-color: transparent !important;
    color: #d1d5db !important;
    border-radius: 50%;
}

</style>
""", unsafe_allow_html=True)
# ---------------- SESSION ----------------
if "chats" not in st.session_state:
    st.session_state.chats = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = {"title": "New Chat", "messages": []}

# ---------------- SIDEBAR ----------------
# ---------------- SIDEBAR ----------------
with st.sidebar:

    # LOGO (unchanged)
    st.markdown("""
        <div style="margin-top:-30px; margin-bottom:15px; display:flex; align-items:center;">
            <img src="https://img.freepik.com/premium-vector/heart-logo_946691-365.jpg"
                 width="32"
                 style="border-radius:6px;">
            <span style="font-size:18px; font-weight:600; margin-left:8px;">
                Heart AI
            </span>
        </div>
    """, unsafe_allow_html=True)

    # NEW CHAT (unchanged)
    if st.button("➕  New chat", key="new_chat_btn"):
        if st.session_state.current_chat["messages"]:
            st.session_state.chats.append(st.session_state.current_chat)

        st.session_state.current_chat = {"title": "New chat", "messages": []}
        st.rerun()

    # SHARE (below new chat ✅)
    if st.button("🔗  Share", key="share_btn"):
        st.toast("Link copied (demo)")

    # 🔍 SEARCH CHAT (NEW)
    search_query = st.text_input("Search chat", placeholder="Search...")

    st.markdown("---")
    st.markdown("### Recents")

    # HISTORY with search filter
    for i, chat in enumerate(st.session_state.chats):
        if search_query.lower() in chat["title"].lower():
            if st.button(chat["title"], key=f"chat_{i}"):
                st.session_state.current_chat = chat
                st.rerun()
# ---------------- MAIN ----------------
# ---------------- DISPLAY CHAT ----------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.current_chat["messages"]:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='text-align:right; margin:10px 0;'>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align:left; margin:10px 0;'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)
# ---------------- BPM FUNCTION ----------------
def extract_bpm(text):
    numbers = re.findall(r'\d+', text)
    return int(numbers[0]) if numbers else None

# ---------------- INPUT ----------------
user_input = st.chat_input(" ask a question...")

if user_input:
    st.session_state.current_chat["messages"].append({"role": "user", "content": user_input})

    # Set chat title from first message
    if len(st.session_state.current_chat["messages"]) == 1:
        st.session_state.current_chat["title"] = user_input[:40]

    bpm = extract_bpm(user_input)

    if bpm:
        if bpm < 60:
            response = f"Low BPM ({bpm}). Take rest."
        elif 60 <= bpm <= 100:
            response = f"Normal BPM ({bpm}). Good condition."
        else:
            response = f"High BPM ({bpm}). Relax and consult doctor."
    else:
        try:
            res = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": user_input}]
            )
            response = res.choices[0].message.content
        except:
            response = "Error connecting to AI."

    st.session_state.current_chat["messages"].append({"role": "assistant", "content": response})

    st.rerun()
