import streamlit as st
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re

# Text Cleaning Functions
def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub(r'\[[^]]*\]', '', text)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    text = re.sub(r'\s+', ' ', text).strip()  # Clean up extra whitespace
    return text

# Streamlit App
st.title("XML Text Processor")
st.write("Upload an XML file to parse and clean the text.")

# File Upload
uploaded_file = st.file_uploader("Choose an XML file", type="xml")

if uploaded_file is not None:
    # Parse XML
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        raw_text = ET.tostring(root, encoding='utf8').decode('utf8')
        
        # Display Raw XML Content
        st.subheader("Raw XML Content")
        st.text_area("XML Content", raw_text, height=300)
        
        # Process and Clean Text
        cleaned_text = denoise_text(raw_text)
        
        # Display Cleaned Text
        st.subheader("Cleaned Text")
        st.text_area("Cleaned Text Content", cleaned_text, height=300)
        
    except ET.ParseError:
        st.error("There was an error parsing the XML file. Please check the file format.")
