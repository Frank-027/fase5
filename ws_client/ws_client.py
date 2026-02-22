import websocket
import json
import mariadb
import time

# Configuratie voor WebSocket client
WS_HOST = "mqtt_to_ws"
WS_PORT = 8765
WS_URL = f"ws://{WS_HOST}:{WS_PORT}"

#database connectie
def connect_db(retries=10, delay=3):
    for attempt in range(retries):
        try:
            conn = mariadb.connect(
                user="cansatuser",
                password="SkyByte26",
                host="mariadb",
                port=3306,
                database="cansatdb"
            )
            print("[DB] Verbonden met MariaDB")
            return conn
        except mariadb.Error as e:
            print(f"[DB] Connectie poging {attempt+1} mislukt: {e}")
            time.sleep(delay)
    print("[DB] Kan geen verbinding maken na meerdere pogingen.")
    return None
    
def insert_measurement(conn, data):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO measurements (type, temperature, pressure, altitude) VALUES (?, ?, ?, ?)",
            (data.get("type"), data.get("temperature"), data.get("pressure"), data.get("altitude"))
        )
        conn.commit()
        print(f"[DB] Gegevens succesvol opgeslagen in de database: {data}")
    except mariadb.Error as e:
        print(f"[DB] Error inserting data: {e}")    

# Haal een record op van de WebSocket en sla deze op in de database
conn = connect_db() #één connectie maken voor de hele loop
if conn is None:
    print("[DB] Stoppen: geen verbinding met database mogelijk!")
    exit(1)  # script stoppen omdat DB connectie niet lukt

def on_message(ws, message):
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        print(f"[WS] Fout bij het decoderen van JSON: {message}")
        return
    except KeyError as e:
        print(f"[WS] Ontbrekende sleutel in data: {e}")
        return
    
    print("Ontvangen data:")
    for key, value in data.items():
        print(f"{key}: {value}")
    if conn:
        insert_measurement(conn, data)

    print(f"[{time.strftime('%H:%M:%S')}] - {'-'*30}")  # scheiding tussen records

def on_open(ws):
    print(f"Verbonden met WebSocket server {WS_URL}")
 
# --------------------------------
# Main execution
# --------------------------------
print(f"Starten WebSocket client, verbinding maken met {WS_URL}...")

ws = websocket.WebSocketApp(
    WS_URL,
    on_message=on_message,
    on_open=on_open
)

ws.run_forever()