#include "sys/time.h"
#include <Arduino.h>
#include "BLEDevice.h"
#include "BLEUtils.h"
#include "BLEBeacon.h"
#include "BLEAdvertising.h"
#include "BLEEddystoneURL.h"
#include "esp_sleep.h"


#define GPIO_DEEP_SLEEP_DURATION 10     // sleep x seconds and then wake up
RTC_DATA_ATTR static time_t last;    // remember last boot in RTC Memory
RTC_DATA_ATTR static uint32_t bootcount; // remember number of boots in RTC Memory
#define BEACON_UUID "8ec76ea3-6668-48da-9866-75be8bc86f4d" // UUID 1 128-Bit (may use https://www.uuidgenerator.net/)

BLEAdvertising *pAdvertising;
struct timeval now;

const int url_len = 17;
const char URLausgabe[url_len] = "12345678xxxx.com";
char url[url_len];

unsigned long lasttime = 0;

void setBeacon()
{
  BLEAdvertisementData oAdvertisementData = BLEAdvertisementData();
  BLEAdvertisementData oScanResponseData = BLEAdvertisementData();
  
  int scheme_len, ext_len = 1, idx, url_idx;
  char *ret_data;

  ret_data = (char *)calloc(1, url_len + 13);

  ret_data[0] = 2;   // Len
  ret_data[1] = 0x01;  // Type Flags
  ret_data[2] = 0x06;  // GENERAL_DISC_MODE 0x02 | BR_EDR_NOT_SUPPORTED 0x04
  ret_data[3] = 3;   // Len
  ret_data[4] = 0x03;  // Type 16-Bit UUID
  ret_data[5] = 0xAA;  // Eddystone UUID 2 -> 0xFEAA LSB
  ret_data[6] = 0xFE;  // Eddystone UUID 1 MSB
  ret_data[7] = 19; // Length of Beacon Data
  ret_data[8] = 0x16;  // Type Service Data
  ret_data[9] = 0xAA;  // Eddystone UUID 2 -> 0xFEAA LSB
  ret_data[10] = 0xFE; // Eddystone UUID 1 MSB
  ret_data[11] = 0x10; // Eddystone Frame Type
  ret_data[12] = 0xF4; // Beacons TX power at 0m

  idx = 13;

  for(int i = 0; i < url_len; i++)
  {
    ret_data[idx+i] = url[i];
  }

// Set Length of Beacon Data to maximum allowed size of 30 bytes
  ret_data[7] = 30 - 8;

  Serial.printf("struct size %d url size %d reported len %d\n",
                url_len + 13,
                url_len, ret_data[7]);

  Serial.printf("URL in data %s\n", &ret_data[13]);

  std::string eddyStoneData(ret_data);

  oAdvertisementData.addData(eddyStoneData);
  oScanResponseData.setName("URLBeacon");
  pAdvertising->setAdvertisementData(oAdvertisementData);
  pAdvertising->setScanResponseData(oScanResponseData);
}

void setupBeacon()
{
  gettimeofday(&now, NULL);
  Serial.printf("start ESP32 %d\n", bootcount++);

  last = now.tv_sec;

  // Create the BLE Device
  BLEDevice::init("URLBeacon");

  BLEDevice::setPower(ESP_PWR_LVL_N12);

  // Create the BLE Server
  // BLEServer *pServer = BLEDevice::createServer(); // <-- no longer required to instantiate BLEServer, less flash and ram usage

  pAdvertising = BLEDevice::getAdvertising();

  setBeacon();
  // Start advertising
  pAdvertising->start();
}
void changeURL()
{
  Serial.println("Advertizing started...");
  delay(1000);
  
  Serial.println("Bitte URL eingeben"); //Prompt User for Input
    delay(1000);

  String newURL;
  newURL = Serial.readString(); //Read the data the user has put in
  Serial.println(newURL);
  newURL.toCharArray(url, 17);
}

void setup() {
Serial.begin(115200);
memcpy (url, URLausgabe, url_len);
setupBeacon();
}

void loop() {
if (Serial.available() > 0) {
  changeURL();
  setupBeacon();
  
}
  if (millis() > lasttime + 1000)
  {
    Serial.println("I am available!");
    lasttime = millis();
  }

}
