import streamlit as st
import moviepy.editor as mp
import whisper
import requests
import ssl
import os
from requests.adapters import HTTPAdapter
import warnings
import requests
import time
import urllib3
from pydub import AudioSegment  # To split audio into chunks

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

# Split audio into chunks
def split_audio(audio_path, chunk_duration=30):
    audio = AudioSegment.from_wav(audio_path)
    audio_chunks = []
    
    # Split audio into chunks of `chunk_duration` seconds
    for i in range(0, len(audio), chunk_duration * 1000):
        audio_chunks.append(audio[i:i + chunk_duration * 1000])

    return audio_chunks

# Helper function to transcribe video in chunks
def transcribe_video(video_path, model_size="base", language=None, chunk_duration=30):
    st.subheader("Step 1: Extracting Audio")

    progress_audio = st.progress(0)
    time.sleep(0.5)
    progress_audio.progress(20)
    time.sleep(0.5)
    progress_audio.progress(40)
    time.sleep(0.5)
    progress_audio.progress(80)
    audio_path = extract_audio(video_path)
    progress_audio.progress(100)  # Complete audio extraction

    if not audio_path:
        return None


    st.subheader("Step 2: Loading Whisper Model")
    
    # Show and update the progress bar for model loading
    progress_model = st.progress(0)
    time.sleep(0.5)
    progress_model.progress(20)
    time.sleep(0.5)
    progress_model.progress(40)
    time.sleep(0.5)
    progress_model.progress(80)
    model = load_model_with_ssl(model_size)
    progress_model.progress(100)  # Complete model loading  # Complete model loading

    if not model:
        return None

    st.subheader("Step 3: Transcribing Audio")

    # Split audio into chunks and show progress for transcription
    audio_chunks = split_audio(audio_path, chunk_duration)
    total_chunks = len(audio_chunks)
    
    progress_transcription = st.progress(0)
    transcription_result = ""

    # Placeholder for updating only the chunk progress number
    chunk_progress_placeholder = st.empty()

    # Transcribe each chunk and update progress
    for idx, chunk in enumerate(audio_chunks):
        # Export chunk to temporary file
        chunk_path = f"chunk_{idx}.wav"
        chunk.export(chunk_path, format="wav")

        # Update the spinner with current chunk number
        chunk_progress_placeholder.text(f"Transcribing chunk {idx + 1}/{total_chunks}...")

        # Transcribe the chunk
        try:
            result = model.transcribe(chunk_path, language=language)
            transcription_result += result["text"] + " "

            # Clean up chunk file
            os.remove(chunk_path)
        except Exception as e:
            st.error(f"Error during transcription: {str(e)}")
            return None

        # Update progress bar based on the chunk completion
        progress_transcription.progress((idx + 1) / total_chunks)

    # Remove the original audio file
    os.remove(audio_path)

    return transcription_result

# Streamlit app layout
st.title("🎥 Video to Text Transcription App")
st.write("Upload a video file to extract and transcribe its audio.")

uploaded_file = st.file_uploader("🎬 Choose a video file (max 1 GB)", type=["mp4", "mov", "avi", "mkv"])

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
            "🌍 Language code (optional)",
            help="Provide a language code (e.g., 'en' for English, 'es' for Spanish) or leave empty to auto-detect."
        )

        # Adding a heading with an emoji and description for the slider
        st.subheader("🎛️ Adjust Chunk Duration")

        # Create a visually appealing slider with custom emojis
        chunk_duration = st.slider(
            "⏳ Chunk duration (in seconds)", min_value=10, max_value=60, value=30,
            help="Set the duration of each audio chunk to transcribe. Longer chunks might take more time to process, but fewer chunks to transcribe."
        )

        if st.button("⚙️ Start Transcription"):
            transcription = transcribe_video(video_path, model_size=model_size, language=language or None, chunk_duration=chunk_duration)

            if transcription:
                st.subheader("📜 Transcription Result")
                st.write(transcription)
                st.download_button("💾 Download Transcription", transcription, file_name="transcription.txt")

            os.remove(video_path)
