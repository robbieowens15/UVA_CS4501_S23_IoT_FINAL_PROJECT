from flask import Flask, request
import json
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'nam1.cloud.thethings.network'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'group11app@ttn'
app.config['MQTT_PASSWORD'] = 'NNSXS.IYW7VFU4FDUSCDDL4A5HHCGPMEY6N22B6Z44SGI.SUJKEKTTIPXNM45WVYMDCTOMX7PNJPLJCKEX2YC5WPTCNRFPBD4A'
app.config['MQTT_TLS_ENABLED'] = False
topic = 'v3/+/devices/+/up'

mqtt_client = Mqtt(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")


@app.route("/")
def index():
    return "Hello World"

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if(rc == 0):
        print("connected")
        mqtt_client.subscribe(topic)
    else:
        print('Not connected')

@socketio.on('connect')
def connect_socket():
    print('client connected')
    socketio.emit('hello','Connected to Flask websocket')

@mqtt_client.on_message()
def messages(client, userdata, message):
    print("message recieved: "+ message.payload)
    lat = float(message.payload[0:7])
    lng = float(message.payload[8:15])
    speed = float(message.payload[16:])
    outgoing = {"lat":lat, "lng":lng, "speed":speed}
    socketio.emit('ttn_data', outgoing)

