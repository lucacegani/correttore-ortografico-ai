import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. Configurazione API e Modello
api_key = st.secrets["api_key"].strip()
genai.configure(api_key=api_key)

# Configurazione del Maestro (Presa dalle tue istruzioni di AI Studio)
SYSTEM_PROMPT = """
Sei il "Maestro Digitale", un tutor esperto in didattica per la scuola primaria (bambini di 10-11 anni). Il tuo tono è incoraggiante, chiaro e mai severo.
Obiettivo: Aiutare l'alunno a trasformare i suoi testi in testi corretti, spiegando gli errori in modo pedagogico.

Compiti specifici:
1. Fase OCR (se ricevi un'immagine): Trascrivi fedelmente tutto il testo che vedi, mantenendo anche gli errori originali.
2. Fase Correzione: Riscrivi il testo in modo corretto. Mantieni lo stile del bambino, non usare parole troppo difficili.
3. Fase Spiegazione: Scegli 2 o 3 errori importanti e spiega la regola (es. l'uso dell'H, doppie, ecc.) assegnando un 'Punto Riconoscimento' per ogni regola spiegata correttamente.

Formato della risposta:
📝 Il tuo testo originale
[Testo originale]
✅ La versione corretta
[Testo corretto]
💡 I consigli del Maestro
Regola: [Spiegazione con punti riconoscimento]
Incoraggiamento: [Frase positiva]
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# 2. Interfaccia Grafica (Stile Quaderno)
st.set_page_config(page_title="Maestro Digitale", page_icon="🍎")

st.markdown("""
    <style>
    .stTextArea textarea {
        background-color: #f0f8ff;
        color: #172554; /* Blu scuro per leggibilità */
        font-size: 18px !important;
        border: 2px solid #bfdbfe;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍎 Il Maestro Digitale")

# Selettore Voce (Simulato come nel tuo progetto)
voce_scelta = st.sidebar.selectbox("Scegli la voce del Maestro:", ["Kore (Dolce)", "Puck (Vivace)", "Zephyr", "Fenrir"])

# Area Input
uploaded_file = st.file_uploader("📸 Carica la foto del quaderno", type=['png', 'jpg', 'jpeg'])
user_text = st.text_area("✍️ Scrivi qui il tuo testo (il Maestro leggerà esattamente quello che scrivi):", height=200)

# Bottone Ascolta Testo Originale (Tassativo: Legge esattamente come scritto)
if user_text:
    if st.button("🔊 Ascolta quello che hai scritto"):
        # Pulizia testo per JS
        clean_input = user_text.replace('"', '').replace("'", "").replace("\n", " ")
        st.components.v1.html(f"""
            <script>
            var msg = new SpeechSynthesisUtterance("{clean_input}");
            msg.lang = 'it-IT';
            msg.rate = 0.8; // Più lento per far sentire gli errori
            window.speechSynthesis.speak(msg);
            </script>
        """, height=0)

# Bottone Correzione
if st.button("✨ Chiedi la correzione al Maestro", type="primary"):
    if not user_text and not uploaded_file:
        st.warning("Inserisci del testo o una foto!")
    else:
        with st.spinner("Il Maestro sta analizzando..."):
            content = []
            if uploaded_file:
                img = Image.open(uploaded_file)
                content.append(img)
            if user_text:
                content.append(user_text)
            
            response = model.generate_content(content)
            risposta_piena = response.text
            
            st.markdown("---")
            st.write(risposta_piena)
            
            # Bottone per leggere la CORREZIONE
            clean_output = risposta_piena.replace('"', '').replace("'", "").replace("\n", " ").replace("*", "")
            st.components.v1.html(f"""
                <button onclick="speak()" style="background-color:#4CAF50; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;">
                🔊 Ascolta la correzione del Maestro
                </button>
                <script>
                function speak() {{
                    var msg = new SpeechSynthesisUtterance("{clean_output}");
                    msg.lang = 'it-IT';
                    window.speechSynthesis.speak(msg);
                }}
                </script>
            """, height=60)
