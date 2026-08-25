---
title: Outputting TCP Log Messages via UDP
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[FreeRTOS-Plus-TCP and FreeRTOS-Plus-FAT Examples](TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


[FreeRTOS\_debug\_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_debug_printf-and-freertos_debug_printf)
and [FreeRTOS\_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_printf-and-freertos_printf) are
used to output log messages from within the FreeRTOS-Plus-TCP TCP/IP stack, and
can be used by the application writer for the same purpose. The UDP
logging example demonstrates how to send FreeRTOS\_debug\_printf() and
FreeRTOS\_printf() output to a UDP port.

The following settings in FreeRTOSConfig.h configure the UDP logging
functionality.

```c
/* If set to 1 then each message sent via the UDP logging facility will end
   with rn. If set to 0 then each message sent via the UDP logging facility will
   end with n. */

 #define configUDP_LOGGING_NEEDS_CR_LF ( 1 )
 
/* Sets the maximum length for a string sent via the UDP logging facility. */
 #define configUDP_LOGGING_STRING_LENGTH ( 200 )
 
/* The UDP logging facility buffers messages until the UDP logging task is able
   to transmit them. configUDP_LOGGING_MAX_MESSAGES_IN_BUFFER sets the maximum
   number of messages that can be buffered at any one time. */
 #define configUDP_LOGGING_MAX_MESSAGES_IN_BUFFER ( 20 )
 
/* The UDP logging facility creates a task to send buffered messages to the UDP
   port. configUDP_LOGGING_TASK_STACK_SIZE sets the task's stack size. */
 #define configUDP_LOGGING_TASK_STACK_SIZE ( 512 )
 
/* The UDP logging facility creates a task to send buffered messages to the UDP
   port. configUDP_LOGGING_TASK_PRIORITY sets the task's priority. It is
   suggested to give the task a low priority to ensure it does not adversely effect
   the performance of other TCP/IP stack activity. */
 #define configUDP_LOGGING_TASK_PRIORITY ( tskIDLE_PRIORITY + 2 )
   
 /* The UDP port numbers to use. */
 #define configUDP_LOGGING_PORT_LOCAL 1499
 #define configUDP_LOGGING_PORT_REMOTE 1500
 
/* The IP address to which the UDP messages are sent.
   NOTE: If these settings are omitted then the UDP messages will be sent to
   the local broadcast address, although broadcast messages can be blocked by switches
   and routers. */
 #define configUDP_LOGGING_ADDR0 192
 #define configUDP_LOGGING_ADDR1 168
 #define configUDP_LOGGING_ADDR2 0
 #define configUDP_LOGGING_ADDR3 3
```

![Logging messages produced by the free RTOS TCP/IP stack](/media/2018/udp_logging_output.jpg)   
*UDP logging output viewed using [UDPTerm](http://www.cinetix.de/interface/tiptrix/udpterm.htm),
from Cinetix*
