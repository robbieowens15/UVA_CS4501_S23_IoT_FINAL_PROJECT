from flask import Flask, request
import json
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json
import base64
import math
import struct
app = Flask(__name__)


app.config['MQTT_BROKER_URL'] = 'nam1.cloud.thethings.network'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'group11app@ttn'
app.config['MQTT_PASSWORD'] = 'NNSXS.IYW7VFU4FDUSCDDL4A5HHCGPMEY6N22B6Z44SGI.SUJKEKTTIPXNM45WVYMDCTOMX7PNJPLJCKEX2YC5WPTCNRFPBD4A'
app.config['MQTT_TLS_ENABLED'] = False
topic = 'v3/+/devices/+/up'

mqtt_client = Mqtt(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

base_lat = 38.031770
base_lng = -78.511003


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
    message_json = json.loads(message.payload.decode())
    decoded_payload = base64.b64decode(message_json['uplink_message']['frm_payload'])
    
    lat_lng_speed = struct.unpack('dddb', decoded_payload)
    print('Lat: '+str(lat_lng_speed[0])+'\nLng: '+str(lat_lng_speed[1])+'\nSpeed: '+str(lat_lng_speed[2])+'\nBattery: '+str(lat_lng_speed[3]))
    outgoing = {"lat":lat_lng_speed[0], "lng":lat_lng_speed[1], "speed":lat_lng_speed[2], "battery":lat_lng_speed[3]}
    socketio.emit('ttn_data', outgoing)
    if(lat_lng_speed[3] < 20): #if the battery is lower than 20%
        mqtt_client.publish('v3/+/devices/+/down/push', 0x0001)


