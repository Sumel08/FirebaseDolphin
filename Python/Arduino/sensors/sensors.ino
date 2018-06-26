#include <NewPing.h>

#define TRIGGER_PIN 6
#define ECHO_PING 7
#define MAX_DISTANCE 400

NewPing sonar(TRIGGER_PIN, ECHO_PING, MAX_DISTANCE);
const int IN_A0 = A0;

void setup() {
    pinMode (IN_A0, INPUT);
    Serial.begin(9600);
}

void loop() {
    delay(1000);
    Serial.println(get_data());
}

float get_temperature() {

  return 12.5;
}

float get_humidity() {

  return 10.05;
}

float get_distance() {
  return sonar.ping_cm();
}

int get_luminosity() {
  return analogRead(0);
}

String get_data() {
 return "{\"temperature\": " + String(get_temperature()) + ", \"humidity\": " + String(get_humidity()) + ", \"distance\": " + String(get_distance()) + ", \"luminosity\": " + String(get_luminosity()) + "}"; 
}

