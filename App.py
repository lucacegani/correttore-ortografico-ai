import streamlit as st
import google.generativeai as genai

# Configurazione rapida
try:
    api_key = st.secrets["api_key"].strip()
    genai.configure(api_key=api_key)
    
    # Proviamo a elencare i modelli per vedere quale puoi usare
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Scegliamo il primo disponibile (di solito gemini-pro o gemini-1.5-flash)
    model_name = available_models[0] if available_models else 'gemini-pro'
    model = genai.GenerativeModel(model_name)
    
    st.success(f"✅ Connesso con successo! Modello in uso: {model_name}")
except Exception as e:
    st.error(f"❌ Errore critico: {e}")
    st.info("Se vedi ancora 404, prova a creare una chiave con un account Gmail differente.")

# Interfaccia minima per test
user_input = st.text_input("Fai una domanda veloce al maestro:")
if st.button("Invia"):
    response = model.generate_content(user_input)
    st.write(response.text)
