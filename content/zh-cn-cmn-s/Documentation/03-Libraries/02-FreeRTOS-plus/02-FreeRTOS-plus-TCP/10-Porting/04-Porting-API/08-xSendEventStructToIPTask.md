---
title: xSendEventStructToIPTask()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[以太网驱动程序移植 API](../Network_interface_functions.md)]

FreeRTOS_IP_Private.h

```c
BaseType_t xSendEventStructToIPTask( const IPStackEvent_t *pxEvent, TickType_t xTimeout );
        
```

xSendEventStructToIPTask() 在整个嵌入式  TCP/IP 堆栈的
实现中被用于将各种事件发送至 RTOS 任务，
该任务正在运行嵌入式 TCP/IP 堆栈。该函数可供[网络端口层](../Embedded_Ethernet_Porting.md)使用，
以便网络端口层可以将接收事件发送到相同的 RTOS
任务。


**参数：** 

+ *pxEvent* 

  指向 IPStackEvent_t 类型的结构体的指针。

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
*IPStackEvent_t 类型*

+ *xTimeout* 

  无法立即发送消息时，等待发送消息的时间（以 RTOS tick 为单位），
  消息将发送至 RTOS 任务，
  该任务正在运行嵌入式 TCP/IP 堆栈。
  如果
  [网络事件队列已满](../TCP_IP_Configuration.md#ipconfigEVENT_QUEUE_LENGTH)，则可能无法立即发送消息。


**返回：** 

如果事件已成功发送至 RTOS 任务，
而该任务正在运行嵌入式 TCP/IP 堆栈，则返回 pdPASS。如果 xTimeout 大于
零，则调用任务可能已保持在阻塞状态（因此
不消耗任何 CPU 时间）以等待消息发送，但
在函数返回之前，消息已成功发送。

如果由于网络事件队列已满而无法向 RTOS 任务发送事件，
（该任务正在运行嵌入式 TCP/IP 堆栈），[](../TCP_IP_Configuration.md#ipconfigEVENT_QUEUE_LENGTH)
则返回 pdFAIL。如果 xTimeout 大于零，则
调用任务可能已保持在阻塞状态以等待
网络事件队列上的可用空间，但在那之前
阻塞时间已过期。


**用法示例：** 

在[“将 FreeRTOS 移植到不同的微控制器”](../Embedded_Ethernet_Porting.md)页面上提供了示例
。在该页面搜索 xSendEventStructToIPTask() 以查找示例
源代码。


