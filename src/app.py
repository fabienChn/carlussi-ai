import io
import base64
import json
import ssl
import audioop
import numpy as np
from flask import Flask, request
from flask_sock import Sock, ConnectionClosed
from twilio.twiml.voice_response import VoiceResponse, Start
from twilio.rest import Client
from librosa.core import resample
from whisperer import whisperer  # Import the whisperer function

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ignore SSL certificate verification (not recommended for production use)
ssl._create_default_https_context = ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
sock = Sock(app)
twilio_client = Client()

CL = '\\x1b[0K'
BS = '\\x08'

# Buffer to store audio data
audio_buffer = bytes()

@app.route('/call', methods=['POST'])
def call():
    """Accept a phone call."""
    response = VoiceResponse()
    start = Start()
    start.stream(url=f'wss://{request.host}/stream')
    response.append(start)
    response.say('Please leave a message')
    response.pause(length=60)
    print(f'Incoming call from {request.form["From"]}')
    return str(response), 200, {'Content-Type': 'text/xml'}


@sock.route('/stream')
def stream(ws):
    """Receive and transcribe audio stream."""
    global audio_buffer  # Use the global audio buffer
    while True:
        try:
            message = ws.receive()
            data = json.loads(message)
        except ConnectionClosed:
            break
        if data.get('event') == 'media':
            audio = base64.b64decode(data['media']['payload'])
            audio = audioop.ulaw2lin(audio, 2)

            # Add the audio data to the buffer
            audio_buffer += audio

            # If the buffer has at least 30 seconds of audio (16kHz sample rate), process it
            if len(audio_buffer) >= 30 * 16000 * 2:  # 2 bytes per sample
                # Interpret the PCM audio data as a numpy array
                audio_data = np.frombuffer(audio_buffer, dtype=np.int16)

                # Upsample the audio from 8kHz to 16kHz
                audio_data_resampled = resample(audio_data.astype(float), orig_sr=8000, target_sr=16000)

                # Print the length of the audio data
                print(f"Audio data length: {len(audio_data_resampled)}")

                # Transcribe the audio data using the Whisper ASR
                try:
                    transcription = whisperer(audio_data_resampled, 16000)
                    print(f"Transcription: {transcription}")  # Print the transcription
                except Exception as e:
                    print(f"Error during transcription: {e}")
                    continue

                # Send the transcription back to the client
                ws.send(json.dumps({'transcription': transcription}))

                # Clear only the oldest second of the buffer
                audio_buffer = audio_buffer[16000 * 2:]  # 2 bytes per sample

                # Print the length of the audio buffer
                print(f"Buffer length after clearing: {len(audio_buffer)}")




if __name__ == '__main__':
    from pyngrok import ngrok
    port = 5000
    public_url = ngrok.connect(port, bind_tls=True).public_url
    number = twilio_client.incoming_phone_numbers.list()[0]
    number.update(voice_url=public_url + '/call')
    print(f'Waiting for calls on {number.phone_number}')

    app.run(port=port)

