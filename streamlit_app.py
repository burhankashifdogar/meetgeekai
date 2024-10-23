
import streamlit as st
import moviepy.editor as mp
import whisper
import torch
import requests
import ssl
import os
from requests.adapters import HTTPAdapter
import warnings
import requests
import urllib3

# Disable SSL warnings
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()


# Automatically set up SSL context for secure HTTPS connections
ssl_context = ssl.create_default_context()
ssl_context.load_default_certs()

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = ssl_context
        super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

# Apply SSL context to all HTTPS connections using requests
session = requests.Session()
session.mount("https://", SSLAdapter())

# Function to ensure SSL during Whisper model loading
def load_model_with_ssl(model_size):
    try:
        st.info(f"Loading Whisper model: {model_size}")
        # Disable SSL verification in requests temporarily
        model = whisper.load_model(model_size)
        return model
    except Exception as e:
        st.error(f"Error loading Whisper model '{model_size}': {str(e)}")
        return None

# Helper function to extract audio
def extract_audio(video_path):
    audio_path = "meeting_audio.wav"
    try:
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
    except Exception as e:
        st.error(f"Error processing video file: {str(e)}")
        return None

    return audio_path

# Helper function to transcribe video
def transcribe_video(video_path, model_size="base", language=None):
    st.subheader("Step 1: Extracting Audio")

    audio_path = extract_audio(video_path)
    if not audio_path:
        return None

    device = torch.device("cpu")
    st.info("Using CPU for inference due to limited MPS support on M1/M2.")

    st.subheader("Step 2: Transcribing Audio")

    model = load_model_with_ssl(model_size)
    if not model:
        return None

    # Add spinner while the transcription is taking place
    with st.spinner("Transcribing audio... This may take a while depending on the length of the video."):
        try:
            result = model.transcribe(audio_path, language=language)
        except Exception as e:
            st.error(f"Error during transcription: {str(e)}")
            return None
        finally:
            os.remove(audio_path)

    return result["text"]

# Streamlit app layout
st.title("Video to Text Transcription App")
st.write("Upload a video file to extract and transcribe its audio.")

uploaded_file = st.file_uploader("Choose a video file (max 1 GB)", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file:
    max_size_mb = 500
    uploaded_file.seek(0, os.SEEK_END)
    file_size_mb = uploaded_file.tell() / (1024 * 1024)
    uploaded_file.seek(0)

    if file_size_mb > max_size_mb:
        st.error(f"File size exceeds the 500 MB limit. Your file size is {file_size_mb:.2f} MB.")
    else:
        video_path = "temp_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        model_size = st.selectbox(
            "Select Whisper model size:",
            ["tiny", "base", "small"],
            index=1,
            help="Larger models offer higher accuracy but may take longer to process."
        )

        language = st.text_input(
            "Language code (optional)",
            help="Provide a language code (e.g., 'en' for English, 'es' for Spanish) or leave empty to auto-detect."
        )

        if st.button("Start Transcription"):
            transcription = transcribe_video(video_path, model_size=model_size, language=language or None)

            if transcription:
                st.subheader("Step 3: Displaying Transcription")
                st.write(transcription)
                st.download_button("Download Transcription", transcription, file_name="transcription.txt")

            os.remove(video_path)