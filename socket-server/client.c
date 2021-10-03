#include <WiFi.h>
#include "Wire.h"

// Constants for data manipulation
const int MPU_ADDR = 0x68;

// Constants for connections
const char* ssid = "yourNetworkName";
const char* password =  "yourNetworkPass";
 
const uint16_t port = 5050 ;
const char * host = "WiFi.localIP";

struct variables
{  
  int pressure, ax, ay, az, gx, gy, gz;
  bool erase, calibrate;
};

void setup() {
 
  Serial.begin(115200);
 
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
 
}

void loop() {
    WiFiClient client;
 
    if (!client.connect(host, port)) {
 
        Serial.println("Connection to host failed");
 
        delay(10);
        return;
    }

    

    Serial.println("Connected to server successful!");
 
    client.print("Hello from ESP32!");
 
    Serial.println("Disconnecting...");
    client.stop();
 
    delay(10000);
}