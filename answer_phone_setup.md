*Twilio Programmable Voice with Flask
This project uses Flask and Twilio's Programmable Voice API to set up a web application that can answer incoming calls and respond with a speech message.*

# Project Setup

Follow these steps to set up the project:

### Activate the Virtual Environment

Open a terminal and navigate to the project's directory, then type:

`source myenv/bin/activate`

### Install the Required Libraries

You will need the Flask and Twilio libraries for this project:

`pip install flask twilio`

### Start the Flask Application

With the virtual environment activated, you can start the Flask application using the following command:

`python answer_phone.py`

Your application should now be running at http://127.0.0.1:5000.

### Run Ngrok

In a new terminal window, start ngrok on the same port where your Flask app is running:

`./ngrok http 5000`

Once ngrok is running, you will see an output like this:

`Forwarding                    https://e40a-185-238-219-91.ngrok.io -> http://localhost:5000 
The URL https://e40a-185-238-219-91.ngrok.io is your ngrok URL, which routes to your local Flask application.`

### Set Up Your Twilio Phone Number

Log into the Twilio Console, and go to the "Phone Numbers" section.

Click on your Twilio number, and in the "Voice & Fax" configuration settings, set the "A Call Comes In" Webhook URL to your ngrok URL appended with `/answer`.

https://e40a-185-238-219-91.ngrok.io/answer

### Test the Application

To test the application, simply call your Twilio phone number from your mobile phone. You should hear the message specified in `answer_phone.py`.

Replace https://e40a-185-238-219-91.ngrok.io with your unique ngrok URL.

The Flask application in `answer_phone.py` defines a single route, `/answer`, which is used to handle incoming calls. When this route is hit, it responds with TwiML to instruct Twilio to read a message aloud to the caller.