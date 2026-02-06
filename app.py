import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="PromptGen dla Nano Banana Pro",
    page_icon="🍌",
    layout="centered"
)

# --- CSS (SZATA GRAFICZNA) ---
st.markdown("""
    <style>
    /* Główne tło i kolory */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    
    /* Nagłówek */
    h1 {
        color: #FFE135 !important;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* Przycisk wgrywania pliku */
    .stFileUploader {
        border: 2px dashed #FFE135;
        border-radius: 10px;
        padding: 20px;
        background-color: #1E1E1E;
    }
    
    /* Główny przycisk akcji */
    div.stButton > button {
        background-color: #FFE135;
        color: #000000;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #FFF090;
        box-shadow: 0 0 15px #FFE135;
        color: #000000;
    }
    
    /* Obszar tekstowy wyniku */
    .stTextArea textarea {
        background-color: #1E1E1E;
        color: #FFE135;
        border: 1px solid #444;
        font-family: 'Courier New', monospace;
    }
    
    /* Stopka */
    .footer {
        text-align: center;
        font-size: 0.8em;
        color: #666;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIKA APLIKACJI ---

def generate_prompt(image, api_key):
    """Wysyła zdjęcie do Gemini Vision w celu uzyskania opisu."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Instrukcja dla modelu wizyjnego, aby stworzył idealny prompt
        prompt_instruction = """
        Analyze this image meticulously. You are an expert prompt engineer for a high-end AI image generator called 'Nano Banana Pro'.
        
        Create a detailed text-to-image prompt based on this image. Structure it as follows:
        1. **Subject**: Detailed description of the main subject.
        2. **Environment**: Background, setting, atmosphere.
        3. **Lighting & Color**: Type of light (soft, cinematic, neon), color palette.
        4. **Style & Medium**: e.g., Photorealistic, 35mm film, Cyberpunk, Oil painting, Digital Art.
        5. **Technical keywords**: e.g., 8k, highly detailed, sharp focus, masterpiece.

        Output ONLY the raw prompt text, ready to be copied. No markdown formatting like 'Here is the prompt:'.
        """
        
        with st.spinner('🍌 Obieranie pikseli... (Analiza obrazu)'):
            response = model.generate_content([prompt_instruction, image])
            return response.text
    except Exception as e:
        return f"Błąd: {str(e)}"

# --- INTERFEJS UŻYTKOWNIKA ---

st.title("NANOBANANA • PROMPTER")
st.markdown("<p style='text-align: center; color: #888;'>Wgraj zdjęcie, a AI napisze dla Ciebie idealny prompt.</p>", unsafe_allow_html=True)

# Sidebar na klucz API (dla bezpieczeństwa)
with st.sidebar:
    st.header("Ustawienia")
    api_key = st.text_input("Twój klucz Google Gemini API", type="password")
    st.info("Klucz zdobędziesz za darmo na: aistudio.google.com")
    st.markdown("---")
    st.write("Engine: **Gemini 1.5 Flash Vision**")

# Sekcja główna
uploaded_file = st.file_uploader("Wybierz zdjęcie (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Wyświetlanie podglądu
    col1, col2 = st.columns([1, 2])
    
    image = Image.open(uploaded_file)
    
    with col1:
        st.image(image, caption='Twój obraz', use_container_width=True)
    
    with col2:
        st.write("### Gotowy generować?")
        if not api_key:
            st.warning("⚠️ Proszę podać klucz API w panelu bocznym.")
        else:
            if st.button("GENERUJ PROMPT 🍌"):
                result_prompt = generate_prompt(image, api_key)
                
                st.success("Gotowe!")
                st.text_area("Twój Prompt dla Nano Banana Pro:", value=result_prompt, height=250)
                st.caption("Skopiuj powyższy tekst i wklej do generatora.")

# Stopka
st.markdown("<div class='footer'>Powered by Gemini Vision • Designed koscikiewicz.com</div>", unsafe_allow_html=True)
