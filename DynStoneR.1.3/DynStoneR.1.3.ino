/*
   The following code is for the most part based on code previously written by Neil Kolban, Evandro Copercini and beegee-tokyo
   Modified by Noah at BBR
*/

#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <BLEEddystoneURL.h>
#include <BLEEddystoneTLM.h>
#include <BLEBeacon.h>

#define ENDIAN_CHANGE_U16(x) ((((x)&0xFF00) >> 8) + (((x)&0xFF) << 8))

int scanTime = 1; //In seconds
BLEScan *pBLEScan;

uint8_t Ausgabe[17];

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks
{
    void onResult(BLEAdvertisedDevice advertisedDevice)
    {
      
      uint8_t *payLoad = advertisedDevice.getPayload();

      BLEUUID checkUrlUUID = (uint16_t)0xfeaa;

      if (advertisedDevice.getServiceUUID().equals(checkUrlUUID))
      {
        if (payLoad[11] == 0x10)
        {
          
          Serial.println("Found an EddystoneURL beacon!");
          BLEEddystoneURL foundEddyURL = BLEEddystoneURL();
          std::string eddyContent((char *)&payLoad[11]); // incomplete EddystoneURL struct!

          foundEddyURL.setData(eddyContent);
          std::string bareURL = foundEddyURL.getURL();
          if (bareURL[0] == 0x00)
          {
            size_t payLoadLen = advertisedDevice.getPayloadLength();
            Serial.print("DATA--> ");
            for (int idx = 0; idx < 16; idx++)
            {
              Serial.print(payLoad[idx+13]);
              Serial.print(" ");
              Ausgabe[idx] = payLoad[idx+13];
            }
            Serial.printf("\nContent is: %s", Ausgabe);
            Serial.println(" ");
            return;
          }
        }
      }
    }
};

void setup()
{
  Serial.begin(115200);
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99); // less or equal setInterval value
}

void loop()
{
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  pBLEScan->clearResults(); // delete results fromBLEScan buffer to release memory
  delay(2000);
}
