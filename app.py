import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from PyPDF2 import PdfReader
import os

# Initialize LLM with Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key="AIzaSyDlGuiJOqQePVsQEu5gWiftb74RDGvcq-c")

# App Title
st.set_page_config(page_title="Multilingual Translator", layout="wide")
st.title("🌐 Multilingual Translator")
st.write("Translate your text or PDF content into multiple languages with ease!")

# Sidebar
st.sidebar.header("📄 PDF Translator")
uploaded_file = st.sidebar.file_uploader("Upload your PDF here:", type="pdf")

# Language Selection
language = st.sidebar.selectbox(
    "🌍 Select a language for translation:",
    [
         "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", "Basque", "Belarusian", 
    "Bengali", "Bosnian", "Bulgarian", "Catalan", "Cebuano", "Chinese", "Corsican", "Croatian", 
    "Czech", "Danish", "Dutch", "English", "Esperanto", "Estonian", "Filipino", "Finnish", "French", 
    "Frisian", "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian Creole", "Hausa", 
    "Hawaiian", "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", 
    "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Kinyarwanda", "Korean", 
    "Kurdish", "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", 
    "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian", "Myanmar (Burmese)", 
    "Nepali", "Norwegian", "Nyanja (Chichewa)", "Odia (Oriya)", "Pashto", "Persian", "Polish", 
    "Portuguese", "Punjabi", "Romanian", "Russian", "Samoan", "Scots Gaelic", "Serbian", "Sesotho", 
    "Shona", "Sindhi", "Sinhala (Sinhalese)", "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", 
    "Swahili", "Swedish", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Turkish", "Turkmen", "Ukrainian", 
    "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"
    ]
)

# PDF Translation
if uploaded_file:
    pdf_reader = PdfReader(uploaded_file)
    pdf_text = "".join([page.extract_text() for page in pdf_reader.pages])

    st.sidebar.subheader("📝 Extracted PDF Content")
    st.sidebar.text_area("Preview PDF Content:", pdf_text[:500], height=150)

    if st.sidebar.button("Translate PDF"):
        if pdf_text.strip():
            prompt = f"""
            Act as a professional translator. Translate the following PDF content into **{language}**.
            Preserve the tone and structure of the original text.

            **PDF Content:**  
            {pdf_text}
            """
            response = llm.invoke(prompt)
            translated_text = response.content

            st.subheader("📖 Translated PDF Content")
            st.text_area("Translation:", translated_text, height=250)

            translated_file_path = "translated_file.txt"
            with open(translated_file_path, "w", encoding="utf-8") as f:
                f.write(translated_text)
            with open(translated_file_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Translated PDF",
                    data=f,
                    file_name="translated_file.txt",
                    mime="text/plain",
                )
            os.remove(translated_file_path)
        else:
            st.sidebar.error("No content found in the uploaded PDF.")

# Text Translation
st.subheader("✍️ Text Translator")
st.write("Enter text below to translate:")
user_text = st.text_area("Enter your text:", placeholder="Type your text here...")

if st.button("Translate Text"):
    if user_text.strip():
        prompt = f"""
        Act as a professional translator. Translate the following text into **{language}**.
        Preserve the tone and structure of the original text.

        **Text Content:**  
        {user_text}
        """
        response = llm.invoke(prompt)
        translated_text = response.content

        st.subheader("📝 Translated Text")
        st.text_area("Translation:", translated_text, height=250)

        translated_file_path = "translated_text.txt"
        with open(translated_file_path, "w", encoding="utf-8") as f:
            f.write(translated_text)
        with open(translated_file_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Translated Text",
                data=f,
                file_name="translated_text.txt",
                mime="text/plain",
            )
        os.remove(translated_file_path)
    else:
        st.error("Please enter some text for translation.")
