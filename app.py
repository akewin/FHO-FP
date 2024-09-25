from flask import Flask, render_template, request
from flask_socketio import SocketIO
import pyttsx3

app = Flask(__name__)
socketio = SocketIO(app)

def speak_message(message):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # List all available voices
    for voice in voices:
        print(f"Voice: {voice.name}, ID: {voice.id}, Lang: {voice.languages}")

    # Set the voice to Portuguese (Brazil)
    for voice in voices:
        if 'pt_BR' in voice.id:
            engine.setProperty('voice', voice.id)
            break
    else:
        print("Portuguese (Brazil) voice not found. Using default voice.")

    engine.setProperty('rate', 150)
    engine.say(message)
    engine.runAndWait()
    engine.stop()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('speak')
def handle_speak(message):
    print(f"Falando: {message}")
    speak_message(message)
    socketio.emit('spoken', {'message': message})

@app.route('/esp8266', methods=['POST'])
def handle_esp8266():
    message = request.data.decode('utf-8')
    print(f"Mensagem do ESP8266: {message}")
    socketio.emit('esp8266_message', {'message': message})
    speak_message(message)
    return "OK"

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)