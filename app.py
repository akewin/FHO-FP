from flask import Flask, render_template, request
from flask_socketio import SocketIO
import pyttsx3

app = Flask(__name__)
socketio = SocketIO(app)

def speak_message(message):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', 'pt-br')
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