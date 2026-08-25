---
title: FreeRTOS support for LoRaWAN Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**NOTE**: The FreeRTOS Support for LoRaWAN demo project is in the FreeRTOS-Labs. It is fully functional, 
but undergoing optimizations or refactoring to improve memory usage, modularity, documentation, demo 
usability, or test coverage. It is available in 
the [Lab-Project-FreeRTOS-LoRaWAN](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN) repository 
on GitHub separately from the main Labs Project Download. 

As described above, Class A offers the most energy efficient mode of communication and results in the 
longest battery life. Both uplink and downlink messages can be either confirmed (an ACK is required 
from the other party) or unconfirmed (no-ACK required). The following diagrams Figure 3a and 3b shows 
the sequence of confirmed uplink and downlink. For detailed explanation, refer to Section 18 
of [LoRaWAN 1.0.3](https://lora-alliance.org/wp-content/uploads/2020/11/lorawan1.0.3.pdf) specification. 

[![](/media/2020/Figure-3a.png)](/media/2020/Figure-3a.png)   
*Figure 3a - Uplink timing diagram for confirmed data messages (Source: LoRa Alliance) Click to enlarge.*

[![](/media/2020/Figure-3b.png)](/media/2020/Figure-3b.png)   
*Figure 3b - Downlink timing diagram for confirmed data messages (Source: LoRa Alliance) Click to enlarge.*

The demo on this page describes a working example of Class A application. It spawns a Class A application 
task which sends an uplink message periodically following t link he fair access policy defined by 
the [LoRaWAN regional parameters](https://resources.lora-alliance.org/technical-specifications/rp002-1-0-4-regional-parameters). 
Uplink messages can be sent either in confirmed or unconfirmed mode. After a successful uplink, the 
task waits for any downlink messages or other events from the MAC layer. It writes the frame payload 
and port received downlink to the console. If MAC layer indicates that there are further downlink messages 
pending or an uplink needs to be sent for control purposes, then it sends an empty uplink immediately. 
If a frame loss is detected by MAC layer, then it triggers a re-join procedure to reset the frame counters. 
Once all downlink data and events are processed, the task goes back to sleep until the next transfer cycle.

All events from MAC layer to application are sent using light weight task notifications. LoRaWAN allows 
multiple requests for the server to be piggy-backed to an uplink message. The responses to these requests 
are received by application in order using a queue. A downlink queue exists in case application wants 
to read multiple payloads received at once, before sending an uplink payload. 


## Low Power Mode

An important feature of Class A based communication is that application sleeps for most part of its 
lifecycle thereby consuming less power. Low power mode can be enabled for the demo using 
FreeRTOS [tickless idle feature](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support). Tickless idle mode can be enabled by providing 
a board specific implementation for `portSUPPRESS_TICKS_AND_SLEEP()` macro and setting `configUSE_TICKLESS_IDLE` 
to the appropriate value in FreeRTOSConfig.h. Enabling tickless mode allows MCU to sleep when the tasks are 
idle, but be waken up by an interrupt from the radio or other timer events.


## Getting Started

Hardware needed for the demo described in this blog post:

* Nordic NRF52840-Dev Kit
* Semtech sx1262mb2cas (comes with the Antenna)
* [LoRa Raspberry Pi Gateway](https://www.sparkfun.com/products/15336) ([Getting Started](https://cdn.sparkfun.com/assets/3/0/d/e/2/Get_Start_with_RAK2245_Pi_HAT_V2.4R.pdf) 
  and connecting gateway to The Things Network - not covered in this page)


### Supported Platforms

| Vendor | MCU | LoRa Radio Shield | IDE |
| ------ | --- | ----------------- | --- |
| Nordic | [NRF52840-DK](https://www.nordicsemi.com/Software-and-Tools/Development-Kits/nRF52840-DK) | [sx1262mb2cas](https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1262mb2cas) | [Segger Embedded Studio (SES)](https://www.segger.com/downloads/embedded-studio) |
| STMicroeletronics | [STM32-L4](https://www.st.com/en/microcontrollers-microprocessors/stm32l4-series.html) | [sx1276MB1LAS](https://www.semtech.com/products/wireless-rf/lora-transceivers/sx1276mb1las) | [System workbench for STM32](https://www.st.com/en/development-tools/sw4stm32.html) |


## Quick setup

###  Device Hardware Setup (Nordic NRF52840 + Semtech SX126x Mbed Radio)

The Nordic NRF52480 development kit is shown in Figure 4 and the Mbed shield for Semtech SX126x LoRa 
Radio transceiver is shown in Figure 5.

[![](/media/2020/Figure-4.png)](/media/2020/Figure-4.png)   
*Figure 4: Nordic NRF52840-DK Board  Click to enlarge.*

[![](/media/2020/Figure-5.png)](/media/2020/Figure-5.png)   
*Figure 5: Semtech SX126x LoRa Radio transceiver  Click to enlarge.*

The kit is compatible with the Arduino Uno version 3 standard, which makes it possible to stack the 
SX126x shield on top of it as shown in Figure 6. The Nordic MCU runs FreeRTOS and the LoRa MAC layer, 
and it communicates with the LoRa Radio transceiver over SPI, GPIO and Uart interfaces.

[![](/media/2020/Figure-6-right-scaled.jpg)](/media/2020/Figure-6-right-scaled.jpg)   
*Figure 6 Nordic NRF52840-DK Board and Semtech SX126x LoRa put together Click to enlarge.*


###  Setup IDE

* [Download the latest Segger Embedded studio IDE for ARM](https://www.segger.com/downloads/embedded-studio/)
* Install Embedded studio IDE for ARM IDE.


###  Download and view code

- [Setup SSH with Git repo](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account).

- Download the [repository](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN.git), along with the dependent repositories:

  ```c
  git clone --recurse-submodules https://github.com/FreeRTOS/Lab-Project-FreeRTOS-LoRaWAN.git  
  ```

- FreeRTOS LoRaWAN implementation uses a slightly patched version of LoRaMac-Node v4.4.4. The patch is 
  used to expose a radio HAL callback to notify of the interrupt events from radio. To apply the patch: 

  ```c
  cd Lab-Project-FreeRTOS-LoRaWAN  

  git apply --whitespace=fix FreeRTOS-LoRaMac-node-v4_4_4.patch  
  ```

- Open Solution in the Segger Embedded Studio from the following path: 
  `demos/classA/Nordic_NRF52/classa_demo.emProject`

  [![](/media/2020/Figure-7.png)](/media/2020/Figure-7.png)   
  *Figure 7 Segger IDE showing ClassA Demo Project  Click to enlarge.*


###  Device registration on The Things Network (TTN)

Before end-device can communicate via The Things Network (TTN), follow 
the [steps](https://www.thethingsnetwork.org/docs/devices/registration.html)  to register it with an 
application.


### Set up the Activation Credentials

Over the Air Activation (OTAA) and Activation By Personalization (ABP) methods require Device EUI, Join 
EUI, and the necessary keys to be provisioned within the device. For a production use case, it is strongly 
recommended that you pre-provision these credentials using a secure element. To support pre-provisioned 
credentials, a user needs to provide an implementation of a secure element using the interface secure-element.h 
provided by the LoRaMac-node. Reference implementations for different secure elements can be found in 
the LoRaMac-node repository. 

The sample provided uses a software-based secure element. The credentials can be retrieved either from 
a memory location or flash using getter functions. By default, the sample hardcodes the credentials 
as const static variables. The steps below describe how to set the values of these variables.

* Go to the file `demos/classA/common/credentials.c` and configure the global variables based on the 
  activation type for the demo. NOTE: The parameters are provided as an array of hex values that represent 
  bytes in big-endian ordering.

* For Over The Air Activation (OTAA):
  + Set the variable devEUI to the 8 byte globally unique device EUI.
  + Set the variable joinEUI to the 8 byte join EUI.
  + Set appKey to the 16 byte pre-shared network key.

* For Activation By Personalization (ABP):
  + Set the variable devEUI to the 8 byte globally unique device EUI.
  + Set variable joinEUI to the 8 byte join EUI.
  + Set the variables appSessionKey and nwkSessionKey to the 16 byte pre-shared session keys.
  + Set END\_DEVICE\_ADDR to the 24 bit NET ID which is pre-allocated.

  ```c
  /**  
   * @brief Device EUI needed for both OTAA and ABP activation.  
   */  
  static const uint8_t devEUI[ 8 ] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };  
    
  /**  
   * @brief JOIN EUI needed for both OTAA and ABP activation.  
   */  
  static const uint8_t joinEUI[ 8 ] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };  
    
  /**  
   * @brief App key required for OTAA activation.  
   */  
  static const uint8_t appKey[ 16 ] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };  
  ```

* Comment out or remove the line beginning with #error 
 
  ```c
  #error "Please configure DEV EUI, Join EUI and App key to run the demo using OTAA"  
  ```


### Set up the LoRaWAN Region

* Selecting a region for the sample will also select the frequency plan and other parameters for LoRaMAN, 
  per [LoRaWAN regional parameters](https://resources.lora-alliance.org/technical-specifications/rp002-1-0-4-regional-parameters) 
  guidelines. By default, the sample is set to connect to the US915 region

* To select a different region for the sample, go to the class A task `demos/classA/common/classa_task.c` 
  and update LORAWAN\_REGION with the appropriate region type. Example:

  ```c
  #define LORAWAN_REGION         ( LORAMAC_REGION_US915 )  
  ```

The list of enumerations for all regions can be found in the header file LoRaMac-node/src/mac/LoRaMac.h 


### Build and Run your code

* Connect your nrf52840-dk.
* In the SES Build Menu, select Build classa\_demo. Figure 8 below shows UART output in the IDE's debug 
  terminal
* In the SES Debug Menu, select Go. This will flash and run the demo in debug mode. There is a breakpoint 
  at the beginning of the program. When you are ready, you can continue execution.

[![](/media/2020/Figure-8.png)](/media/2020/Figure-8.png)   
*Figure 8 Segger IDE showing Build Complete  Click to enlarge.*


###  Join the device

* The device sends a Join request after initializing LoRaWAN stack. 

  [![](/media/2020/Figure-9.png)](/media/2020/Figure-9.png)   
  *Figure 9 TTN Console showing end-device Join Request  Click to enlarge.*

* The TTN console in Figure 10 shows a Join Accept is sent back from the LNS to the gateway, and then 
  to the end-device.

  [![](/media/2020/Figure-10.png)](/media/2020/Figure-10.png)   
  *Figure 10 TTN Console showing end-device Join Accept  Click to enlarge.*

* The end-device debug console in Figure 11 shows that the Join accept is received and the device completes 
  the Join process successfully. The end-device gets the `Device Address` which is then used for all uplink 
  and downlink communication. 

  [![](/media/2020/Figure-11.png)](/media/2020/Figure-11.png)   
  *Figure 11 Segger IDE showing Join procedure complete with Device Address assignment  Click to enlarge.*


### Send Uplink

LoRaWAN Class A communications allow a device to send uplink data at any time after a successful activation. 
However, devices that connect to a LoRaWAN network, should follow the duty cycle restrictions and fair access 
policy defined for a particular region. The policy limits the packet size or air time and the duty cycle allowed 
for transmission. Read more on duty cycle restrictions and the fair access 
policy [here](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle.html).

The Class A demo task for FreeRTOS sends a periodic uplink of 2 bytes for a configured interval based 
on the duty cycle intervals. Here is a screenshot of the packets sent by the device and received on TTN:


* As shown in Figure 12, device sends an uplink packet of 2 bytes `0xFEED` every TX-RX cycle. Packets 
  are sent as unconfirmed, which means ACK is not received for these packets. (Note: To change to confirmed 
  mode, set the following config in `demos/classA/common/classa_task.c`).

  ```c
  #define LORAWAN_CONFIRMED_SEND                 ( 1 )  
  ```

  [![](/media/2020/Figure-12.png)](/media/2020/Figure-12.png)   
  *Figure 12 Segger IDE showing successful device uplink  Click to enlarge.*

* The Figure 13 shows the packets received by the TTN console along with receive metadata such as gateway 
  RSSI, SNR. 

  [![](/media/2020/Figure-13.png)](/media/2020/Figure-13.png)   
  *Figure 13 TTN console showing end-device uplink along with receive metadata  Click to enlarge.*


### Receive Downlink

For LoRaWAN Class A communications, a device opens receive slots only after every uplink message. The 
downlink packets can be queued for a device from the TTN console. The LNS selects the gateway for the 
device and queues the packet for a gateway. The device receives the downlink packet after it has successfully 
sent the next uplink packet.

* To queue a downlink packet from TTN, Go to the Applications page, then click on your application. 
  Click on the registered devices tab and select the device to which you want to send the downlink packet 
  to. In the device page , under downlink tab, queue a payload for downlink as shown in Figure 14. (Figure 
  14 shows payload 2 bytes `0xC0DE` queued on `FPort 2` in unconfirmed-mode.)

  [![](/media/2020/Figure-14.png)](/media/2020/Figure-14.png)   
  *Figure 14 TTN console to schedule downlink  Click to enlarge.*

* In Class A mode of operation, TTN network server schedules the downlink data and sends it to the device 
  when it receives the next uplink packet from the device.

  [![](/media/2020/Figure-15.png)](/media/2020/Figure-15.png)
  *Figure 15 TTN console to schedule downlink  Click to enlarge.*

* The end-device receives the downlink data `0xC0DE` on `FPort 2` in one of the two receive windows after 
  the next uplink, as shown in the Figure 16:

  [![](/media/2020/Figure-16.png)](/media/2020/Figure-16.png)   
  *Figure 16 Segger IDE showing downlink received for end-device  Click to enlarge.*
