# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

#Step1: Setup Audio recorder (ffmpeg & portaudio)
# ffmpeg, portaudio, pyaudio
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Record audio from microphone and save as MP3 file.
    
    Args:
        file_path (str): Path to save the recorded audio file.
        timeout (int): Maximum time to wait for a phrase to start (in seconds).
        phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
        
    Returns:
        bool: True if recording successful, False otherwise.
    """
    recognizer = sr.Recognizer()
    
    try:
        # Check if microphone is available
        mic_list = sr.Microphone.list_microphone_names()
        if not mic_list:
            logging.error("No microphone found")
            return False
            
        logging.info(f"Available microphones: {mic_list}")
        
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, 
                                        timeout=timeout, 
                                        phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert to WAV format first
            wav_data = audio_data.get_wav_data()
            logging.info("Converting to WAV format...")
            
            # Create WAV file temporarily
            wav_path = file_path.replace('.mp3', '.wav')
            with open(wav_path, 'wb') as wav_file:
                wav_file.write(wav_data)
            
            # Convert WAV to MP3
            audio_segment = AudioSegment.from_wav(wav_path)
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            # Clean up temporary WAV file
            os.remove(wav_path)
            
            logging.info(f"Audio saved to {file_path}")
            return True
            
    except sr.WaitTimeoutError:
        logging.error("No speech detected within timeout period")
        return False
    except sr.UnknownValueError:
        logging.error("Could not understand audio")
        return False
    except sr.RequestError as e:
        logging.error(f"Could not request results from Speech Recognition service; {e}")
        return False
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False


def transcribe_audio(audio_file_path):
    """
    Transcribe audio file to text using Groq's API.
    
    Args:
        audio_file_path (str): Path to the audio file.
        
    Returns:
        str: Transcribed text or None if failed.
    """
    try:
        # Initialize Groq client
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        # Verify audio file exists
        if not os.path.exists(audio_file_path):
            logging.error(f"Audio file not found: {audio_file_path}")
            return None
            
        # Get file size for logging
        file_size = os.path.getsize(audio_file_path)
        logging.info(f"Transcribing audio file: {audio_file_path} (size: {file_size/1024:.1f} KB)")
        
        # Transcribe the audio
        with open(audio_file_path, "rb") as audio_file:
            logging.info("Starting transcription...")
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
                language="en",
                response_format="text"
            )
            
            logging.info("Transcription complete")
            return transcription.text
            
    except Exception as e:
        logging.error(f"Error transcribing audio: {e}")
        return None


#############################################################################
# Example usage:
if __name__ == "__main__":
    audio_filepath = "patient_voice_test_for_patient.mp3"
    
    # Record audio
    if record_audio(audio_filepath):
        # Transcribe audio
        transcription = transcribe_audio(audio_filepath)
        if transcription:
            print("\nTranscription:", transcription)
        else:
            print("Failed to transcribe audio")
    else:
        print("Failed to record audio")