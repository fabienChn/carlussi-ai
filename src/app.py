import io
import soundfile
import base64
import json
import ssl
from flask import Flask, request
from flask_sock import Sock, ConnectionClosed
from twilio.twiml.voice_response import VoiceResponse, Start
from twilio.rest import Client

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ignore SSL certificate verification (not recommended for production use)
ssl._create_default_https_context = ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
sock = Sock(app)
twilio_client = Client()

CL = '\x1b[0K'
BS = '\x08'


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
    while True:
        try:
            message = ws.receive()
            data = json.loads(message)
        except ConnectionClosed:
            break
        if data.get('event') == 'media':
            audio = base64.b64decode(data['media']['payload'])
            with io.BytesIO(audio) as audio_stream:
                audio_data, sample_rate = soundfile.read(audio_stream, dtype='int16')

            # audio = audioop.ulaw2lin(audio, 2)
            # audio = audioop.ratecv(audio, 2, 1, 8000, 16000, None)[0]
            print(audio, audio_data, sample_rate)
            
        elif data.get('event') in ['connected', 'start', 'stop']:
            print(f"Received event: {data['event']}")


if __name__ == '__main__':
    from pyngrok import ngrok
    port = 5000
    public_url = ngrok.connect(port, bind_tls=True).public_url
    number = twilio_client.incoming_phone_numbers.list()[0]
    number.update(voice_url=public_url + '/call')
    print(f'Waiting for calls on {number.phone_number}')

    app.run(port=port)