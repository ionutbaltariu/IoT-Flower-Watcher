from flask import Flask, render_template
import time
import json
import serial
import threading
import Adafruit_DHT
import time

app = Flask(__name__)

last_soil_humidity_value = 0
last_temperature_value = 0
last_air_humidity_value = 0
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

@app.route('/')
def index():
    return render_template('index.html', soil_humidity=str(last_soil_humidity_value), temperature=str(last_temperature_value),
            air_humidity=str(last_air_humidity_value))

def get_values_from_serial():
    global last_soil_humidity_value 
    ser = serial.Serial('/dev/ttyACM0',9600, timeout=1)
    while True:
        try:
            read_serial=ser.readline()
            read_json = json.loads(read_serial.decode())
            if(read_json['moisture'] is not None):
                last_soil_humidity_value = float(read_json['moisture'])*100
            print(last_soil_humidity_value)
        except json.decoder.JSONDecodeError:
            pass
        except serial.serialutil.SerialException:
            pass


def read_temperature_and_humidity():
    global last_air_humidity_value
    global last_temperature_value
    while True:
        air_humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if air_humidity is None and temperature is None:
            print("error")
        else:
            last_air_humidity_value = air_humidity
            last_temperature_value = temperature
        time.sleep(30)


moisture_thread = threading.Thread(target=get_values_from_serial)
dht11_thread = threading.Thread(target=read_temperature_and_humidity)

if __name__ == '__main__':
    moisture_thread.start()
    dht11_thread.start()
    app.run(host='0.0.0.0')
