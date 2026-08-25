---
title: LoRaWAN API References
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**NOTE**: The FreeRTOS LoRaWAN demo project is in the FreeRTOS-Labs. It is fully functional, but undergoing 
optimizations or refactoring to improve memory usage, modularity, documentation, demo usability, or test 
coverage. It is available in the [Lab-Project-FreeRTOS-LoRaWAN](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN) 
repository on GitHub separately from the main Labs Project Download. 


The following section provides detailed description and usage samples for LoRaWAN APIs in FreeRTOS.


## Setup

LoRaWAN\_Init() can be used to initialize the LoRaWAN stack for a region. It takes a region parameter 
as input and initializes the LoRaMAC stack with the default parameters for that region. This API also 
creates a background LoRaMAC task which loops and processes events from the radio and MAC layers. The 
API is not re-entrant or thread safe.

```c
LoRaMacStatus_t status;  

status = LoRaWAN_Init( LORAMAC_REGION_US915 );  

if( status == LORAMAC_STATUS_OK )   
{  
      /* Continue with LoRaWAN Activation. */  
}  
else  
{  
      /* Exit the program with the appropriate error code. */  
}  
```


## Configure network parameters for LoRaWAN

The following APIs can be used to configure the network parameters for LoRAWAN. 

`LoRaWAN_SetAdaptiveDataRate()` can be used to turn on or off adaptive data rates for the end-device. 
This API can be invoked anytime after the LoRaWAN has been initialized. Turning on adaptive data rates 
will allow the network server to calculate an optimized data rate for the end-device based on its location 
and other factors.

The APIs `LoRaWAN_GetNetworkParams()` and `LoRaWAN_SetNetworkParams()` can be used to modify other network 
parameters, such as channel frequency and data rate, for the second receive window of the device and 
TX power. If you are using Over the Air Activation (OTAA), a join should be initiated for the new parameters 
to take effect. 


## Activitation

Two types of activation are supported: Over The Air Activation (OTAA) or Activation By Personalization (ABP).

The `LoRaWAN_Join()` API is used for OTAA. Example:

```c
LoRaMacStatus_t status;  

status = LoRaWAN_Join();  

if( status == LORAMAC_STATUS_OK )   
{  
      /* Send or receive data with LoRaWAN. */  
}  
else  
{  
      /*All JOIN attempts are exhausted. Report this to end user. */  
}  
```

The API is a blocking call until join handshake is completed or all the retries are exhausted. 
The credentials required for Over the Air Activation should be provided using the getter functions below, 
or pre-provisioned using a secure element.

```c
void getDeviceEUI( uint8_t * param )  
{  
    /* Copy the 8 byte device EUI into param here. */   
}  
  
void getJoinEUI( uint8_t * param )  
{  
   /* Copy the 8 byte join EUI into param here. */  
}  
  
void getAppKey( uint8_t * param )  
{  
  /* Copy the 16 byte app key into param here. */  
}  
```

The API does Join attempts for a configured number of times. Retries are performed at random intervals 
and under different frequency bands, as recommended by the LoRaWAN specification. The number of retries 
and the retry intervals can be tuned using the following configs in `demos/classA/Nordic_NRF52/config/LoRaWANConfig.h` :

```c
#define lorawanConfigMAX_JOIN_ATTEMPTS      ( 1000 )  
#define lorawanConfigJOIN_RETRY_INTERVAL_MS ( 2000 )  
#define lorawanConfigMAX_JITTER_MS          ( 500 )  
```

(2) `LoRaWAN_ActivateByPersonalization()` API can be used for activating a device using ABP method.


```c
LoRaMacStatus_t status;  

status = LoRaWAN_ActivateByPersonalization();  
  
if( status == LORAMAC_STATUS_OK )   
{  
      /* Send or receive data with LoRaWAN. */  
}  
else  
{  
      /* ABP activation failed. Report this to end user. */  
}  
```

In the ABP method, an end-device uses its pre-provisioned credentials and does not perform a handshake 
with the Network Server. The credentials for ABP can be provided using the following getter functions:

```c
void getDeviceEUI( uint8_t * param )  
{  
    /* Copy the 8 byte device EUI into param here. */   
}  
  
void getJoinEUI( uint8_t * param )  
{  
   /* Copy the 8 byte join EUI into param here. */  
}  
  
uint32_t getDeviceAddress( void )  
{  
   /* Return the 24 bit network id of the address. */  
}  
  
void getGetAppSessionKey( uint8_t * param )  
{  
    /* Copy the 16 byte app session key into param here. */  
}  
  
void getGetNwkSessionKey( uint8_t * param )  
{  
     /* Copy the 16 byte network session key into param here. */  

}
```


## Send Uplink Data

The `LoRaWAN_Send()` API can be used to send uplink data to a LoRa Network Server. Uplink data can be 
confirmed or unconfirmed. For confirmed messages, the API blocks until an acknowledgment is received 
from the Network Server. This API also performs a configured number of retries, with different data 
rates, until it receives an acknowledgment. For unconfirmed messages, the API returns as soon as a message 
is sent out of the radio.

```c
LoRaWANMessage_t uplink;  

uplink.port = LORAWAN_APP_PORT;  
memcpy( uplink.data, &data, bytesToSend );  
uplink.length = bytesToSend;  
uplink.dataRate = dataRateToSend; /* Set to zero if using adaptive data rate. */  
  
status = LoRaWAN_Send( &uplink, IS_CONFIRMED );  
  
if( status == LORAMAC_STATUS_OK )  
{  
   /*   
    * Successfully sent uplink data.  
    * Wait for receive windows to receive any downlink data.  
    */   
}  
else  
{  
    /* Failed to send data uplink, Check end-device and gateway connectivity. */
}  
```


## Receive Downlink Data

The `LoRaWAN_Receive()` API can be used to block for a specified time until data is received. Applications 
can choose to wait for downlink data for any period of time by giving a timeout parameter in milliseconds. 
For example, for class A use cases, an application can wait for the receive window’s duration after sending 
an uplink message. The downlink queue size can be adjusted based on application needs through the 
config `lorawanConfigDOWNLINK_QUEUE_SIZE` in `demos/classA/Nordic_NRF52/config/LoRaWANConfig.h` 

```c
LoRaWANMessage_t downlink;  

status = LoRaWAN_Receive( &downlink, CLASSA_RECEIVE_WINDOW_DURATION_MS );  

if( status == pdTRUE )  
{  
    /* Successfully received downlink data. */  
    decodeData( &downlink.data, downlink.length; downlink.port );  
}  
else  
{  
     /* No data downlink. Do Nothing. */  
}  
```


## Poll for LoRaWAN Events

The `LoRaWAN_PollEvent()` API can be used to poll for any events received from the LoRaWAN network. 
The network supports receiving the following events at the application layer. 

```c
typedef enum LoRaWANEventType  
{  
    LORAWAN_EVENT_UNKNOWN = 0,                  
/**< @brief Type to denote an unexpected event type. */   
    LORAWAN_EVENT_DOWNLINK_PENDING,            
/**< @brief Indicates that server has to send more downlink data or waiting for a mac command uplink. */   
    LORAWAN_EVENT_TOO_MANY_FRAME_LOSS,         
/**< @brief Indicates too many frames are missed between end device and LoRa network server. */   
    LORAWAN_EVENT_DEVICE_TIME_UPDATED,         
/**< @brief Indicates the device time has been synchronized with LoRa network server. */   
    LORAWAN_EVENT_LINK_CHECK_REPLY             
/**< @brief Reply for a link check request from end device. */   
}
```

Applications can poll for any events by optionally blocking for them and then take appropriate actions. 
The example below shows the application behavior for two such events.

```c
BaseType_t status;  
LoRaWANEventInfo_t event;  

for (;;)  
{  
    status = LoRaWAN_PollEvent( &event, 0 );  
  
   if( status == pdTRUE )  
   {  
        switch( event.type)  
        {  
            case LORAWAN_EVENT_DOWNLINK_PENDING:  
                /*   
                 * MAC layer indicated a pending downlink event or an uplink command to be flushed.  
                 * Send an empty uplink to fetch the downlink packet.  
                 */   
                prvFetchDownlinkPacket();  
                break;  

           case LORAWAN_EVENT_TOO_MANY_FRAME_LOSS:  
                /* Too many frame loss between end-device and Network server. Trigger a re-join. */  
                LoRaWAN\_Join();   
                break;  

           ....  

           ....  

           default:  
               break;  

       }  
   }  
   else  
   {  
        break;  
   }  
}    
```

## Cleanup

The `LoRaWAN_Cleanup()` API is used to stop and de-initialize the LoRaMac stack, and delete the LoRaMac 
task and associated resources. 
