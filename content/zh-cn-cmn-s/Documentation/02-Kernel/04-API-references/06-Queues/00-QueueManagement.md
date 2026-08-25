---
title: 队列管理
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 模块

* [pcQueueGetName](/Documentation/02-Kernel/04-API-references/06-Queues/17-pcQueueGetName)
* [uxQueueMessagesWaiting](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement/#uxqueuemessageswaiting)
* [uxQueueMessagesWaitingFromISR](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement/#uxqueuemessageswaitingfromisr)
* [uxQueueSpacesAvailable](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement/#uxqueuespacesavailable)
* [vQueueAddToRegistry](/Documentation/02-Kernel/04-API-references/06-Queues/15-vQueueAddToRegistry)
* [vQueueDelete](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement/#vqueuedelete)
* [vQueueUnregisterQueue](/Documentation/02-Kernel/04-API-references/06-Queues/16-vQueueUnregisterQueue)
* [xQueueCreate](/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate/)
* [xQueueCreateStatic](/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic)
* [xQueueGetStaticBuffers](/Documentation/02-Kernel/04-API-references/06-Queues/18-xQueueGetStaticBuffers)
* [xQueueIsQueueEmptyFromISR](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement/#xqueueisqueueemptyfromisr)
* [xQueueIsQueueFullFromISR](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement/#xqueueisqueuefullfromisr)
* [xQueueOverwrite](/Documentation/02-Kernel/04-API-references/06-Queues/11-xQueueOverwrite)
* [xQueueOverwriteFromISR](/Documentation/02-Kernel/04-API-references/06-Queues/12-xQueueOverwriteFromISR)
* [xQueuePeek](/Documentation/02-Kernel/04-API-references/06-Queues/13-xQueuePeek)
* [xQueuePeekFromISR](/Documentation/02-Kernel/04-API-references/06-Queues/14-xQueuePeekFromISR)
* [xQueueReceive](/Documentation/02-Kernel/04-API-references/06-Queues/09-xQueueReceive)
* [xQueueReceiveFromISR](/Documentation/02-Kernel/04-API-references/06-Queues/10-xQueueReceiveFromISR)
* [xQueueReset](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement/#xqueuereset)
* [xQueueSend](/Documentation/02-Kernel/04-API-references/06-Queues/03-xQueueSend)
* [xQueueSendFromISR](/Documentation/02-Kernel/04-API-references/06-Queues/04-xQueueSendFromISR)
* [xQueueSendToBack](/Documentation/02-Kernel/04-API-references/06-Queues/05-xQueueSendToBack)
* [xQueueSendToBackFromISR](/Documentation/02-Kernel/04-API-references/06-Queues/06-xQueueSendToBackFromISR)
* [xQueueSendToFront](/Documentation/02-Kernel/04-API-references/06-Queues/07-xQueueSendToFront)
* [xQueueSendToFrontFromISR](/Documentation/02-Kernel/04-API-references/06-Queues/08-xQueueSendToFrontFromISR)



## 详细描述

### uxQueueMessagesWaiting

queue.h 

```c
UBaseType_t uxQueueMessagesWaiting( QueueHandle_t xQueue );
```

返回队列中存储的消息数。


**参数：**

- *xQueue* 

  正在查询的队列的句柄。


**返回：**

- 队列中可用的消息数。

---


### uxQueueMessagesWaitingFromISR

queue.h 

```c
UBaseType_t uxQueueMessagesWaiting( QueueHandle_t xQueue );
```

`uxQueueMessagesWaiting()` 的一个版本，可以从 ISR 中调用。返回队列中存储的消息数。


**参数：**

- *xQueue* 

  正在查询的队列的句柄。


**返回：**

- 队列中可用的消息数。

---

### uxQueueSpacesAvailable

queue.h

```c
UBaseType_t uxQueueSpacesAvailable( QueueHandle_t xQueue );
```

返回队列中的可用空间数。

**参数：**

+ `xQueue`     

  正在查询的队列的句柄。

**返回：**

+ 队列中可用的可用空间数。 

---

### vQueueDelete

queue.h 

```c
void vQueueDelete( QueueHandle_t xQueue );
```

删除队列 — 释放分配用于存储放置在队列中的项目的所有内存。


**参数：**

- *xQueue*

  要删除的队列的句柄。

---


### xQueueReset

queue.h 

```c
BaseType_t xQueueReset( QueueHandle_t xQueue );
```

将队列重置为其原始的空状态。 


**参数：**

- *xQueue*

  正在重置的队列的句柄。


**返回：**

- 因为 FreeRTOS V7.2.0 `xQueueReset()` 总是返回 pdPASS。

---


### xQueueIsQueueEmptyFromISR

queue.h 

```c
BaseType_t xQueueIsQueueEmptyFromISR( const QueueHandle_t pxQueue );
```

查询队列以确定队列是否为空。此函数只能用于 ISR。


**参数：**

- *xQueue*

  正在查询的队列的句柄 


**返回：**

- 如果队列不为空，则返回 pdFALSE； 
- 如果队列为空，则返回 pdTRUE。

---


### xQueueIsQueueFullFromISR

queue.h 

```c
BaseType_t xQueueIsQueueFullFromISR( const QueueHandle_t pxQueue );
```

查询队列以确定队列是否已满。此函数只能用于 ISR。


**参数：**

- *xQueue* 

  正在查询的队列的句柄。


**返回：**

- 如果队列未满，则返回 pdFALSE； 
- 如果队列已满，则返回 pdTRUE。

