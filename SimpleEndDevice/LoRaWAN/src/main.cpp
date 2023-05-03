#include "LoRaWan_APP.h"
#include <Arduino.h>
#include "driver/temp_sensor.h"
#include "TinyGPS++.h"

TinyGPSPlus gps;

uint8_t devEui[] = {0x4B, 0x4D, 0xC4, 0xBB, 0x8C, 0xD1, 0x67, 0x3A};  
bool overTheAirActivation = true;
uint8_t appEui[] = {0x65, 0xFE, 0xC7, 0x6D, 0xB1, 0xA0, 0x66, 0xC1};  // you should set whatever your TTN generates. TTN calls this the joinEUI, they are the same thing. 
uint8_t appKey[] = {0x25, 0xC3, 0x54, 0xC3, 0x63, 0x8E, 0xF6, 0x0B, 0xAF, 0xDB, 0xA6, 0x4A, 0x1C, 0xEB, 0x6D, 0xB9};  // you should set whatever your TTN generates 

//These are only used for ABP, for OTAA, these values are generated on the Nwk Server, you should not have to change these values
uint8_t nwkSKey[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
uint8_t appSKey[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
uint32_t devAddr =  (uint32_t)0x00000000;  

/*LoraWan channelsmask*/
uint16_t userChannelsMask[6]={ 0xFF00,0x0000,0x0000,0x0000,0x0000,0x0000 };

/*LoraWan region, select in arduino IDE tools*/
LoRaMacRegion_t loraWanRegion = ACTIVE_REGION;  // we define this as a user flag in the .ini file. 

/*LoraWan Class, Class A and Class C are supported*/
DeviceClass_t  loraWanClass = CLASS_A;

/*the application data transmission duty cycle.  value in [ms].*/
uint32_t appTxDutyCycle = 15000;

/*ADR enable*/
bool loraWanAdr = true;

void initTempSensor(){
    temp_sensor_config_t temp_sensor = TSENS_CONFIG_DEFAULT();
    temp_sensor.dac_offset = TSENS_DAC_L2; //TSENS_DAC_L2 is default, range: -10 to 80 degree celcius
    temp_sensor_set_config(temp_sensor);
    temp_sensor_start();
}

// uint32_t license[4] = {};

/* Indicates if the node is sending confirmed or unconfirmed messages */
bool isTxConfirmed = true;

/* Application port */
uint8_t appPort = 1;
/*!
* Number of trials to transmit the frame, if the LoRaMAC layer did not
* receive an acknowledgment. The MAC performs a datarate adaptation,
* according to the LoRaWAN Specification V1.0.2, chapter 18.4, according
* to the following table:
*
* Transmission nb | Data Rate
* ----------------|-----------
* 1 (first)       | DR
* 2               | DR
* 3               | max(DR-1,0)
* 4               | max(DR-1,0)
* 5               | max(DR-2,0)
* 6               | max(DR-2,0)
* 7               | max(DR-3,0)
* 8               | max(DR-3,0)
*
* Note, that if NbTrials is set to 1 or 2, the MAC will not decrease
* the datarate, in case the LoRaMAC layer did not receive an acknowledgment
*/
uint8_t confirmedNbTrials = 8;


static uint8_t battery_percent = 100;

/* Prepares the payload of the frame */
static void prepareTxFrame( uint8_t port )
{
	/*appData size is LORAWAN_APP_DATA_MAX_SIZE which is defined in "commissioning.h".
	*appDataSize max value is LORAWAN_APP_DATA_MAX_SIZE.
	*if enabled AT, don't modify LORAWAN_APP_DATA_MAX_SIZE, it may cause system hanging or failure.
	*if disabled AT, LORAWAN_APP_DATA_MAX_SIZE can be modified, the max value is reference to lorawan region and SF.
	*for example, if use REGION_CN470, 
	*the max value for different DR can be found in MaxPayloadOfDatarateCN470 refer to DataratesCN470 and BandwidthsCN470 in "RegionCN470.h".
	*/
    // This data can be changed, just make sure to change the datasize as well. 

	double lat = gps.location.lat();
	double lng = gps.location.lng();
	double speed = gps.speed.mps();
	if(battery_percent > 0){
		battery_percent -= 10;
	}

	char* lat_bits = (char*)&lat;
	char* lng_bits = (char*)&lng;
	char* speed_bits = (char*)&speed;

    appDataSize = 25;
	for(int i = 0; i < 8; i++){
		appData[i] = lat_bits[i];
		appData[i+8] = lng_bits[i];
		appData[i+16] = speed_bits[i];
	}

	appData[24] = battery_percent;
	Serial.println(lat);
	Serial.println(lng);
	Serial.println(speed);
}


RTC_DATA_ATTR bool firstrun = true;

void setup() {
  Serial.begin(115200);
  Mcu.begin();
  if(firstrun)
  {
    LoRaWAN.displayMcuInit();
    firstrun = false;
  }
	deviceState = DEVICE_STATE_INIT;
}

void loop()
{
	
	switch( deviceState )
	{
		case DEVICE_STATE_INIT:
		{
#if(LORAWAN_DEVEUI_AUTO)
			LoRaWAN.generateDeveuiByChipID();
#endif
			LoRaWAN.init(loraWanClass,loraWanRegion);
			break;
		}
		case DEVICE_STATE_JOIN:
		{
      LoRaWAN.displayJoining();
			LoRaWAN.join();
			if (deviceState == DEVICE_STATE_SEND){
			 	LoRaWAN.displayJoined();
			}
			break;
		}
		case DEVICE_STATE_SEND:
		{
      		LoRaWAN.displaySending();
			prepareTxFrame( appPort );
			LoRaWAN.send();
			deviceState = DEVICE_STATE_CYCLE;
			break;
		}
		case DEVICE_STATE_CYCLE:
		{
			// Schedule next packet transmission
			txDutyCycleTime = 20000;
			LoRaWAN.cycle(txDutyCycleTime);
			deviceState = DEVICE_STATE_SLEEP;
			break;
		}
		case DEVICE_STATE_SLEEP:
		{
      		LoRaWAN.displayAck();
			LoRaWAN.sleep(loraWanClass);
			break;
		}
		default:
		{
			deviceState = DEVICE_STATE_INIT;
			break;
		}
	}
}