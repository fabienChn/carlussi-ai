from flask import Flask, request, Response
from flask_socketio import SocketIO, emit
from google.cloud import speech

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a random secret key
socketio = SocketIO(app)

# Configure Transcription Request for German
transcription_request = {
    "config": {
        "encoding": "MULAW",
        "sampleRateHertz": 8000,
        "languageCode": "de-DE",
        "model": "phone_call",
        "useEnhanced": True,
    },
    "interimResults": True,
}

# Handle Web Socket Connection
@socketio.on('connect')
def handle_connect():
    print('New Connection Initiated')
    recognizeStream = None

    @socketio.on('message')
    def handle_message(msg):
        event = msg.get('event')
        if event == 'connected':
            print('A new call has connected.')

            # Create Stream to the Google Speech to Text API
            nonlocal recognizeStream
            recognizeStream = speech.SpeechClient().streaming_recognize(transcription_request)
            for data in recognizeStream:
                transcript = data.results[0].alternatives[0].transcript
                print(transcript)

        elif event == 'start':
            print('Starting Media Stream', msg.get('streamSid'))

        elif event == 'media':
            # Check that recognizeStream is not None and not destroyed
            if recognizeStream and not recognizeStream._stream.closed:
                # Write Media Packets to the recognize stream
                recognizeStream._stream.send(msg.get('media').get('payload'))
            else:
                print('Attempt to write to destroyed recognizeStream ignored')

        elif event == 'stop':
            print('Call Has Ended')
            if recognizeStream:
                recognizeStream._stream.close()

# Handle HTTP Request
@app.route("/", methods=["GET", "POST"])
def root():
    print("request method is:")
    print(request.method)
    if request.method == "POST":
        response = """
            <Response>
              <Start>
                <Stream url="wss://{host}/"/>
              </Start>
              <Say>I will stream the next 60 seconds of audio through your websocket</Say>
              <Pause length="60" />
            </Response>
        """.format(host=request.headers.get('Host'))
        return Response(response, content_type='text/xml')
    else:
        return "Hello World"

if __name__ == "__main__":
    print("Listening at Port 8080")
    socketio.run(app, host='0.0.0.0', port=8080)
