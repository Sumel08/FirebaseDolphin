void setup() {
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

String get_data() {
 return "{\"temperature\": " + String(get_temperature()) + ", \"humidity\": " + String(get_humidity()) + "}"; 
}

