import json
import serial

ser = serial.Serial('/dev/ttyACM1',9600)
while True:
    try:
        read_serial=ser.readline()
        print(json.loads(read_serial.decode()))
    except json.decoder.JSONDecodeError:
        pass
