import streamlit as st
from datetime import datetime
import os, sys
HERE = os.path.abspath(os.path.dirname(__file__))      
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, ".."))  
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from backend.app.config import REQUEST_TIMEOUT
from backend.app.config import ALLOWED_MODELS

MODEL_CHOICES = sorted(list(ALLOWED_MODELS))

import requests
import re
import html

st.set_page_config(
    page_title="ekm AI – Multi Model Chat",
    page_icon="😎",
)

def handle_thinking_tags(text, show):
    if show:
        return re.sub(
            r"<think>(.*?)</think>",
            lambda m: f'<div style="color:gray;font-style:italic;">🧠 {html.escape(m.group(1))}</div>',
            text,
            flags=re.DOTALL,
        )
    else:
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)


def chat():
    # --- Typing Header ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap');

        .title-container {
            font-family: 'Inter', sans-serif;
            font-size: 2.2em;
            font-weight: 600;
            color: white;
            display: flex;
            align-items: flex-start;
        }

        .typewriter {
            overflow: hidden;
            white-space: nowrap;
            border-right: .12em solid #ffffff55;
            width: 0;
            animation: typing 2s steps(20, end) forwards;
        }

        .beta {
            font-size: 0.5em;
            color: #aaa;
            position: relative;
            top: -0.5em;
            margin-left: 5px;
            opacity: 0;
            animation: fadeIn 0.3s ease forwards;
            animation-delay: 2s;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 17.8ch; } 
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        </style>

        <div class="title-container">
            <div class="typewriter">Welcome to The ekm AI!</div>
            <div class="beta">β</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # --- API URL ---
    BACKEND_URL = os.environ.get(
    "BACKEND_URL",
    "http://127.0.0.1:8000/chat"  # fallback for local dev
)
    # --- Sidebar ---
    st.sidebar.title("🎛️ Quick Actions")

    # Model selection
    ekm_model = st.sidebar.selectbox("🧠 Choose Model", MODEL_CHOICES)
    show_thinking = st.sidebar.checkbox(" Show AI Thinking", value=False)

    # Divider
    st.sidebar.markdown("---")

    # Model info + Clear Chat
    st.sidebar.markdown(f"**📊 Current Model:**")
    st.sidebar.markdown(f"`{ekm_model}`")
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.messages = []

    # Divider
    st.sidebar.markdown("---")

    # Help & Feedback section
    with st.sidebar.expander("💬 Help & Feedback", expanded=False):
        st.markdown("💡 **Tips for Best Results:**")
        st.markdown("- Keep your prompt short and clear.\n- Avoid long or vague input.\n- You can switch models anytime.")
        st.markdown("📩 [Send Feedback](https://t.me/ekam_ai)")

    # Support Us section (separate expander)
    with st.sidebar.expander("💖 Support Us", expanded=False):
         st.markdown("""
    _Love what you see?_ 
    Keep ekm AI thriving with your support.  
    - **Ko-fi**: [Support us here](https://ko-fi.com/yourpage)  
    - **UPI**: ``your-upi@bank``
    """)

    # Divider
    st.sidebar.markdown("---")

    # Android App Button
    st.sidebar.link_button("📱 Download Android App", "https://your-apk-link.com")

    # Divider
    st.sidebar.markdown("---")

    # Horizontal Navigation Buttons
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🏠 Home"):
            navigate("home")

    with col2:
        if st.button("ℹ️ About"):
            navigate("about")

    # --- Fetching from Backend ---
    def fetch_ekm_data(user_req: str, ekm_model: str):
        try:
            payload = {
                "model": ekm_model,
                "messages": st.session_state.messages,
            }
            response = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return response.json().get("res", "⚠️ Unexpected response format.")
            elif response.status_code == 429:
                return "⚠️ Too many requests — slow down. (429)"
            else:
                return f"❌ Error {response.status_code}: {response.text}"
            
        except requests.exceptions.Timeout:
            return "❌ Request timed out. Try again later."
    
        except Exception as e:
            return f"❌ Failed to reach backend: {e}"

    # --- Session Memory ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "busy" not in st.session_state:
        st.session_state.busy = False
    
    prompt = st.chat_input("Ask..?", disabled=st.session_state.busy)    

    # --- Render Chat History ---
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(handle_thinking_tags(msg["content"], show_thinking))

    # --- Handle New Prompt ---
    if prompt and not st.session_state.busy:
        st.session_state.busy = True
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("thinking...", show_time=True):
                final_res = fetch_ekm_data(
                    user_req=prompt,
                    ekm_model=ekm_model,
                )
                st.markdown(handle_thinking_tags(final_res, show_thinking), unsafe_allow_html=True) # can be risky
                st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
        <span style="font-size: 12px; color: #bbb;">
            • <b>Model:</b>
            <span style="background-color: #1e1e1e; color: #8ef08e; padding: 2px 6px; border-radius: 6px; font-size: 11px; margin-left: 4px;">
                {ekm_model}
            </span>
        </span>
        <span style="font-size: 11px; color: #777;">{datetime.now().strftime("%H:%M")}</span>
    </div>
""", unsafe_allow_html=True)

        # --- Save assistant reply ---
        st.session_state.messages.append({
            "role": "assistant",
            "content": final_res
        })
        st.session_state.busy = False

# --- Session Default ---
if "page" not in st.session_state:
    st.session_state.page = "home"


# --- Navigation Helper ---
def navigate(page_name):
    st.session_state.page = page_name

# --- Page functions ---
def home():
    st.markdown("""
        <style>
            .hero-title {
                font-size: 2.5em;
                font-weight: 800;
                color: white;
                text-align: center;
                margin-top: 1em;
                margin-bottom: 0.2em;
            }

            .hero-subtitle {
                text-align: center;
                font-size: 1.2em;
                color: #cccccc;
                margin-bottom: 2em;
            }

            .video-container {
                display: flex;
                justify-content: center;
                margin-bottom: 1.5em;
            }

            .rounded-video {
                border-radius: 18px;
                overflow: hidden;
                width: 100%;
                max-width: 700px;
                aspect-ratio: 16/9;
            }

            .chat-cta-wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 20vh;
                margin-bottom: 1em;
            }

            .chat-cta-btn {
                padding: 0.6em 1.5em;
                font-size: 1.1em;
                border-radius: 10px;
                background-color: #222;
                color: white;
                border: 1px solid #444;
                transition: 0.2s ease;
            }

            .chat-cta-btn:hover {
                background-color: #333;
                border-color: #666;
            }

            .glass-box {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 18px;
                padding: 1.5em;
                text-align: center;
                transition: transform 0.2s ease, background 0.3s ease;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
            }

            .glass-box:hover {
                transform: scale(1.02);
                background: rgba(255, 255, 255, 0.08);
            }

            .footer-text {
                text-align: center;
                color: #999;
                margin-top: 3em;
                font-size: 0.9em;
            }
        </style>
    """, unsafe_allow_html=True)

    # HERO SECTION
    st.markdown("<div class='hero-title'>🚀 ekm AI – Access multiple models without login</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>Start instantly. No sign-up, no data stored. Just ask.</div>", unsafe_allow_html=True)

    # VIDEO SECTION
    st.markdown("""
        <div class="video-container">
            <div class="rounded-video">
                <iframe width="100%" height="100%" src="https://www.youtube.com/embed/9mhf7VWo_8o"
                    title="ekm AI Intro" frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen></iframe>
            </div>
        </div>
    """, unsafe_allow_html=True)
   
    st.markdown("####")

   # CTA BUTTON CENTERED
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💬 Let's Chat with ekm AI", key="cta-btn"):
            navigate("chat")

    st.markdown("####")        

    # FEATURES SECTION
    st.markdown("### 🔍 What Makes ekm AI Different?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="glass-box">
                🧠 <b>Private by Design</b><br>
                Your chats stay on this session. No data is stored or tracked.
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="glass-box">
                🧬 <b>Multiple AI Models</b><br>
                Switch between different large language models in one interface.
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="glass-box">
                🚪 <b>No Sign-Up Required</b><br>
                Open ekm AI and start chatting — no accounts or barriers.
            </div>
        """, unsafe_allow_html=True)

    # FOOTER
    st.markdown("""
        <div class="footer-text">
            Built with 🧠 and ❤️ by ekm AI Devs.  
            <br>Fully open-source. Contributions welcome.
        </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("🏠 Home")

        st.markdown("---")

        # 📱 Android App Download
        st.markdown("### 📱 Android App")
        st.markdown("_Take ekm AI everywhere you go._")
        st.link_button("⬇️ Download on Android", "https://your-apk-link.com")

        st.markdown("___")  # divider

        # 💖 Support Us
        st.markdown("### 💖 Support Us")
        st.markdown("""
    _Love what you see?_ Keep ekm AI thriving with your support.  
    - **Ko-fi**: [Support us here](https://ko-fi.com/yourpage)  
    - **UPI**: ``your-upi@bank``
    """)

        st.markdown("___")  # divider

        # 🧑‍💻 GitHub
        st.markdown("### 🧑‍💻 GitHub")
        st.markdown("""
    _Join our growing developer community._  
                    
    Contribute code, open issues, or simply give us a ⭐ to boost visibility!
    """)
        st.link_button("✨ GitHub Visit", "https://github.com/ekam-labs")

        st.markdown("___")  # divider

        # Bottom row: Telegram + About Us
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📢 Telegram", "https://t.me/ekam_ai")
        with col2:
            if st.button("ℹ️ About Us"):
                navigate("about")

def about():
    st.title("👨‍💻 About Us")

    st.markdown("""
    ekm AI is an **open-source**, privacy-first chatbot interface that allows users to access multiple AI models
    without needing to sign up or share any data.

    Our mission is to empower users and developers with tools that are:
    - ⚡ Fast and accessible
    - 🔓 Transparent and open
    - 🌐 Built for a global community

    You can find more about supporting us or contributing via the links in the sidebar.
    """)

    st.markdown("---")
    st.markdown("## 🤝 Our Partners")
    partner_col1, partner_col2 = st.columns(2)

    # --- Partner: TechLoop ---
    with partner_col1:
        st.markdown("### TXXL")
        st.image("https://yt3.googleusercontent.com/_YQkfoRHZqVCixmfk2n_hlSHMjJDbt7hpjXc4uJxvn9Fn6eQx_uFbaJxyLsrX85VeazBFeXzFA=s160-c-k-c0x00ffffff-no-rj", width=120)
        st.link_button("📺 YouTube", "https://youtube.com/@txlextended", use_container_width=True)
        st.link_button("📢 Telegram", "https://t.me/txlextended", use_container_width=True)

    # --- Partner: APW ---
    with partner_col2:
        st.markdown("### APW")
        st.image("https://yt3.googleusercontent.com/L4Uq1N633hzcnBSTE442q6BVQeiuSAO8qDfI6KDy8R9LrGTsuBItst5a83qkRaNdOJOUYhP9_bA=s160-c-k-c0x00ffffff-no-rj", width=120)
        st.link_button("📺 YouTube", "https://youtube.com/@androidportworld", use_container_width=True)
        st.link_button("📢 Telegram", "https://t.me/apw", use_container_width=True)

    st.divider()

    st.markdown("## 📬 Contact Us")
    contact_col1, contact_col2 = st.columns([1, 1])

    with contact_col1:
        st.link_button("📢 YouTube", "https://youtube.com/@ekamlabs", use_container_width=True)

    with contact_col2:
        st.link_button("📢 Telegram", "https://t.me/ekam_ai", use_container_width=True)

    # --- Sidebar ---
    with st.sidebar:
        st.title("🪄 ekm AI")

        if st.button("🏠 Home"):
            navigate("home")
        if st.button("💬 Chat"):
            navigate("chat")

        st.markdown("---")

        # 💖 Support Us
        st.markdown("### 💖 Support Us")
        st.markdown("""
    _Love what you see?_ Keep ekm AI thriving with your support.  
    - **Ko-fi**: [Support us here](https://ko-fi.com/yourpage)  
    - **UPI**: ``your-upi@bank``
    """)

        st.markdown("---")

        # 🧑‍💻 GitHub
        st.markdown("### 🧑‍💻 GitHub")
        st.markdown("""
    _Join our growing developer community._  
                    
    Contribute code, open issues, or simply give us a ⭐ to boost visibility!
    """)
        st.link_button("✨ GitHub Visit", "https://github.com/ekam-labs")

        st.markdown("---")

        # 📱 Android App Download
        st.markdown("### 📱 Android App")
        st.markdown("_Take ekm AI everywhere you go._")
        st.link_button("⬇️ Download on Android", "https://your-apk-link.com")


  # --- RENDER CURRENT PAGE ---
if st.session_state.page == "home":
    home()
elif st.session_state.page == "chat":
    chat()
elif st.session_state.page == "about":
    about()
