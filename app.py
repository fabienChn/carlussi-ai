from flask import Flask, request
from flask_sockets import Sockets
from twilio.rest import Client
from twilio.twiml.voice_response import Start, VoiceResponse
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from websocket import WebSocketConnectionClosedException as ConnectionClosed
import torchaudio
import json
import base64
import numpy as np

app = Flask(__name__)
sock = Sockets(app)
twilio_client = Client()

# Initialize Wav2Vec model
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

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
            waveform, _ = torchaudio.load(audio, num_frames=16000)
            inputs = tokenizer(waveform.numpy()[0], return_tensors="pt", padding=True)
            logits = model(inputs.input_values.to("cpu"), attention_mask=inputs.attention_mask.to("cpu")).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = tokenizer.decode(predicted_ids[0])
            print(transcription)
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
