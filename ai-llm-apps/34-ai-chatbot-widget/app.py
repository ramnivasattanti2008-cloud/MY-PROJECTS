import streamlit as st
import os
import google.genai as genai

st.set_page_config(page_title="AI Chatbot Widget Builder", page_icon="🤖", layout="centered")
st.markdown("""
<style>
.stApp{background:#0e0e1a}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:#1a1a2e;color:#e0e0e0;border:1px solid #444}
.stButton>button{background:linear-gradient(135deg,#a29bfe,#74b9ff);color:#fff;border:none;border-radius:8px;padding:.5rem 1.5rem;font-weight:700;font-size:1rem}
h1,h2,h3{color:#dfe6e9!important}
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Chatbot Widget Builder")
st.markdown("*Customize your AI chatbot personality and get embeddable HTML*")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Set `GEMINI_API_KEY` environment variable to use this app.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

with st.sidebar:
    st.header("🎨 Widget Configuration")
    bot_name = st.text_input("Bot Name", value="AI Assistant")
    bot_personality = st.selectbox("Personality", ["Friendly", "Professional", "Casual", "Witty", "Expert", "Supportive"])
    primary_color = st.color_picker("Primary Color", "#6c63ff")
    avatar_emoji = st.text_input("Avatar Emoji", value="🤖", max_chars=3)
    welcome_msg = st.text_input("Welcome Message", value="Hi! How can I help you today?")

# Build HTML widget
def build_widget_html(name, personality, color, emoji, welcome):
    return f"""<!-- {name} Chatbot Widget -->
<div id="ai-chatbot-{name.lower().replace(' ','-')}" style="position:fixed;bottom:20px;right:20px;z-index:9999;font-family:Arial,sans-serif">
  <div id="chat-window-{name.lower().replace(' ','-')}" style="display:none;width:360px;max-height:500px;background:#1a1a2e;border-radius:16px;box-shadow:0 8px 32px rgba(0,0,0,0.5);overflow:hidden;flex-direction:column;border:1px solid {color}33">
    <div style="background:{color};padding:16px 20px;display:flex;align-items:center;gap:10px">
      <span style="font-size:24px">{emoji}</span>
      <div><div style="color:#fff;font-weight:700;font-size:16px">{name}</div><div style="color:#fff9;border-radius:8px;font-size:11px;opacity:0.8">{personality} Assistant</div></div>
      <button onclick="document.getElementById('chat-window-{name.lower().replace(' ','-')}').style.display='none'" style="margin-left:auto;background:rgba(255,255,255,0.2);border:none;color:#fff;border-radius:50%;width:28px;height:28px;cursor:pointer;font-size:16px;line-height:1">×</button>
    </div>
    <div id="chat-messages-{name.lower().replace(' ','-')}" style="flex:1;padding:16px;overflow-y:auto;max-height:340px;min-height:200px">
      <div style="background:#2d2d44;padding:10px 14px;border-radius:12px 12px 12px 4px;color:#e0e0e0;font-size:14px;margin-bottom:8px;max-width:85%">{welcome}</div>
    </div>
    <div style="padding:12px 16px;background:#12121f;border-top:1px solid #333;display:flex;gap:8px">
      <input id="chat-input-{name.lower().replace(' ','-')}" placeholder="Ask {name}..." style="flex:1;background:#2d2d44;border:1px solid #444;color:#e0e0e0;padding:10px 14px;border-radius:24px;font-size:14px;outline:none" onkeydown="if(event.key==='Enter'){{sendMessage{name.lower().replace(' ','_')}()}}"/>
      <button onclick="sendMessage{name.lower().replace(' ','_')}()" style="background:{color};border:none;color:#fff;border-radius:50%;width:42px;height:42px;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center">▶</button>
    </div>
  </div>
  <button onclick="toggleChat{name.lower().replace(' ','_')}()" style="background:{color};border:none;color:#fff;width:60px;height:60px;border-radius:50%;cursor:pointer;font-size:28px;box-shadow:0 4px 16px {color}66;display:flex;align-items:center;justify-content:center">{emoji}</button>
</div>
<script>
function toggleChat{name.lower().replace(' ','_')}(){{var w=document.getElementById('chat-window-{name.lower().replace(' ','-')}');w.style.display=w.style.display==='none'?'flex':'none'}}
function sendMessage{name.lower().replace(' ','_')}(){{
  var inp=document.getElementById('chat-input-{name.lower().replace(' ','-')}');var msgs=document.getElementById('chat-messages-{name.lower().replace(' ','-')}');
  var q=inp.value.trim();if(!q)return;
  msgs.innerHTML+='<div style="background:{color};padding:10px 14px;border-radius:12px 12px 4px 12px;color:#fff;font-size:14px;margin-bottom:8px;max-width:85%;margin-left:auto">'+q.replace(/</g,'&lt;')+'</div>';
  inp.value='';msgs.scrollTop=msgs.scrollHeight;
  // Note: Replace with your actual API call to backend
  msgs.innerHTML+='<div style="background:#2d2d44;padding:10px 14px;border-radius:12px 12px 12px 4px;color:#e0e0e0;font-size:14px;margin-bottom:8px;max-width:85%">⚙️ Connect this widget to your AI backend for real responses.</div>';
  msgs.scrollTop=msgs.scrollHeight;
}}
</script>"""

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎨 Live Preview")
    st.markdown(f"**Bot Name:** {bot_name}")
    st.markdown(f"**Personality:** {bot_personality}")
    st.markdown(f"**Avatar:** {avatar_emoji}")
    st.markdown(f"**Welcome:** {welcome_msg}")
    st.markdown(f"**Color:** {primary_color}")

with col2:
    st.subheader("🖥️ Widget Preview")
    preview_html = build_widget_html(bot_name, bot_personality, primary_color, avatar_emoji, welcome_msg)
    st.markdown(preview_html, unsafe_allow_html=True)

st.divider()
st.subheader("📋 Embeddable HTML Code")
st.code(preview_html, language="html")
st.button("📋 Copy HTML", on_click=lambda: st.toast("HTML copied to clipboard! (Paste manually)"))

st.divider()
st.subheader("💬 Test the Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": welcome_msg}]

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_msg = st.chat_input(f"Ask {bot_name}...")
if user_msg:
    st.session_state.chat_history.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    with st.spinner(f"{bot_name} is thinking..."):
        try:
            response = model.generate_content(
                f"You are a {bot_personality} AI assistant named {bot_name}. Respond conversationally. {welcome_msg}"
                f"\n\nUser: {user_msg}"
            )
            reply = response.text
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)
        except Exception as e:
            st.error(f"Error: {e}")

if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = [{"role": "assistant", "content": welcome_msg}]
    st.rerun()

st.caption("🔑 Uses Google Gemini — set `GEMINI_API_KEY` environment variable.")
