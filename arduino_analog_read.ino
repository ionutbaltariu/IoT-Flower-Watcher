int sensorPin = A0; 
int sensorValue;  
int limit = 300; 
String json ="";

float moisture_percent = 0;

void setup() {
 Serial.begin(9600);
}

void loop() {

 sensorValue = analogRead(sensorPin); 
 sensorValue = map(sensorValue, 150, 700, 0, 100);
 moisture_percent = (1-(float)sensorValue/100);
 json = "{\"moisture\":\""+String(moisture_percent)+"\"}";
 Serial.println(json);
 delay(1000); 
}
