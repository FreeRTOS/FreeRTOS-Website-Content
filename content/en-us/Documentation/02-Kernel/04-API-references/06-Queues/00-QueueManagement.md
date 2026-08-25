---
title: Queue Management
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Modules

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


## Detailed Description

### uxQueueMessagesWaiting

queue.h 

```c
UBaseType_t uxQueueMessagesWaiting( QueueHandle_t xQueue );
```

Return the number of messages stored in a queue.


**Parameters:**

- *xQueue* 

  A handle to the queue being queried.


**Returns:**

- The number of messages available in the queue.

---


### uxQueueMessagesWaitingFromISR

queue.h 

```c
UBaseType_t uxQueueMessagesWaiting( QueueHandle_t xQueue );
```

A version of `uxQueueMessagesWaiting()` that can be called from an ISR. Return the number of messages stored in a queue.


**Parameters:**

- *xQueue* 

  A handle to the queue being queried.


**Returns:**

- The number of messages available in the queue.

---

### uxQueueSpacesAvailable

queue.h

```c
UBaseType_t uxQueueSpacesAvailable( QueueHandle_t xQueue );
```

Return the number of free spaces in a queue.

**Parameters:**

+ `xQueue`     

  A handle to the queue being queried.

**Returns:**

+ The number of free spaces available in the queue. 

---

### vQueueDelete

queue.h 

```c
void vQueueDelete( QueueHandle_t xQueue );
```

Delete a queue - freeing all the memory allocated for storing of items placed on the queue.

Do not delete a queue that has tasks blocked on it (tasks that are in the Blocked
state waiting to send to or read from the queue).


**Parameters:**

- *xQueue*

  A handle to the queue to be deleted.

---


### xQueueReset

queue.h 

```c
BaseType_t xQueueReset( QueueHandle_t xQueue );
```

Resets a queue to its original empty state. 


**Parameters:**

- *xQueue*

  The handle of the queue being reset.


**Returns:**

- Since FreeRTOS V7.2.0 `xQueueReset()` always returns pdPASS.

---


### xQueueIsQueueEmptyFromISR

queue.h 

```c
BaseType_t xQueueIsQueueEmptyFromISR( const QueueHandle_t pxQueue );
```

Queries a queue to determine if the queue is empty. This function should only be used in an ISR.


**Parameters:**

- *xQueue*

  The handle of the queue being queried 


**Returns:**

- pdFALSE if the queue is not empty, or 
- pdTRUE if the queue is empty.

---


### xQueueIsQueueFullFromISR

queue.h 

```c
BaseType_t xQueueIsQueueFullFromISR( const QueueHandle_t pxQueue );
```

Queries a queue to determine if the queue is full. This function should only be used in an ISR.


**Parameters:**

- *xQueue* 

  The handle of the queue being queried.


**Returns:**

- pdFALSE if the queue is not full, or 
- pdTRUE if the queue is full.

