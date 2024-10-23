# 🎥 Video to Text Transcription App

This is a **Streamlit** app that extracts audio from a video file and transcribes it into text using **OpenAI's Whisper model**. You can upload video files, choose different Whisper model sizes, and adjust the chunk duration for transcription. The app supports multiple languages, and you can specify a language code for transcription or let the app detect it automatically.

[![Open in Streamlit Cloud](https://img.shields.io/badge/Open%20in-Streamlit%20Cloud-F24747?logo=streamlit)](https://meetgeekai.streamlit.app) 
![License](https://img.shields.io/github/license/Franky1/Streamlit-ffmpeg-Test?logo=github) 
![Language](https://img.shields.io/github/languages/top/Franky1/Streamlit-ffmpeg-Test?logo=python) 
![Python Version](https://img.shields.io/badge/Python-3.7%20|%203.8%20|%203.9-blue?logo=python) 

## 🌟 Features

- **Video Upload**: Upload `.mp4`, `.mov`, `.avi`, or `.mkv` video files (up to 1GB).
- **Whisper Model Selection**: Choose from different Whisper model sizes (`tiny`, `base`, `small`) for transcription accuracy and speed trade-offs.
- **Language Detection**: Provide an optional language code or let the app detect the language automatically.
- **Adjustable Chunk Duration**: Customize the duration of audio chunks for processing, allowing for more control over transcription speed and accuracy.
- **Transcription Result**: Download the transcription as a `.txt` file.

## 🔧 Installation

To run the app locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Franky1/Streamlit-ffmpeg-Test
   cd Streamlit-ffmpeg-Test
   ```
   ```bash
   git clone https://github.com/burhankashifdogar/meetgeekai
   cd meetgeekai

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install the Required Packages**:
    ```bash
    pip install -r requirements.txt
4. **Run the Streamlit App**:
    ```bash
    streamlit run app.py

## 📚 How to Use the App


- Open the app in your browser by going to http://localhost:8501.
- Upload a Video File: Drag and drop a video file (up to 1GB) into the upload box.
- Select Whisper Model: Choose the Whisper model size based on your preference. Larger models provide more accuracy but take longer to transcribe.
- Language Code: Optionally, provide a language code (e.g., 'en' for English or 'es' for Spanish) or leave it blank for auto-detection.
- Chunk Duration: Use the slider to adjust the duration of each audio chunk to be transcribed.
- Start Transcription: Click the "Start Transcription" button to begin the process. You will see progress updates as each chunk is transcribed.
- Download the Result: After transcription, download the resulting text file.

## 🧠 Model Information

The transcription is powered by OpenAI's Whisper model, a powerful speech recognition model capable of transcribing in multiple languages with high accuracy.

For more information about the Whisper model, visit [Whisper on GitHub](https://github.com/openai/whisper).