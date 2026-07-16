import streamlit as st
import os
from groq import Groq
from datetime import datetime

# ============================================
# KONFIGURASI PAGE
# ============================================
st.set_page_config(
    page_title="Chatbot AI Kageyoru",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS - GLASSMORPHISM + GRADIENT
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background gradient animasi */
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Sidebar glassmorphism */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
}

/* Chat bubble user */
[data-testid="stChatMessage"] [data-testid="stChatMessageContent"]:has([data-testid="stMarkdownContainer"]) {
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px 20px 4px 20px;
    padding: 16px;
    color: #ffffff;
}

/* Chat bubble assistant */
[data-testid="stChatMessage"][data-testid="stChatMessage"]:nth-child(even) [data-testid="stChatMessageContent"] {
    background: rgba(99, 102, 241, 0.2) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 20px 20px 20px 4px;
    padding: 16px;
    color: #ffffff;
}

/* Input box */
[data-testid="stChatInput"] {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 16px;
    color: #ffffff;
}

/* Tombol */
.stButton > button {
    background: rgba(99, 102, 241, 0.3) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(99, 102, 241, 0.4) !important;
    border-radius: 12px;
    color: #ffffff !important;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: rgba(99, 102, 241, 0.5) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
}

/* Select box */
.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 12px;
    color: #ffffff !important;
}

/* Text color global */
h1, h2, h3, h4, h5, h6, p, label, span {
    color: #ffffff !important;
}

/* Scrollbar cantik */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
}

::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.5);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.8);
}

/* Quick prompt buttons */
div[data-testid="stHorizontalBlock"] button {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    height: auto !important;
    color: #e0e0e0 !important;
    font-size: 0.9rem !important;
    line-height: 1.4 !important;
    white-space: normal !important;
    text-align: left !important;
}

div[data-testid="stHorizontalBlock"] button:hover {
    background: rgba(99, 102, 241, 0.2) !important;
    border-color: rgba(99, 102, 241, 0.5) !important;
    color: #ffffff !important;
}

/* Avatar styling */
[data-testid="stChatMessageAvatar"] {
    background: rgba(99, 102, 241, 0.3) !important;
    border-radius: 50% !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# INISIALISASI GROQ CLIENT
# ============================================
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    st.error("⚠️ GROQ_API_KEY tidak ditemukan di environment variables!")
    st.stop()

# ============================================
# PERSONA SYSTEM PROMPT
# ============================================
PERSONAS = {
    "🧑‍💻 Programmer": "Kamu adalah programmer senior yang ramah. Jelaskan konsep coding dengan analogi sederhana. Gunakan bahasa Indonesia santai (aku/kamu). Hindari jargon berlebihan.",
    "🎬 Kreator Konten": "Kamu adalah kreator konten kreatif. Berikan ide konten, script, atau tips viral dengan gaya santai dan engaging. Bahasa Indonesia gaul tapi tetap sopan.",
    "📈 Analis Crypto": "Kamu adalah analis crypto yang realistis. Jelaskan analisis teknikal dengan bahasa sederhana. SELALU ingatkan bahwa ini bukan financial advice dan crypto sangat volatile.",
    "🤙 Teman Ngobrol": "Kamu adalah teman ngobrol santai. Jawab dengan gaya conversational, pakai bahasa Indonesia sehari-hari, dan sesekali kasih emoji. Jangan terlalu formal."
}

# ============================================
# MODEL OPTIONS
# ============================================
MODELS = {
    "⚡ Llama 3.1 8B (Cepat)": "llama-3.1-8b-instant",
    "🧠 Llama 3.3 70B (Pintar)": "llama-3.3-70b-versatile",
    "🔥 Mixtral 8x7B": "mixtral-8x7b-32768",
    "💎 Gemma 2 9B": "gemma2-9b-it"
}

# ============================================
# SESSION STATE
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = "🤙 Teman Ngobrol"

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "⚡ Llama 3.1 8B (Cepat)"

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan")
    
    # Pilih Persona
    persona = st.selectbox(
        "🎭 Persona AI",
        options=list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.selected_persona)
    )
    st.session_state.selected_persona = persona
    
    st.caption(f"*{persona}* aktif")
    
    st.divider()
    
    # Pilih Model
    model = st.selectbox(
        "🔧 Model AI",
        options=list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.selected_model)
    )
    st.session_state.selected_model = model
    
    st.divider()
    
    # Export Chat
    if st.session_state.messages:
        chat_history = ""
        for msg in st.session_state.messages:
            role = "User" if msg["role"] == "user" else "AI"
            chat_history += f"[{role}]\n{msg['content']}\n\n"
        
        st.download_button(
            label="📝 Export Chat",
            data=chat_history,
            file_name=f"chat_kageyoru_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
    
    # Clear Chat
    if st.button("🗑️ Hapus Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("**Ditenagai oleh:**")
    st.markdown("🚀 Groq  •  🦙 Llama 3  •  📊 Streamlit")

# ============================================
# HEADER
# ============================================
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 2.5rem; font-weight: 700; background: linear-gradient(90deg, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🤖 Chatbot AI Kageyoru
    </h1>
    <p style="color: rgba(255,255,255,0.6); font-size: 1rem; margin-top: -10px;">
        Asisten AI cepat & cerdas untuk berbagai kebutuhanmu
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# QUICK PROMPTS (Tampil kalau chat kosong)
# ============================================
if not st.session_state.messages:
    st.markdown("### 🎯 Mulai dengan pertanyaan ini:")
    
    quick_prompts = [
        "Jelaskan AI itu apa, tapi kayak aku umur 5 tahun",
        "Analisis teknikal BTC minggu ini gimana?",
        "Kasih ide konten TikTok tentang teknologi AI",
        "Bantu aku debug Python: list index out of range"
    ]
    
    cols = st.columns(2)
    for idx, prompt in enumerate(quick_prompts):
        with cols[idx % 2]:
            if st.button(prompt, key=f"quick_{idx}", use_container_width=True):
                # Simulate user input
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Get AI response
                try:
                    system_msg = PERSONAS[st.session_state.selected_persona]
                    groq_messages = [{"role": "system", "content": system_msg}]
                    for m in st.session_state.messages:
                        groq_messages.append({"role": m["role"], "content": m["content"]})
                    
                    response = client.chat.completions.create(
                        model=MODELS[st.session_state.selected_model],
                        messages=groq_messages,
                        temperature=0.7,
                        max_tokens=1024
                    )
                    
                    ai_response = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                except Exception as e:
                    st.session_state.messages.append({"role": "assistant", "content": f"Waduh, error: {str(e)}"})
                
                st.rerun()

# ============================================
# TAMPILKAN CHAT HISTORY
# ============================================
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# ============================================
# INPUT CHAT
# ============================================
if prompt := st.chat_input("Ketik pesanmu di sini..."):
    # Tambah pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    
    # AI Response dengan streaming
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            system_msg = PERSONAS[st.session_state.selected_persona]
            groq_messages = [{"role": "system", "content": system_msg}]
            
            for m in st.session_state.messages:
                groq_messages.append({"role": m["role"], "content": m["content"]})
            
            # Stream response
            stream = client.chat.completions.create(
                model=MODELS[st.session_state.selected_model],
                messages=groq_messages,
                temperature=0.7,
                max_tokens=1024,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Simpan ke session
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"Waduh, terjadi kesalahan: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})