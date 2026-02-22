#  =============================
#  WebSocket Publisher voor BMP280-CanSat data
#  -----------------------------
#  Leest data in CSV formaat van MQTT broker 
#  en stuurt deze door via WebSocket
#  in JSON Formaat
#
#  broker, topic en filename in config.ini
#  WS server host en poort in config.ini
#
#  Auteur: F.Demonie
#  Datum: 2026-02-20
#  Versie: 1.0
#  =============================
import json
import paho.mqtt.client as mqtt
from websocket_server import WebsocketServer
import configparser
import time

# Config inlezen
CONFIG_FILE = "config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

MQTT_BROKER = config["MQTT"]["mq_broker"]
MQTT_PORT = int(config["MQTT"]["mq_port"])
MQTT_TOPIC = config["MQTT"]["mq_topic"]

WS_PORT = int(config["WS_SERVER"]["ws_port"])
WS_SERVER = config["WS_SERVER"]["ws_host"] 

# WebSocket server
def new_client(client, server):
    print("WebSocket client verbonden")

ws_server = WebsocketServer(port=WS_PORT, host=WS_SERVER)
ws_server.set_fn_new_client(new_client)

# CSV → JSON conversie
def csv_to_json(csv_line):
    parts = csv_line.split(";")
    record_type = parts[0]

    if record_type == "B":
        return {
            "type": "B",
            "temperature": float(parts[1]),
            "pressure": float(parts[2]),
            "altitude": float(parts[3])
        }
    else:
        print("ERROR: Onbekend record:", csv_line)
        return None

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Verbonden met MQTT broker ({MQTT_BROKER}:{MQTT_PORT})")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    csv_line = msg.payload.decode().strip()
    print(f"MQTT: {csv_line}")

    json_record = csv_to_json(csv_line)
    if json_record:
        ws_server.send_message_to_all(json.dumps(json_record))
        print(f"WS record verzonden: {json.dumps(json_record)}")

# ==============================
# MQTT setup
# ==============================
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Wachten tot MQTT broker beschikbaar is
while True:
    try:
        print("Verbinden met MQTT broker...")
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("MQTT verbonden!")
        break
    except Exception as e:
        print("MQTT nog niet beschikbaar, opnieuw proberen in 3 seconden...")
        time.sleep(3)

# ==============================
# Start servers
# ==============================
print(f"WebSocket server op poort {WS_PORT}")
mqtt_client.loop_start()
ws_server.run_forever()