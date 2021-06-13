# IoT Flower Monitoring
Repository for the Project at the Microprocessor Systems Discipline - consists of a simple flower monitoring application made using Python, a Raspberry Pi 3, Arduino, DHT11, a soil moisture sensor and a buzzer.

## [Project on Hackster](https://www.hackster.io/flowerpower/flower-monitoring-using-raspberry-pi-arduino-fbcad8)

# Story

Imagine what life would be like without our inanimate green friends.. Flowers, beyond the fact that they are excellent items for decoration of various environments, are actual stress reducers and nature maintainers ( producing oxygen through photosynthesis).

We all know how busy the modern life of a programmer can get, especially with the chaotic schedules the pandemic times brought upon us, therefore we thought of automating the process of checking how 'healthy' a plant is at the current moment of time.

# Installation&use instructions

* Install the required Python modules
```
python3 -m pip install requirements.txt
```

* Make sure to upload the **Arduino** sketch to your board.
* Connect the sensors/actuators as indicated in the schematic found [here](https://www.hackster.io/flowerpower/flower-monitoring-using-raspberry-pi-arduino-fbcad8)
* Create a new email address or use an already existent one to send warning emails from.
* Modify server.py 'email' variable with your email of use.
* Set the email password as an enviornment variable

```
sudo vim ~/.bashrc
```

Add following line to your .bashrc

```
export iot_password="<Your_password_here>" 
```

Execute in the current shell environment.

```
source ~/.bashrc
```


* Run the Flask web server

```
python3 server.py
```
## The website is now running at the following link: 

```
<your_raspberry_pi_local_ip>:5000 
```

# Key concepts learned:

* teamwork: project planning, task allocation
* improved knowledge about threading, Flask, UART, Raspberry Pi 3, Arduino
* using Raspberry Pi 3 pins and various sensors/actuators
* Linux administration
* ssh
* basic Electronics knowledge
* sending emails with stmplib and MIMEText
