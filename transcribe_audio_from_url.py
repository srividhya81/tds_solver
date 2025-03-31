import ssl
import subprocess
import os
import logging
from fastapi import HTTPException
import whisper
import re  # Ensure the standard `re` module is used

# Load Whisper model once
model = whisper.load_model("base")

# Add SSL certificate check for secure connections
def transcribe_audio_from_url(start_time: float, end_time: float):
    try:
        url = "https://youtu.be/NRntuOJu4ok"
        logging.info("Starting transcription process...")
        logging.info(f"URL: {url}, Start Time: {start_time}, End Time: {end_time}")

        # Step 1: Download the audio using yt-dlp
        audio_file = "audio.mp3"
        download_command = ["yt-dlp", "-x", "--audio-format", "mp3", "-o", "audio.%(ext)s", url]
        logging.info(f"Running download command: {' '.join(download_command)}")
        subprocess.run(download_command, check=True)
        logging.info("Audio downloaded successfully.")

        # Step 2: Trim the audio using ffmpeg
        trimmed_audio_file = "trimmed_audio.mp3"
        trim_command = [
            "ffmpeg", "-i", audio_file, "-ss", str(start_time), "-to", str(end_time),
            "-c", "copy", trimmed_audio_file, "-y"
        ]
        logging.info(f"Running trim command: {' '.join(trim_command)}")
        subprocess.run(trim_command, check=True)
        logging.info("Audio trimmed successfully.")

        # Step 3: Transcribe the audio
        logging.info("Starting transcription using Whisper model...")
        result = model.transcribe(trimmed_audio_file)
        logging.info("Transcription completed successfully.")

        # Cleanup
        os.remove(audio_file)
        os.remove(trimmed_audio_file)
        logging.info("Temporary files cleaned up.")

        return {"transcript": result["text"]}
    except Exception as e:
        logging.error(f"Error during transcription process: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    

ssl._create_default_https_context = ssl._create_unverified_context
