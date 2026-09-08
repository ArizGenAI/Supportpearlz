"""SupportPearlz — OpenAI-powered Streamlit support UI."""
from __future__ import annotations

import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="SupportPearlz — Pearlz Home Systems", page_icon="💧", layout="wide")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
[data-testid="stAppViewContainer"] { background:linear-gradient(180deg,#f6fbfc 0%,#ffffff 42%); }
[data-testid="stHeader"] { background:transparent; }
.block-container { max-width:1180px; padding:2rem 2rem 4rem; }
.brand { display:flex; align-items:center; gap:14px; margin:4px 0 28px; }
.brand-mark { width:46px; height:46px; border-radius:15px; display:grid; place-items:center; background:linear-gradient(135deg,#0d8294,#29c5ca); color:white; font-size:23px; box-shadow:0 10px 24px rgba(13,130,148,.20); }
.brand-name { font-family:'Plus Jakarta Sans',sans-serif; font-size:20px; font-weight:800; color:#10212b; line-height:1.05; }
.brand-sub { font-size:12px; color:#78909a; margin-top:4px; }
.hero { padding:34px 36px 30px; border:1px solid #e1ecef; border-radius:28px; background:radial-gradient(circle at 90% 0%,#dff7f8 0,#f8fcfc 34%,#fff 70%); box-shadow:0 18px 50px rgba(26,72,84,.07); margin-bottom:24px; }
.hero-kicker { color:#0d8294; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:.12em; }
.hero h1 { font-family:'Plus Jakarta Sans',sans-serif; color:#10212b; font-size:38px; line-height:1.12; margin:8px 0 10px; }
.hero p { color:#61727d; max-width:700px; font-size:15px; margin:0; }
.card { border:1px solid #e6edf0; border-radius:20px; background:#fff; padding:18px 20px; min-height:112px; box-shadow:0 8px 26px rgba(20,58,68,.04); }
.card-title { font-weight:700; color:#10212b; margin-bottom:6px; }
.card-text { color:#61727d; font-size:13px; line-height:1.55; }
[data-testid="stSidebar"] { background:#fbfdfd; border-right:1px solid #e6edf0; }
[data-testid="stChatMessage"] { border-radius:18px; margin:10px 0; }
[data-testid="stChatMessageContent"] { font-size:15px; line-height:1.65; }
.stButton > button { border-radius:12px; font-weight:600; }
.footer-note { text-align:center; color:#8a9aa2; font-size:12px; margin-top:26px; }
</style>""", unsafe_allow_html=True)

SYSTEM_PROMPT = """You are SupportPearlz, a helpful customer support assistant for Pearlz Home Systems. Answer clearly and professionally. Help with product questions, troubleshooting, warranty, service, orders, shipping, returns, maintenance, and filters. If the user asks for information you do not know, say that you don't have enough information instead of inventing company-specific facts."""


def get_api_key() -> str:
    try:
        secret_key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        secret_key = ""
    return secret_key or os.getenv("OPENAI_API_KEY", "")


def ask_openai(question: str, history: list[dict[str, str]], api_key: str) -> str:
    client = OpenAI(api_key=api_key)
    input_messages = [{"role": "developer", "content": SYSTEM_PROMPT}]
    input_messages.extend(history[-12:])
    input_messages.append({"role": "user", "content": question})
    response = client.responses.create(model="gpt-5.6-luna", input=input_messages)
    return response.output_text


def main() -> None:
    st.markdown("""<div class="brand"><div class="brand-mark">💧</div><div><div class="brand-name">SupportPearlz</div><div class="brand-sub">Pearlz Home Systems · Customer Support</div></div></div><section class="hero"><div class="hero-kicker">AI customer support</div><h1>How can we help today?</h1><p>Ask questions about Pearlz products, troubleshooting, warranty, service, orders, shipping, filters, and more.</p></section>""", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 💧 SupportPearlz")
        st.caption("Connect your OpenAI API key to activate AI responses.")
        st.divider()
        st.markdown("**Step 1 · OpenAI API key**")
        saved_key = get_api_key()
        api_key = st.text_input("API key", value="", type="password", placeholder="sk-...", help="For local use, you can also set OPENAI_API_KEY in Streamlit secrets or environment variables.")
        api_key = api_key.strip() or saved_key
        if api_key:
            st.success("OpenAI connected", icon="✅")
        else:
            st.info("Enter your API key to enable the chat.")
        st.divider()
        if st.button("🔄 Reset conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    c1, c2, c3 = st.columns(3)
    for col, title, text in [
        (c1, "🔧 Troubleshooting", "Get guided help for common product issues and symptoms."),
        (c2, "🛡️ Warranty & service", "Ask about warranty, maintenance, and service."),
        (c3, "📦 Orders & shipping", "Ask about orders, shipping, returns, and documentation."),
    ]:
        with col:
            st.markdown(f'<div class="card"><div class="card-title">{title}</div><div class="card-text">{text}</div></div>', unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if not st.session_state.messages:
        st.markdown("<div style='color:#71828b;font-size:13px;margin:24px 0 8px;font-weight:600'>Try asking</div>", unsafe_allow_html=True)
        prompts = ["What does my warranty cover?", "How do I troubleshoot my AquaPearl 500?", "What is the filter replacement process?"]
        cols = st.columns(3)
        for col, prompt in zip(cols, prompts):
            with col:
                if st.button(prompt, use_container_width=True):
                    if not api_key:
                        st.warning("Please enter your OpenAI API key in the sidebar first.")
                    else:
                        with st.spinner("Preparing your support response..."):
                            try:
                                answer = ask_openai(prompt, st.session_state.messages, api_key)
                                st.session_state.messages.extend([{"role":"user", "content":prompt}, {"role":"assistant", "content":answer}])
                                st.rerun()
                            except Exception as exc:
                                st.error(f"Unable to get a response from OpenAI: {exc}")

    question = st.chat_input("Ask about your Pearlz product, warranty, shipping, filters...")
    if question:
        if not api_key:
            st.warning("Please enter your OpenAI API key in the sidebar first.")
        else:
            with st.spinner("Preparing your support response..."):
                try:
                    answer = ask_openai(question, st.session_state.messages, api_key)
                    st.session_state.messages.extend([{"role":"user", "content":question}, {"role":"assistant", "content":answer}])
                    st.rerun()
                except Exception as exc:
                    st.error(f"Unable to get a response from OpenAI: {exc}")

    st.markdown("<div class='footer-note'>SupportPearlz · Powered by OpenAI · Keep your API key private.</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
