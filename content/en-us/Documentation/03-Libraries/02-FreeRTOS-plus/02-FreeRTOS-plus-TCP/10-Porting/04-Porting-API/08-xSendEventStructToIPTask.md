---
title: xSendEventStructToIPTask()
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Ethernet Driver Porting API](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/01-Network_interface_functions)]

FreeRTOS\_IP\_Private.h

```c
BaseType_t xSendEventStructToIPTask( const IPStackEvent_t *pxEvent, TickType_t xTimeout );
```

xSendEventStructToIPTask() is used throughout the embedded TCP/IP stack's
implementation to send various events to the RTOS task that is running the
embedded TCP/IP stack. The function is made available to the [network port layer](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)
so the network port layer can send receive events to the same RTOS
task.


**Parameters:**

+ *pxEvent*

  A pointer to a structure of type IPStackEvent\_t.

  ```c
  typedef struct IP_TASK_COMMANDS
  {
      /* Specifies the type of event being posted to the RTOS task. Must be set to
         eNetworkRxEvent to signify a receive event. */
      eIPEvent_t eEventType;

      /* Points to additional data about the event. Set pvData to the address
         of the network buffer descriptor that references the received frame. */
      void *pvData;
  } IPStackEvent_t;
  ```
  *The IPStackEvent\_t type*

+ *xTimeout*

  The time, specified in RTOS ticks, to wait for the message
  to be sent to the RTOS task that is running the embedded
  TCP/IP stack if the message cannot be sent immediately.
  The message might not be able to be sent immediately if
  the [network event queue is full](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigEVENT_QUEUE_LENGTH).


**Returns:**

If the event was successfully sent to the RTOS task that is running the
embedded TCP/IP stack then pdPASS is returned. If xTimeout is greater than
zero then the calling task may have been held in the Blocked state (so
not consuming any CPU time) to wait for the message to be sent - but the
message was sent successfully before the function returned.

If the event could not be sent to the RTOS task that is running the
embedded TCP/IP stack because the [network event queue](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigEVENT_QUEUE_LENGTH)
was full then pdFAIL is returned. If xTimeout is greater than zero then
the calling task may have been held in the Blocked state to wait for
space to become available on the network event queue, but the block time
expired before that happened.


**Example usage:**

Examples are provided on the [Porting FreeRTOS to a Different Microcontroller](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)
page. Search for xSendEventStructToIPTask() on that page to find example
source code.
