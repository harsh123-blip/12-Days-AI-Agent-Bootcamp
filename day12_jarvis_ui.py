import streamlit as st
import json
import time
import webbrowser
import pyautogui
from groq import Groq

# ==========================================
# 1. PAGE SETTING
# ==========================================
st.set_page_config(page_title="J.A.R.V.I.S. AI OS", page_icon="🤖", layout="wide")
pyautogui.FAILSAFE = True

st.title("🤖 J.A.R.V.I.S. — Grand Automation & Earning OS")
st.caption("Powered by Groq LPU • Stateful Agent Engine • Live OS Control")
st.markdown("---")

# ==========================================
# 2. OS TOOLS
# ==========================================
def open_app(app_name: str):
    pyautogui.press("win")
    time.sleep(0.5)
    pyautogui.write(app_name, interval=0.01)
    time.sleep(0.5)
    pyautogui.press("enter")
    return f"✅ '{app_name}' app chalu kar diya gaya hai."

def open_website(url: str):
    webbrowser.open(url)
    return f"🌐 '{url}' browser me khol diya gaya hai."

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open a desktop app like msedge, notepad, mspaint, calc",
            "parameters": {
                "type": "object",
                "properties": {"app_name": {"type": "string"}},
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "Open a website URL like https://youtube.com",
            "parameters": {
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"]
            }
        }
    }
]

# ==========================================
# 3. SIDEBAR
# ==========================================
with st.sidebar:
    st.header("⚙️ System Control Panel")
    api_key = st.text_input("🔑 Groq API Key Dalein:", type="password")
    
    st.markdown("---")
    st.subheader("⚡ 1-Click OS Actions")
    if st.button("🎨 MS Paint Kholein", use_container_width=True):
        st.toast(open_app("mspaint"))
        
    if st.button("💬 WhatsApp Web Kholein", use_container_width=True):
        st.toast(open_website("https://web.whatsapp.com"))
        
    if st.button("🗑️ Chat Memory Saaf Karein", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": "Tum Jarvis ho, ek futuristic computer automation assistant. Hindi me smart jawab do aur zarurat padne par tools chalao."}
        ]
        st.rerun()

# ==========================================
# 4. MEMORY
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Tum Jarvis ho, ek futuristic computer automation assistant. Hindi me smart jawab do aur zarurat padne par tools chalao."}
    ]

for msg in st.session_state.messages:
    if isinstance(msg, dict) and msg["role"] in ["user", "assistant"] and msg.get("content"):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# ==========================================
# 5. LIVE CHAT + TOOL ENGINE
# ==========================================
user_cmd = st.chat_input("Jarvis ko koi bhi aadesh dein (jaise: YouTube kholo ya Notepad kholo)...")

if user_cmd:
    if not api_key:
        st.error("⚠️ Pehle baayi taraf apni Groq API Key daalo!")
    else:
        st.session_state.messages.append({"role": "user", "content": user_cmd})
        with st.chat_message("user"):
            st.write(user_cmd)

        client = Groq(api_key=api_key)
        
        with st.spinner("🧠 Jarvis soch raha hai aur system check kar raha hai..."):
            res = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=st.session_state.messages,
                tools=tools_schema,
                tool_choice="auto"
            )
            ai_msg = res.choices[0].message

            if ai_msg and ai_msg.tool_calls:
                # Assistant ka tool call dict bana ke memory me daalo
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_msg.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                        } for tc in ai_msg.tool_calls
                    ]
                })

                for tool in ai_msg.tool_calls:
                    raw_args = tool.function.arguments or "{}"
                    args = json.loads(raw_args)
                    
                    if tool.function.name == "open_app":
                        output = open_app(args.get("app_name", "notepad"))
                    else:
                        output = open_website(args.get("url", "https://youtube.com"))
                        
                    st.toast(output)
                    st.session_state.messages.append({
                        "role": "tool",
                        "tool_call_id": tool.id,
                        "content": str(output)
                    })

                final = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=st.session_state.messages
                )
                reply_text = final.choices[0].message.content
            else:
                reply_text = ai_msg.content

            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            with st.chat_message("assistant"):
                st.write(reply_text)