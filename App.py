import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configurazione API Key
api_key = st.secrets["api_key"].strip()
genai.configure(api_key=api_key)

# Proviamo il modello più stabile in assoluto
model = genai.GenerativeModel('gemini-1.0-pro')

# 2. Interfaccia
st.set_page_config(page_title="Maestro Digitale 5^A", page_icon="📝")
st.title("📝 Il mio Assistente alla Scrittura")
st.write("Ciao! Scrivi qui sotto o carica la foto del tuo quaderno.")

uploaded_file = st.file_uploader("📸 Carica la foto", type=['png', 'jpg', 'jpeg'])
user_text = st.text_area("✍️ Scrivi qui:", height=150)

if st.button("✨ Controlla il mio lavoro", type="primary"):
    if not user_text and not uploaded_file:
        st.warning("Scrivi qualcosa prima!")
    else:
        with st.spinner("Il maestro sta leggendo..."):
            try:
                prompt = "Sei un maestro di scuola primaria. Se c'è un'immagine, trascrivila fedelmente. Poi correggi eventuali errori del testo e dai consigli gentili all'alunno."
                
                content_to_send = [prompt]
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    content_to_send.append(img)
                if user_text:
                    content_to_send.append(user_text)

                # Generazione risposta
                response = model.generate_content(content_to_send)
                testo_risposta = response.text
                
                st.success("Ecco la correzione:")
                st.write(testo_risposta)

                # --- SISTEMA DI LETTURA VOCALE ---
                # Pulizia profonda del testo per evitare errori JavaScript
                clean_text = testo_risposta.replace('"', '').replace("'", "").replace("\n", " ").replace("\r", " ")
                
                html_speech = f"""
                <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center; margin-top:20px;">
                    <p style="color:#31333F; font-family:sans-serif; font-weight:bold;">Vuoi ascoltare la correzione?</p>
                    <button id="speakBtn" style="background-color:#4CAF50; color:white; padding:15px 30px; border:none; border-radius:5px; cursor:pointer; font-size:18px; font-weight:bold;">
                        ▶️ CLICCA QUI PER ASCOLTARE
                    </button>
                </div>
                <script>
                    document.getElementById('speakBtn').onclick = function() {{
                        var msg = new SpeechSynthesisUtterance("{clean_text}");
                        msg.lang = 'it-IT';
                        msg.rate = 0.9;
                        window.speechSynthesis.speak(msg);
                    }};
                </script>
                """
                st.components.v1.html(html_speech, height=150)

            except Exception as e:
                st.error(f"Errore di connessione: {{e}}")
                st.info("Nota: Se vedi l'errore 404, assicurati di aver abilitato le API di Gemini nel tuo Google Cloud Console.")
