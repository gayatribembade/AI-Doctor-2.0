import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import uuid
import tempfile
# Add these new imports at the top
from datetime import datetime
import base64
import wave
import io

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_audio
from voice_of_the_doctor import text_to_speech_with_gtts

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create temp directory for uploads
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

system_prompt = """You have to act as a professional doctor, I know you are not but this is for learning purpose. 
What's in this image? Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Do not say 'In the image I see' but say 'With what I see, I think you have ....'
Don't respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot. 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""

@app.route('/')
def index():
    print("Rendering index.html")
    return render_template('index.html')

@app.route('/record_audio', methods=['POST'])
def record_audio():
    try:
        # Get base64 audio data from request
        audio_data = request.json.get('audio_data')
        if not audio_data:
            return jsonify({'success': False, 'error': 'No audio data received'}), 400
        
        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_data.split(',')[1])
        
        # Save as WAV file
        audio_filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        
        # Convert and save as proper WAV file
        with wave.open(audio_filepath, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 2 bytes (16-bit)
            wf.setframerate(44100)  # 44.1kHz
            wf.writeframes(audio_bytes)
        
        # Transcribe audio
        transcription = transcribe_audio(audio_file_path=audio_filepath)
        
        # Clean up
        if os.path.exists(audio_filepath):
            os.remove(audio_filepath)
        
        return jsonify({
            'success': True,
            'transcription': transcription
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Initialize variables
        audio_filepath = None
        image_filepath = None
        speech_to_text_output = ""
        doctor_response = ""
        audio_response_path = None
        
        # Handle audio file
        if 'audio' in request.files and request.files['audio'].filename != '':
            audio_file = request.files['audio']
            if audio_file:
                # Save audio file with unique name
                audio_filename = str(uuid.uuid4()) + '_' + secure_filename(audio_file.filename)
                audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
                audio_file.save(audio_filepath)
                
                # Transcribe audio
                speech_to_text_output = transcribe_audio(audio_file_path=audio_filepath)
                if not speech_to_text_output:
                    speech_to_text_output = "Sorry, I could not understand the audio."
        
        # Handle image file
        if 'image' in request.files and request.files['image'].filename != '':
            image_file = request.files['image']
            if image_file:
                # Save image file with unique name
                image_filename = str(uuid.uuid4()) + '_' + secure_filename(image_file.filename)
                image_filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image_file.save(image_filepath)
        
        # Analyze image with query
        if image_filepath:
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_to_text_output,
                encoded_image=encode_image(image_filepath),
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
        else:
            doctor_response = "No image provided for me to analyze"
        
        # Generate audio response
        audio_output_filename = str(uuid.uuid4()) + "_response.mp3"
        audio_response_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_output_filename)
        text_to_speech_with_gtts(
            input_text=doctor_response, 
            output_filepath=audio_response_path
        )
        
        # Clean up uploaded files
        if audio_filepath and os.path.exists(audio_filepath):
            os.remove(audio_filepath)
        if image_filepath and os.path.exists(image_filepath):
            os.remove(image_filepath)
        
        return jsonify({
            'success': True,
            'speech_text': speech_to_text_output,
            'doctor_response': doctor_response,
            'audio_response': audio_output_filename
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve generated audio files"""
    try:
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(audio_path, as_attachment=False, mimetype='audio/mpeg')
    except:
        return "Audio file not found", 404

# Clean up old files on startup
def cleanup_temp_files():
    """Clean up old temporary files"""
    try:
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except:
        pass

        

if __name__ == '__main__':
    cleanup_temp_files()
    app.run(debug=True, host='127.0.0.1', port=8000)