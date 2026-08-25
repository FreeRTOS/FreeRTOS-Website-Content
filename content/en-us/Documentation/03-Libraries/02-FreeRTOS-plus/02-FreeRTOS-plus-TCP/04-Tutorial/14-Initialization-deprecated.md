---
title: Initialising the TCP/IP Stack
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

**NOTE: These stack initialisation APIs have been deprecated as of FreeRTOS V4.0.0 onwards. Please refer 
to Initialising the TCP/IP Stack for the new APIs supporting IPv6, Multiple Endpoints and Multiple interfaces. 
To use the deprecated APIs please set ipconfigIPv4_BACKWARD_COMPATIBLE to 1 in the FreeRTOSIPConfig.h header 
file.**


This page describes [FreeRTOS\_IPInit()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit)
and the [callback function](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/57-vApplicationIPNetworkEventHook) that
gets invoked when 'network up' and 'network down' events occur.

[FreeRTOS\_IPInit()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit)
must be the first FreeRTOS-Plus-TCP function called. FreeRTOS\_IPInit() can be called
before or after the RTOS scheduler is started.

FreeRTOS\_IPInit() creates the FreeRTOS-Plus-TCP RTOS task. The FreeRTOS-Plus-TCP task
configures and initialises the network interface. If ipconfigUSE\_NETWORK\_EVENT\_HOOK is
set to 1 in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
then the TCP/IP stack will call the [vIPNetworkEventHook()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/57-vApplicationIPNetworkEventHook)
callback function when the network is ready for use.

Two examples are provided below. The first demonstrates FreeRTOS\_IPInit().
The second demonstrates vIPNetworkEventHook().

```c
/* The MAC address array is not declared const as the MAC address will
   normally be read from an EEPROM and not hard coded (in real deployed
   applications).*/
static uint8_t ucMACAddress[ 6 ] = { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55 };

/* Define the network addressing. These parameters will be used if either
   ipconfigUDE_DHCP is 0 or if ipconfigUSE_DHCP is 1 but DHCP auto configuration
   failed. */
static const uint8_t ucIPAddress[ 4 ] = { 10, 10, 10, 200 };
static const uint8_t ucNetMask[ 4 ] = { 255, 0, 0, 0 };
static const uint8_t ucGatewayAddress[ 4 ] = { 10, 10, 10, 1 };

/* The following is the address of an OpenDNS server. */
static const uint8_t ucDNSServerAddress[ 4 ] = { 208, 67, 222, 222 };

int main( void )
{
    /* Initialise the RTOS's TCP/IP stack. The tasks that use the network
       are created in the vApplicationIPNetworkEventHook() hook function
       below. The hook function is called when the network connects. */
    FreeRTOS_IPInit( ucIPAddress,
                     ucNetMask,
                     ucGatewayAddress,
                     ucDNSServerAddress,
                     ucMACAddress );

    /*
     * Other RTOS tasks can be created here.
     */

    /* Start the RTOS scheduler. */
    vTaskStartScheduler();

    /* If all is well, the scheduler will now be running, and the following
       line will never be reached. If the following line does execute, then
       there was insufficient FreeRTOS heap memory available for the idle and/or
       timer tasks to be created. */
    for( ;; );
}
```
*Example use of the FreeRTOS_IPInit() API function*


```c
void vApplicationIPNetworkEventHook( eIPCallbackEvent_t eNetworkEvent )
{
static BaseType_t xTasksAlreadyCreated = pdFALSE;

    /* Both eNetworkUp and eNetworkDown events can be processed here. */
    if( eNetworkEvent == eNetworkUp )
    {
        /* Create the tasks that use the TCP/IP stack if they have not already
           been created. */
        if( xTasksAlreadyCreated == pdFALSE )
        {
            /*
             * For convenience, tasks that use FreeRTOS-Plus-TCP can be created here
             * to ensure they are not created before the network is usable.
             */

            xTasksAlreadyCreated = pdTRUE;
        }
    }
}
```
*Example vApplicationIPNetworkEventHook() definition*

[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
