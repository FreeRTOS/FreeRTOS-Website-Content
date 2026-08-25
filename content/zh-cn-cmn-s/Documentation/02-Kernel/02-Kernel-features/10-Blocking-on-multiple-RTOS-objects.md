---
title: "阻塞多个 RTOS 对象"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 队列集功能简介与示例。
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---


### 队列集简介

[队列集](/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)是一项 FreeRTOS 功能，
可让 RTOS 任务在同时从多个队列和/或
信号量接收数据时进行阻塞（挂起）。队列和信号量被分成集合，之后任务并非对
单个队列或信号量进行阻塞，而是对集合进行阻塞。

**请注意：**虽然有时需要阻塞（挂起）多个队列
（当 FreeRTOS 与遗留代码的第三方集成时），但不受此类限制的设计
通常能以更有效的方式实现相同的功能，方法是使用
替代设计模式 
[（记录在此页面底部）](#队列集的替代使用方法)。


### 使用队列集

队列集的使用方式与 select() API 函数和相关函数类似，
后者是标准伯克利套接字网络 API 的一部分。

队列集可能包含队列和信号量，
合称队列集成员。能获得队列句柄或信号量句柄的 API 函数参数和返回值
使用 QueueSetMemberHandle_t 类型。
QueueHandle_t 和 SemaphoreHandle_t 类型的变量通常可以隐式
转换为 QueueSetMemberHandle_t 参数或返回值，而不会生成编译器
警告（通常不需要显式转换到 QueueSetMemberHandle_t 类型或
从该类型进行显式转换）。

+ **创建队列集**  

  使用队列集之前，必须使用 [xQueueCreateSet()](/Documentation/02-Kernel/04-API-references/07-Queue-sets/01-xQueueCreateSet) 
  API 函数创建队列集。创建后，QueueSetHandle_t 类型的变量会引用队列集。

+ **添加成员到队列集**  

  [xQueueAddToSet()](/Documentation/02-Kernel/04-API-references/07-Queue-sets/02-xQueueAddToSet) API 函数用于添加队列或信号量至队列集。

+ **队列集上的阻塞（挂起）**  

  [xQueueSelectFromSet()](/Documentation/02-Kernel/04-API-references/07-Queue-sets/04-xQueueSelectFromSet) API 函数用于测试队列集中是否有任何 
  成员准备好进行读取——成员为队列时读取指的是“接收”，
  成员为信号量时读取指的是“获得”。

  与使用 [xQueueReceive()](/Documentation/02-Kernel/04-API-references/06-Queues/09-xQueueReceive) 和 [xSemaphoreTake()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake) API 函数一样， 
  xQueueSelectFromSet() 允许调用任务选择性阻塞，直到队列集成员已为
  读取准备就绪为止。

  如果调用 xQueueSelectFromSet() 超时，则返回 NULL。否则 xQueueSelectFromSet() 将返回 
  准备好读取的队列集成员的句柄，帮助调用任务立即 
  调用 xQueueReceive() 或 xSemaphoreTake()（分别在队列句柄或信号量句柄上），同时 
  保证操作会成功。


### 源代码示例

[xQueueCreateSet()](/Documentation/02-Kernel/04-API-references/07-Queue-sets/01-xQueueCreateSet) API 函数文件页面包含一个源代码示例。

名为 QueueSet.c 的标准演示/测试文件（位于 FreeRTOS/Demo/Common/Minimal/ 目录 
（在 FreeRTOS 压缩文件下载主文件夹中））包含一个全面示例。


### 队列集的替代使用方法

除非出现具体集成问题，导致有必要阻塞多个队列，否则 
通常可以通过单个队列，以较少的代码、更小的 RAM、更短的运行时间 
实现相同的功能。FreeRTOS-Plus-UDP 实现简单说明 
如何完成此操作，相关描述请见以下部分。


#### UDP/IP 堆栈：问题定义

管理 FreeRTOS-Plus-UDP 堆栈的任务是事件驱动的。事件有多种
来源。有些事件没有与之关联的任何数据。有些事件有
与之关联的可变数据量。事件包括：

* 接收帧的以太网硬件。帧包含大量数据，而且数据数量可变。
* 完成帧传输、清空网络和 DMA 缓冲区的以太网硬件。
* 发送数据包的应用程序任务。数据包包含大量数据，而且数据数量可变。
* 各种软件定时器，包括 ARP 定时器。定时器事件与任何数据均无关联。


#### UDP/IP 堆栈：解决方案

UDP/IP 堆栈*可以*为每个事件源使用不同的队列，然后
使用队列集一次阻塞所有队列。相反，UDP/IP 堆栈会：

1. 定义一个结构体，该结构体的一个成员保存事件类型，另一个成员保存 
   与事件关联的数据（或数据的指针）。
2. 使用创建的单个队列来保存定义的结构体。每个事件源都会发布到 
   同一队列。

结构体定义如下所示。

```c
typedef struct IP_TASK_COMMANDS
{
    eIPEvent_t eEventType; /* Tells the receiving task what the event is. */
    void *pvData; /* Holds or points to any data associated with the event. */

} xIPStackEvent_t;
```

使用该结构体的示例：

* 当 ARP 定时器到期时，它会向队列发送一个事件，同时将 eEventType 设置为 eARPTimerEvent 
  （枚举类型)。ARP 定时器事件不与任何数据关联，因此并未设置 pvData。
* 当以太网驱动器接收帧时，它会向队列发送一个事件，同时将 eEventType 设置为 eEthernetRxEvent， 
  并将 pvData 设置为指向帧缓冲区。
* 等。

UDP/IP 任务使用简单循环处理事件：

```c
/* The variable used to receive from the queue. */
xIPStackEvent_t xReceivedEvent;

for( ;; )
{
    /* Wait until there is something to do. */
    xQueueReceive( xNetworkEventQueue, &xReceivedEvent, portMAX_DELAY );

    /* Perform a different action for each event type. */
    switch( xReceivedEvent.eEventType )
    {
        case eNetworkDownEvent :
            prvProcessNetworkDownEvent();
            break;

        case eEthernetRxEvent :
            prvProcessEthernetFrame( xReceivedEvent.pvData );
            break;

        case eARPTimerEvent :
            prvAgeARPCache();
            break;

        case eStackTxEvent :
            prvProcessGeneratedPacket( xReceivedEvent.pvData );
            break;

        case eDHCPEvent:
            vDHCPProcess();
            break;

        default :
            /* Should not get here. */
            break;
    }
}
```
