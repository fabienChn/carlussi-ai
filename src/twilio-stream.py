import asyncio
import websockets
from flask import Flask, request, Response
from google.cloud import speech_v1p1beta1 as speech
import threading
import json

app = Flask(__name__)
client = speech.SpeechClient()

request_config = {
    "config": {
        "encoding": speech.RecognitionConfig.AudioEncoding.MULAW,
        "sample_rate_hertz": 8000,
        "language_code": "de-DE",
        "model": "phone_call",
        "use_enhanced": True,
    },
    "interim_results": True,
}

async def handle_ws(websocket, path):
    recognize_stream = None
    async for message in websocket:
        message = json.loads(message)

        if message['event'] == 'connected':
            print("A new call has connected.")
            recognize_stream = client.streaming_recognize(request=request_config)
        
        elif message['event'] == 'start':
            print(f"Starting Media Stream {message['streamSid']}")

        elif message['event'] == 'media' and recognize_stream is not None:
            recognize_stream.write(message['media']['payload'])

        elif message['event'] == 'stop':
            print("Call Has Ended")
            if recognize_stream:
                recognize_stream.cancel()

        await websocket.send("Response from server")

def start_ws_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ws_server = websockets.serve(handle_ws, "0.0.0.0", 8080)
    loop.run_until_complete(ws_server)
    loop.run_forever()

@app.route('/', methods=['GET'])
def index():
    return "Hello World"

@app.route('/', methods=['POST'])
def post():
    host = request.headers['host']
    response = f"""
    <Response>
        <Start>
            <Stream url="wss://{host}/"/>
        </Start>
        <Say>I will stream the next 60 seconds of audio through your websocket</Say>
        <Pause length="60" />
    </Response>
    """
    return Response(response, content_type='text/xml')

if __name__ == '__main__':
    threading.Thread(target=start_ws_server).start()
    app.run(port=8080)
