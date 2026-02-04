import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Recupero API Key dai "Secrets" di Streamlit (Sicurezza)
api_key = st.secrets["api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Configurazione Pagina
st.set_page_config(page_title="Maestro Digitale 5^A", layout="centered")
st.title("📝 Il mio Assistente alla Scrittura")

# 3. Istruzioni di Sistema (Il Prompt che abbiamo deciso insieme)
system_prompt = """
Sei un maestro di scuola primaria. Se ricevi un'immagine, trascrivila. 
Poi correggi il testo (ortografia e grammatica) e aggiungi dei consigli gentili.
"""

# 4. Opzione OCR: Caricamento foto del quaderno
uploaded_file = st.file_uploader("📸 Carica la foto del tuo quaderno (opzionale)", type=['png', 'jpg', 'jpeg'])

# 5. Area di Videoscrittura
user_text = st.text_area("✍️ Scrivi qui il tuo testo oppure usa la foto sopra:", height=200)

if st.button("✨ Controlla il mio lavoro"):
    with st.spinner("Il maestro sta leggendo..."):
        content = [system_prompt]
        
        # Se c'è una foto, aggiungila all'invio per l'OCR
        if uploaded_file:
            img = Image.open(uploaded_file)
            content.append(img)
        
        # Aggiungi il testo dell'utente
        content.append(user_text)
        
        # Risposta dell'IA
        response = model.generate_content(content)
        st.markdown(response.text)
        
        # Tasto per lettura (JavaScript)
        clean_text = response.text.replace('"', '').replace("'", "")
        st.components.v1.html(f"""
            <button onclick="window.speechSynthesis.speak(new SpeechSynthesisUtterance('{clean_text}'))" 
            style="padding:10px; background:#4CAF50; color:white; border:none; border-radius:5px;">
            🔊 Ascolta la correzione
            </button>
        """, height=50)