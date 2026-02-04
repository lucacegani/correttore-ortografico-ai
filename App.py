import streamlit as st
import google.generativeai as genai

# Proviamo a vedere cosa legge l'app (senza mostrare la chiave intera per sicurezza)
if "api_key" in st.secrets:
    k = st.secrets["api_key"]
    st.write(f"✅ Chiave trovata! Inizia con: {k[:5]}... ed è lunga {len(k)} caratteri.")
else:
    st.error("❌ La chiave non è stata trovata nei Secrets di Streamlit!")

if st.button("Fai un test veloce"):
    try:
        genai.configure(api_key=st.secrets["api_key"].strip())
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Dì 'Ciao, sono pronto!'")
        st.success(response.text)
    except Exception as e:
        st.error(f"Errore: {e}")
