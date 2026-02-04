import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configurazione API Key dai Secrets
try:
    api_key = st.secrets["api_key"]
    genai.configure(api_key=api_key)
    # Usiamo il modello corretto
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Errore nella configurazione della chiave API. Controlla i Secrets!")

# 2. Interfaccia Semplice per la scuola
st.set_page_config(page_title="Maestro Digitale 5^A", page_icon="📝")
st.title("📝 Il mio Assistente alla Scrittura")
st.write("Carica una foto del quaderno o scrivi direttamente qui sotto.")

# 3. Input: Foto e Testo
uploaded_file = st.file_uploader("📸 Carica la foto del quaderno", type=['png', 'jpg', 'jpeg'])
user_text = st.text_area("✍️ Oppure scrivi qui:", height=150)

# 4. Bottone di azione
if st.button("✨ Controlla il mio lavoro", type="primary"):
    if not user_text and not uploaded_file:
        st.warning("Per favore, scrivi qualcosa o carica una foto!")
    else:
        with st.spinner("Il maestro sta leggendo..."):
            try:
                # Prepariamo il contenuto per l'IA
                prompt = "Sei un maestro di primaria. Se c'è una foto, trascrivila. Poi correggi il testo e dai consigli gentili."
                content_to_send = [prompt]
                
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    content_to_send.append(img)
                
                if user_text:
                    content_to_send.append(user_text)

                # Chiamata a Gemini
                response = model.generate_content(content_to_send)
                risposta_maestro = response.text
                
                # Mostriamo il risultato
                st.success("Ecco la correzione del Maestro:")
                st.markdown(risposta_maestro)

                # --- TASTO LETTURA VOCALE ---
                # Puliamo il testo per il lettore vocale (rimuoviamo simboli markdown)
                testo_pulito = risposta_maestro.replace('#', '').replace('*', '').replace('"', "'")
                
                html_code = f"""
                <div style="margin-top: 20px;">
                    <button onclick="speak()" style="background-color: #4CAF50; color: white; padding: 15px 32px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px;">
                        🔊 Ascolta la correzione
                    </button>
                </div>
                <script>
                    function speak() {{
                        var msg = new SpeechSynthesisUtterance();
                        msg.text = "{testo_pulito}";
                        msg.lang = 'it-IT';
                        window.speechSynthesis.speak(msg);
                    }}
                </script>
                """
                st.components.v1.html(html_code, height=100)

            except Exception as e:
                st.error(f"Ops! Qualcosa è andato storto: {e}")
