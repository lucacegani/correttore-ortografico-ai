import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configurazione API Key
api_key = st.secrets["api_key"].strip()
genai.configure(api_key=api_key)

# Usiamo il modello che ha funzionato nel test
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Interfaccia della Classe
st.set_page_config(page_title="Maestro Digitale 5^A", page_icon="🍎")
st.title("🍎 Il Maestro Digitale (Classe 5^A)")
st.write("Benvenuti! Caricate la foto del quaderno o scrivete il vostro testo qui sotto.")

# 3. Input alunno
uploaded_file = st.file_uploader("📸 Scatta o carica una foto", type=['png', 'jpg', 'jpeg'])
user_text = st.text_area("✍️ Scrivi qui il tuo compito:", height=150)

if st.button("✨ Chiedi aiuto al Maestro", type="primary"):
    if not user_text and not uploaded_file:
        st.warning("Ehi, non hai scritto nulla!")
    else:
        with st.spinner("Il maestro sta leggendo..."):
            try:
                prompt = "Sei un maestro di scuola primaria italiano gentile e incoraggiante. Se ricevi un'immagine, trascrivila. Correggi gli errori ortografici e grammaticali, spiega le regole in modo semplice e termina sempre con un complimento."
                
                content = [prompt]
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    content.append(img)
                if user_text:
                    content.append(user_text)

                response = model.generate_content(content)
                risposta = response.text
                
                st.success("Ecco i miei consigli:")
                st.write(risposta)

                # --- TASTO LETTURA VOCALE ---
                clean_text = risposta.replace('"', '').replace("'", "").replace("\n", " ").replace("*", "")
                
                html_speech = f"""
                <div style="background-color:#e8f4ea; padding:20px; border-radius:15px; text-align:center; border: 2px solid #4CAF50;">
                    <button id="btnVoce" style="background-color:#4CAF50; color:white; padding:15px 30px; border:none; border-radius:10px; cursor:pointer; font-size:20px; font-weight:bold;">
                        🔊 ASCOLTA IL MAESTRO
                    </button>
                </div>
                <script>
                    document.getElementById('btnVoce').onclick = function() {{
                        var msg = new SpeechSynthesisUtterance("{clean_text}");
                        msg.lang = 'it-IT';
                        msg.rate = 0.9;
                        window.speechSynthesis.speak(msg);
                    }};
                </script>
                """
                st.components.v1.html(html_speech, height=150)

            except Exception as e:
                st.error(f"Errore: {e}")
