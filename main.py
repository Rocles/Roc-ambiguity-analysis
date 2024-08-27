import streamlit as st
import openai
import random
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

@st.cache_data
def analyze_sentence_structure(sentence):
    openai.api_key = OPENAI_API_KEY  # Utiliser la clé API depuis les variables d'environnement
    
    prompt = f"Analyze the sentence structure of the following sentence: '{sentence}'. Does it have a subject, predicate, and object? If not, identify which elements are missing and explain why the sentence might be ambiguous."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Utiliser le modèle mis à jour
        messages=[
            {"role": "system", "content": "You are an expert in sentence structure analysis."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message['content'].strip()

def main():
    st.title("Ambiguity Finder")
    st.sidebar.title("QUANTIFYING AMBIGUITY")
    
    input_method = st.sidebar.radio("Select Input Method:", ["Upload a text file", "Enter text manually"])

    text = ""
    if input_method == "Upload a text file":
        uploaded_file = st.sidebar.file_uploader("Upload a text file", type=["txt"])
        if uploaded_file is not None:
            text = uploaded_file.read().decode("utf-8")
            st.write("### Your uploaded text:")
            st.code(text, language="plaintext")
    
    elif input_method == "Enter text manually":
        text = st.text_area("Enter your text here:")
        if text:
            st.write("### Your entered text:")
            st.code(text, language="plaintext")

    if text:
        analyze_button = st.button("Analyze Ambiguities")
        if analyze_button:
            sentences = text.splitlines()
            ambiguous_sentences = []
            non_ambiguous_sentences = []
            causes_of_ambiguity = []

            for sentence in sentences:
                analysis = analyze_sentence_structure(sentence)
                if "missing" in analysis.lower() or "ambiguous" in analysis.lower():
                    ambiguous_sentences.append(sentence)
                    causes_of_ambiguity.append(analysis)
                else:
                    non_ambiguous_sentences.append(sentence)

            st.write("### Ambiguous Sentences:")
            for i, sentence in enumerate(ambiguous_sentences):
                color = random_color()
                st.markdown(f'<p style="color: {color}">{sentence}</p>', unsafe_allow_html=True)
                st.write(f"**Cause of Ambiguity:** {causes_of_ambiguity[i]}")
            
            st.write("### Non-Ambiguous Sentences:")
            for sentence in non_ambiguous_sentences:
                color = random_color()
                st.markdown(f'<p style="color: {color}">{sentence}</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
