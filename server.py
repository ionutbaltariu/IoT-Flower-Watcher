from flask import Flask, render_template
import time
import json
import serial
import threading
import Adafruit_DHT
import time
import smtplib
import datetime
import os
from buzzer import *
from email.mime.text import MIMEText

app = Flask(__name__)

last_soil_humidity_value = 0
last_temperature_value = 0
last_air_humidity_value = 0
last_sent_email_hour = 0
last_sent_email_hour_th = 0
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
email = 'iotflowermonitoring@gmail.com'
email_password = str(os.environ.get("iot_password"))
mutex = threading.Lock()

def send_mail(message):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email,email_password)
                    

    email_content = MIMEText(message,'plain')
    email_content['Subject']= 'Flower Monitoring Report'

    server.sendmail(email,"ionut.alexandru.baltariu@gmail.com",email_content.as_string())
    server.quit()

    print("Sent mail!")

@app.route('/')
def index():
    return render_template('index.html', soil_humidity=str(last_soil_humidity_value), temperature=str(last_temperature_value),
            air_humidity=str(last_air_humidity_value))

@app.route('/',methods=['POST']) 
def on_play():
    setup()
    play(final_countdown_melody, final_countdown_tempo, 0.30, 1.2000)
    return index()

def get_values_from_serial():
    global last_soil_humidity_value
    global last_sent_email_hour
    global email_password
    ser = serial.Serial('/dev/ttyACM0',9600, timeout=1)
    while True:
        try:
            read_serial=ser.readline()
            read_json = json.loads(read_serial.decode())
            if(read_json['moisture'] is not None):
                last_soil_humidity_value = float(read_json['moisture'])*100
                if last_soil_humidity_value < 50 and (abs(last_sent_email_hour - datetime.datetime.now().hour)) >= 1:
                    last_sent_email_hour = datetime.datetime.now().hour
                    msg = "Your flower has low soil moisture (" + str(last_soil_humidity_value) + ")! Water it urgently!"
                    mutex.acquire()
                    send_mail(msg)
                    mutex.release()

            print(last_soil_humidity_value)
        except json.decoder.JSONDecodeError:
            pass
        except serial.serialutil.SerialException:
            pass


def read_temperature_and_humidity():
    global last_air_humidity_value
    global last_temperature_value
    global last_sent_email_hour_th
    global mutex
    while True:
        air_humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if air_humidity is None and temperature is None:
            print("error")
        else:
            last_air_humidity_value = air_humidity
            last_temperature_value = temperature
            if (temperature < 18 or temperature >= 30 or air_humidity < 25 or air_humidity > 50) and abs(last_sent_email_hour_th - datetime.datetime.now().hour) >= 1: 
                msg = "Temperature/air humidity in flower room too low/high:" + str(temperature) + "*C and " + str(air_humidity) + "%"
                last_sent_email_hour_th = datetime.datetime.now().hour
                mutex.acquire()
                send_mail(msg)
                mutex.release()
        time.sleep(3)


moisture_thread = threading.Thread(target=get_values_from_serial)
dht11_thread = threading.Thread(target=read_temperature_and_humidity)

if __name__ == '__main__':
    moisture_thread.start()
    dht11_thread.start()
    app.run(host='0.0.0.0')
