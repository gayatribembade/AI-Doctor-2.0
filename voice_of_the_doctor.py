# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

#Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    print("TEXT TO SPEECH CONVERTED USING OLD GTTS")

# #Step1b: Setup Text to Speech–TTS–model with ElevenLabs
# import elevenlabs
# from elevenlabs.client import ElevenLabs

# ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

# def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
#     client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     audio=client.generate(
#         text= input_text,
#         voice= "Aria",
#         output_format= "mp3_22050_32",
#         model= "eleven_turbo_v2"
#     )
#     elevenlabs.save(audio, output_filepath)
#     print("TEXT TO SPEECH CONVERTED USING ELEVEN LABS OLD")



#Step2: Use Model for Text output to Voice

import subprocess
import platform
from pydub import AudioSegment
import os
ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg", "bin", "ffmpeg.exe")
AudioSegment.converter = ffmpeg_path
from pydub.playback import play



def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    print("TEXT TO SPEECH CONVERTED USING GTTS NEW")
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['start', '', output_filepath], shell=True)
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")



# def text_to_speech_with_elevenlabs(input_text, output_filepath):
#     client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     audio=client.generate(
#         text= input_text,
#         voice= "Aria",
#         output_format= "mp3_22050_32",
#         model= "eleven_turbo_v2"
#     )
#     elevenlabs.save(audio, output_filepath)
#     print("TEXT TO SPEECH CONVERTED USING ELEVEN LABS NEW")
#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":  # macOS
#             subprocess.run(['afplay', output_filepath])
#         elif os_name == "Windows":  # Windows
#             subprocess.run(['start', '', output_filepath], shell=True)
#         elif os_name == "Linux":  # Linux
#             subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
#         else:
#             raise OSError("Unsupported operating system")
#     except Exception as e:
#         print(f"An error occurred while trying to play the audio: {e}")

#############################################################################################

# input_text="Welcome to Magic Doctor Application"
#text_to_speech_with_gtts_old(input_text=input_text, output_filepath="1_gtts_testing.mp3")
#text_to_speech_with_elevenlabs_old(input_text, output_filepath="2_elevenlabs_testing.mp3") 
#text_to_speech_with_gtts(input_text=input_text, output_filepath="3_gtts_testing_autoplay.mp3")
# text_to_speech_with_elevenlabs(input_text, output_filepath="4_elevenlabs_testing_autoplay.mp3")