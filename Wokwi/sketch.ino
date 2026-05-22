#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 15
#define DHTTYPE DHT22

#define MQ2PIN 34
#define LEDPIN 19
#define BUZZERPIN 18

const char* ssid = "Wokwi-GUEST";
const char* password = "";

String apiKey = "CNHIRY1SMA4SYZ0M";

DHT dht(DHTPIN, DHTTYPE);

void setup() {

  Serial.begin(115200);

  dht.begin();

  pinMode(LEDPIN, OUTPUT);
  pinMode(BUZZERPIN, OUTPUT);

  Serial.println("================================");
  Serial.println("SMART AIR QUALITY MONITORING");
  Serial.println("================================");

  WiFi.begin(ssid, password);

  Serial.print("Menghubungkan WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected!");
  Serial.print("IP Address : ");
  Serial.println(WiFi.localIP());

  Serial.println();
}

void loop() {

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  int gasValue = analogRead(MQ2PIN);

  if (isnan(humidity) || isnan(temperature)) {

    Serial.println("Gagal membaca sensor DHT22");
    delay(2000);
    return;
  }

  String statusUdara;
  int statusCode;

  if (gasValue < 1000) {

    statusUdara = "BAIK";
    statusCode = 1;

    digitalWrite(LEDPIN, LOW);
    noTone(BUZZERPIN);

  }
  else if (gasValue < 2500) {

    statusUdara = "SEDANG";
    statusCode = 2;

    digitalWrite(LEDPIN, HIGH);
    noTone(BUZZERPIN);

  }
  else {

    statusUdara = "BURUK";
    statusCode = 3;

    digitalWrite(LEDPIN, HIGH);
    tone(BUZZERPIN, 1000);
  }

  Serial.println("================================");

  Serial.print("Suhu : ");
  Serial.print(temperature);
  Serial.println(" C");

  Serial.print("Kelembapan : ");
  Serial.print(humidity);
  Serial.println(" %");

  Serial.print("Gas MQ2 : ");
  Serial.println(gasValue);

  Serial.print("Status : ");
  Serial.println(statusUdara);

  Serial.print("Status Code : ");
  Serial.println(statusCode);

  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;

    String url =
      "http://api.thingspeak.com/update?api_key=" + apiKey +
      "&field1=" + String(temperature) +
      "&field2=" + String(humidity) +
      "&field3=" + String(gasValue) +
      "&field4=" + String(statusCode);

    http.begin(url);

    int httpResponseCode = http.GET();

    Serial.print("ThingSpeak Response : ");
    Serial.println(httpResponseCode);

    http.end();
  }

  Serial.println();

  delay(20000);
}