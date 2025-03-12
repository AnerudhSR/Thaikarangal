import streamlit as st
import pytesseract
import cv2
import numpy as np
import os
import tempfile
from gtts import gTTS
from pdf2image import convert_from_path
from PIL import Image
from docx import Document
import pydub

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Change this path as needed

# Function to extract text from an image
def extract_text_from_image(image):
    return pytesseract.image_to_string(image, lang='tam')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += extract_text_from_image(img) + "\n"
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to convert text to Tamil speech with default speed 1.25x
def text_to_speech(text, output_path):
    tts = gTTS(text, lang='ta')
    tts.save(output_path)
    audio = pydub.AudioSegment.from_file(output_path)
    audio = audio.speedup(playback_speed=1.25)
    audio.export(output_path, format="mp3")
    return output_path

# Streamlit UI
st.title("Tamil Document to Audiobook Converter")

option = st.selectbox("Choose Input Type", ["Image", "PDF", "DOCX", "Text", "Live Camera"])

if option == "Image":
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        text = extract_text_from_image(image)
        st.text_area("Extracted Text", text, height=200)
        audio_path = text_to_speech(text, "output.mp3")
        st.audio(audio_path, format='audio/mp3')

elif option == "PDF":
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name
        text = extract_text_from_pdf(temp_path)
        st.text_area("Extracted Text", text, height=200)
        audio_path = text_to_speech(text, "output.mp3")
        st.audio(audio_path, format='audio/mp3')

elif option == "DOCX":
    uploaded_file = st.file_uploader("Upload a DOCX", type=["docx"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name
        text = extract_text_from_docx(temp_path)
        st.text_area("Extracted Text", text, height=200)
        audio_path = text_to_speech(text, "output.mp3")
        st.audio(audio_path, format='audio/mp3')

elif option == "Text":
    text = st.text_area("Enter Tamil Text")
    audio_path = text_to_speech(text, "output.mp3")
    st.audio(audio_path, format='audio/mp3')

elif option == "Live Camera":
    st.write("Capture image from camera and extract Tamil text")
    cap = cv2.VideoCapture(0)
    if st.button("Capture Image"):
        ret, frame = cap.read()
        if ret:
            cap.release()
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            st.image(img, caption="Captured Image", use_column_width=True)
            text = extract_text_from_image(img)
            st.text_area("Extracted Text", text, height=200)
            audio_path = text_to_speech(text, "output.mp3")
            st.audio(audio_path, format='audio/mp3')
