---
title: 通过 UDP 输出 TCP 日志消息
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例](TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


[FreeRTOS_debug_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_debug_printf-and-freertos_debug_printf)
和 [FreeRTOS_printf()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfighas_printf-and-freertos_printf)
用于从 FreeRTOS-Plus-TCP TCP/IP 堆栈中输出日志消息，
并且可由应用程序编写者用于相同目的。UDP日志记录示例演示了如何将
FreeRTOS_debug_printf() 和
FreeRTOS_printf() 输出发送到 UDP 端口。

FreeRTOSConfig.h 中的以下设置可配置 UDP 日志记录
功能。

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

![使用
Cinetix*的 [UDPTerm](http://www.cinetix.de/interface/tiptrix/udpterm.htm)查看由免费 RTOS TCP/IP 堆栈*(/media/2018/udp_logging_output.jpg)   
]UDP日志输出生成的日志消息
