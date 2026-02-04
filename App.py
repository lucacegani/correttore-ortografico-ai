import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configurazione API
api_key = st.secrets["api_key"].strip()
genai.configure(api_key=api_key)

# --- STILE "AI STUDIO" ---
st.set_page_config(page_title="Gemini AI Studio - School Edition", layout="wide")

# CSS personalizzato per emulare i colori di Google
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1a73e8; color: white; }
    .stTextArea textarea { border-radius: 10px; border: 1px solid #dadce0; }
    .sidebar .sidebar-content { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Come in AI Studio) ---
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d47353039331e16a02ad.svg", width=50)
    st.title("Settings")
    model_choice = st.selectbox("Model", ["gemini-2.5-flash", "gemini-1.5-pro"])
    temp = st.slider("Temperature", 0.0, 2.0, 0.7)
    st.info("Queste impostazioni controllano quanto il Maestro è 'creativo'.")

# --- MAIN INTERFACE ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Input")
    user_text = st.text_area("System Instructions / User Prompt", 
                             placeholder="Scrivi qui il compito o le istruzioni...", 
                             height=300)
    uploaded_file = st.file_uploader("Upload Image (OCR)", type=['png', 'jpg', 'jpeg'])

with col2:
    st.subheader("Run & Output")
    if st.button("Run Model"):
        if not user_text and not uploaded_file:
            st.error("Inserisci un testo o un'immagine.")
        else:
            model = genai.GenerativeModel(model_choice)
            with st.spinner("Generating..."):
                # Logica di invio
                prompt = "Sei un maestro di primaria. Correggi e spiega: "
                content = [prompt + user_text]
                if uploaded_file:
                    content.append(Image.open(uploaded_file))
                
                response = model.generate_content(content)
                
                st.markdown("### Response")
                st.write(response.text)
                
                # Tasto Audio integrato nello stile
                clean_text = response.text.replace('"', '').replace("'", "").replace("\n", " ").replace("*", "")
                st.components.v1.html(f"""
                    <button onclick="window.speechSynthesis.speak(new SpeechSynthesisUtterance('{clean_text}'))" 
                    style="width:100%; padding:10px; background:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">
                    🔊 Play Response
                    </button>
                """, height=50)
