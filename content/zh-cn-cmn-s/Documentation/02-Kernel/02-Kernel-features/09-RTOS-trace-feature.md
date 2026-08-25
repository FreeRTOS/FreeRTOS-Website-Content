---
title: 跟踪钩子宏
created: 2018-09-20
categories:
- 内核
说明: 跟踪钩子宏功能的信息和示例。
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: null
- title: 什么是 FreeRTOS
  link: null
- title: FreeRTOS 初学者指南
  link: null
- title: 下载 FreeRTOS
  link: null
- title: 常见问题
  link: null
---


[还提供：**FreeRTOS-Plus-Trace**，一款专用于 FreeRTOS 的第三方跟踪工具——FreeRTOS-Plus 生态系统的一部分](FreeRTOS-Plus/FreeRTOS_Plus_Trace/FreeRTOS_Plus_Trace.md)


### 描述

跟踪钩子宏是一个非常强大的功能，允许您收集有关嵌入式应用程序行为的数据。

FreeRTOS 源代码中的关键关注点包含空宏，
应用程序可以重新定义这些宏，以便提供特定于应用程序的跟踪工具。应用程序只需要实现特别关注的宏，未使用的宏将保留为空，
因此不会影响应用程序的定时。


### 示例

以下是此类宏的一些使用示例：

* 设置数字输出以指示正在执行的任务， 
  并允许使用逻辑分析器查看和记录任务执行序列和定时。
* 类似地，将模拟输出设置为表示正在执行的任务的电压， 
  并允许使用示波器查看和记录任务执行序列和定时。
* 记录任务执行序列、任务定时、RTOS 内核事件和 API 调用以进行离线分析。
* 将 RTOS 内核事件集成到第三方调试器中。


#### 示例 1

FreeRTOS 任务标签功能提供了一种通过数字或模拟输出设置日志记录的简单机制。例如，
标签值可以设置为该任务唯一的电压。
然后可以定义 traceSWITCHED_IN() 宏来简单地将模拟输出设置为与被切换的任务相关联的值 
。例如：

```c
 /* First task sets its tag value to 1. */
void vTask1( void \*pvParameters )
{
 /\* This task is going to be represented by a voltage scale of 1. */
 vTaskSetApplicationTaskTag( NULL, ( void * ) 1 );

 for( ;; )
 {
 /* Task code goes here. */
 }
}
/*************************************************/

/* Second task sets its tag value to 2. */
void vTask2( void \*pvParameters )
{
 /\* This task is going to be represented by a voltage scale of 2. */
 vTaskSetApplicationTaskTag( NULL, ( void * ) 2 );

 for( ;; )
 {
 /* Task code goes here. */
 }
}
/*************************************************/

/* Define the traceTASK_SWITCHED_IN() macro to output the voltage associated
   with the task being selected to run on port 0. */
#define traceTASK_SWITCHED_IN() vSetAnalogueOutput( 0, (int)pxCurrentTCB->pxTaskTag )
```


#### 示例 2

API 调用日志记录可用于记录发生上下文切换的原因。RTOS 内核调用日志记录 
可用于记录任务执行的顺序。例如：

```c
/* traceBLOCKING_ON_QUEUE_RECEIVE() is just one of the macros that can be used to
record why a context switch is about to occur. */
#define traceBLOCKING_ON_QUEUE_RECEIVE(xQueue) 
 ulSwitchReason = reasonBLOCKING_ON_QUEUE_READ;

/* log_event() is an application defined function that logs which tasks ran when,
   and why. */
#define traceTASK_SWITCHED_OUT() 
 log_event( pxCurrentTCB, ulSwitchReason );
```


### 定义

从中断（特别是 tick 中断）调用的宏必须快速执行， 
并且不能占用过多堆栈空间。设置变量、写入跟踪寄存器或输出到端口等操作都是允许的 
。任何试图将 fprintf() 日志数据保存到速度较慢的磁盘的操作都是无效操作！

宏定义必须在加入 FreeRTOS.h 之前进行。定义跟踪宏的最简单位置是 
在 FreeRTOSConfig.h 底部，或者在从底部包含的单独头文件中 
FreeRTOSConfig.h。

下表描述了可用的宏。宏参数用于指示与所记录的事件相关联的 
任务、队列、 信号量或互斥锁。

| **宏定义** | **描述** | **源文件** |
| --- | --- | --- |
| traceBLOCKING_ON_QUEUE_PEEK( pxQueue ) | 在阻塞试图偷看空队列的任务之前，从 xQueuePeek() 中调用的宏。 | queue.c |
| traceBLOCKING_ON_QUEUE_RECEIVE(xQueue) |  表示当前执行的任务在尝试从空队列读取或尝试‘获取’空信号量或互斥锁后即将阻塞的宏。  | queue.c |
| traceBLOCKING_ON_QUEUE_SEND(xQueue) |  指示当前执行的任务在尝试写入已满队列后即将阻塞。  | queue.c |
| traceBLOCKING_ON_STREAM_BUFFER_RECEIVE( xStreamBuffer ) | 当流缓冲区满了，并且指定了一个阻塞时间时，从 xStreamBufferReceive() 中调用。 | stream_buffer.c |
| traceBLOCKING_ON_STREAM_BUFFER_SEND( xStreamBuffer ) | 当流缓冲区满了，并且指定了一个阻塞时间时，从 xStreamBufferSend() 中调用。 | stream_buffer.c |
| traceCREATE_COUNTING_SEMAPHORE() | 信号量成功创建后，从 xSemaphoreCreateCounting() 中调用的宏。 | queue.c |
| traceCREATE_COUNTING_SEMAPHORE_FAILED() | 可用堆内存不足而导致信号量创建失败时，从 xSemaphoreCreateCounting() 中调用的宏。 | queue.c |
| traceCREATE_MUTEX(pxNewMutex) | 互斥锁创建成功后，从 xSemaphoreCreateMutex() 中调用的宏。 | queue.c |
| traceCREATE_MUTEX_FAILED() | 由于可用堆内存不足而导致互斥锁创建失败时，从 xSemaphoreCreateMutex() 中调用的宏。 | queue.c |
| traceEVENT_GROUP_CLEAR_BITS( xEventGroup, uxBitsToClear ) |  在清除所选事件位并返回先前值之前，在xEventGroupClearBits ()内调用。  | event_groups.c |
| traceEVENT_GROUP_CLEAR_BITS_FROM_ISR( xEventGroup, uxBitsToClear ) | 从 xEventGroupClearBitsFromISR() before calling xEventGroupClearBits() | event_groups.c |
| traceEVENT_GROUP_CREATE( xEventGroup ) 中调用的宏。 | 当成功分配一个事件组时，从 xEventGroupCreate() 中调用的宏。 | event_groups.c |
| traceEVENT_GROUP_CREATE_FAILED() | 当无法分配一个事件组时，从 xEventGroupCreate() 中调用的宏。 | event_groups.c |
| traceEVENT_GROUP_DELETE( xEventGroup ) | 在试图删除一个事件组之前，从 vEventGroupDelete() 中调用的宏。 | event_groups.c |
| traceEVENT_GROUP_SET_BITS( xEventGroup, uxBitsToSet ) | 在提高选定的事件位和可能解除阻塞的任务之前，从 xEventGroupSetBits() 中调用的宏。 | event_groups.c |
| traceEVENT_GROUP_SET_BITS_FROM_ISR( xEventGroup, uxBitsToSet ) | 在调用 xEventGroupSetBitsFromISR() 之前，从 xEventGroupSetBits() 中调用的宏。 | event_groups.c |
| traceEVENT_GROUP_SYNC_BLOCK( xEventGroup, uxBitsToSet, uxBitsToWaitFor ) | 在阻塞前从 xEventGroupSync() 中调用，以等待指定阻塞时间后的 rendevous 位被设置的宏。 | event_groups.c |
| traceEVENT_GROUP_WAIT_BITS_BLOCK( xEventGroup, uxBitsToWaitFor ) | 在阻塞前从 xEventGroupWaitBits() 中调用，以等待所需的事件位被设置的宏。 | event_groups.c |
| traceFREE( pvAddress, uiSize ) | 释放内存时，从 vPortFree() 中调用的宏。 | heap_#.c |
| traceGIVE_MUTEX_RECURSIVE(xMutex) | 互斥锁成功“给出”后，从 xSemaphoreGiveRecursive() 中调用的宏。 | queue.c |
| traceGIVE_MUTEX_RECURSIVE_FAILED(xMutex) | 由于调用任务不是互斥锁拥有者而导致互斥锁“给出”失败时，从 xSemaphoreGiveRecursive() 内部调用的宏。 | queue.c |
| traceINCREASE_TICK_COUNT( xTicksToJump ) | 在跳过滴答计数后，从 vTaskStepTick() 中调用的宏。 | tasks.c |
| traceLOW_POWER_IDLE_BEGIN() | 在处理器空闲之前，从 portTASK_FUNCTION() 中调用的宏。 | tasks.c |
| traceLOW_POWER_IDLE_END() | 从空闲状态唤醒后在 portTASK_FUNCTION() 中调用的宏。 | tasks.c |
| traceMALLOC( pvAddress, uiSize ) | 分配内存时，从 pvPortMalloc() 中调用的宏。 | heap_#.c |
| traceMOVED_TASK_TO_READY_STATE(xTask) |  在任务转换为“就绪”状态时调用的宏。  | tasks.c |
| tracePEND_FUNC_CALL( xFunctionToPend, pvParameter1, ulParameter2, ret ) | 在将挂起函数发布到队列后，从 xTimerPendFunctionCall() 中调用的宏。 | timers.c |
| tracePEND_FUNC_CALL_FROM_ISR( xFunctionToPend, pvParameter1, ulParameter2, ret ) | 在将挂起函数发布到队列后，从 xTimerPendFunctionCallFromISR() 中调用的宏。 | timers.c |
| tracePOST_MOVED_TASK_TO_READY_STATE( pxTCB ) | 在任务成功转移到就绪列表的末尾后，从 prvAddTaskToReadyList() 宏中调用的宏。 | tasks.c |
| traceQUEUE_CREATE(pxNewQueue) |  队列创建成功后，从 xQueueCreate() 或 xQueueCreateStatic() 中调用的宏。  | queue.c |
| traceQUEUE_CREATE_FAILED() | 由于可用堆内存不足而导致队列创建失败时，从 xQueueCreate() 或 xQueueCreateStatic() 中调用的宏。 | queue.c |
| traceQUEUE_DELETE(xQueue) | 从 vQueueDelete() 中调用的宏。 | queue.c |
| traceQUEUE_PEEK(xQueue) | 从 xQueuePeek() | queue.c |
| traceQUEUE_PEEK_FAILED( pxQueue ) 中调用的宏。 | 当队列在等待后仍为空时或没有指定等待时，从 xQueuePeek() 中调用的宏。 | queue.c |
| traceQUEUE_PEEK_FROM_ISR( pxQueue ) | 在一个项目从队列中弹出之前，从 xQueuePeekFromISR() 中调用的宏。 | queue.c |
| traceQUEUE_PEEK_FROM_ISR_FAILED( pxQueue ) | 当队列为空时，从 xQueuePeekFromISR() 中调用的宏。 | queue.c |
| traceQUEUE_REGISTRY_ADD( xQueue, pcQueueName ) | 在成功添加队列到注册表后，从 vQueueAddToRegistry() 中调用的宏。 | queue.c |
| traceQUEUE_RECEIVE(xQueue) |  队列接收成功后，从 xQueueReceive() 或任何信号量“获取”函数中调用的宏。  | queue.c |
| traceQUEUE_RECEIVE_FAILED(xQueue) |  由于队列为空而导致队列接收操作失败时（在指定的任何块时间之后），xQueueReceive() 或任何信号量“获取”函数中调用的宏。  | queue.c |
| traceQUEUE_RECEIVE_FROM_ISR(xQueue) |  接收操作成功时从 xQueueReceiveFromISR() 中调用的宏。  | queue.c |
| traceQUEUE_RECEIVE_FROM_ISR_FAILED(xQueue) |  由于队列为空而导致接收操作失败时，从 xQueueReceiveFromISR() 中调用的宏。  | queue.c |
| traceQUEUE_SEND(xQueue) |  队列发送成功后，从 xQueueSend()、xQueueSendToFront()、xQueueSendToBack() 或任何信号量“给出”函数中调用的宏。  | queue.c |
| traceQUEUE_SEND_FAILED(xQueue) |  由于队列已满而导致队列发送操作失败时（在指定的任何块时间之后），从 xQueueSend()、xQueueSendToFront()、xQueueSendToBack() 或任何信号量“给出”函数中调用的宏。  | queue.c |
| traceQUEUE_SEND_FROM_ISR(xQueue) | 发送操作成功时从 xQueueSendFromISR() 中调用的宏。 | queue.c |
| traceQUEUE_SEND_FROM_ISR_FAILED(xQueue) |  由于队列为空而导致发送操作失败时，从 xQueueSendFromISR() 中调用的宏。  | queue.c |
| traceTAKE_MUTEX_RECURSIVE(xMutex) | 从 xQueueTakeMutexRecursive() 中调用的宏。 | queue.c |
| traceTAKE_MUTEX_RECURSIVE_FAILED(xMutex) | 当调用的任务不保存递归互斥锁，并且无法获取递归互斥锁时，从 xQueueTakeMutexRecursive() 中调用的宏。 | queue.c |
| traceTASK_CREATE(xTask) | 任务创建成功时，从 xTaskCreate() （或 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)）中调用的宏。 | tasks.c |
| traceTASK_CREATE_FAILED(pxNewTCB) | 由于可用堆空间不足而导致任务创建失败时，从 xTaskCreate()（或 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)）中调用的宏。 | tasks.c |
| traceTASK_DELAY() | 从 vTaskDelay() 中调用的宏。 | tasks.c |
| traceTASK_DELAY_UNTIL() | 从 vTaskDelayUntil() 中调用的宏。 | tasks.c |
| traceTASK_DELETE(xTask) | 从 vTaskDelete() 中调用的宏。 | tasks.c |
| traceTASK_INCREMENT_TICK(xTickCount) | 在 tick 中断期间调用的宏。 | tasks.c |
| traceTASK_NOTIFY( uxIndexToNotify ) | 当通知一个任务关于一个通知值时，从 xTaskGenericNotify() 中调用的宏。 | tasks.c |
| traceTASK_NOTIFY_FROM_ISR( uxIndexToNotify ) | 在从 ISR 通知一个任务的通知值之前，从 xTaskGenericNotifyFromISR() 中调用的宏。 | tasks.c |
| traceTASK_NOTIFY_GIVE_FROM_ISR( uxIndexToNotify ) | 在从 ISR 通知一个任务的递增通知值之前，从 vTaskGenericNotifyGiveFromISR() 中调用的宏。 | tasks.c |
| traceTASK_NOTIFY_TAKE( uxIndexToWait ) | 在读取和递减通知值时从 ulTaskGenericNotifyTake() 中调用的宏。如果值仍然为零，则保持不变。  | tasks.c |
| traceTASK_NOTIFY_TAKE_BLOCK( uxIndexToWait ) | 当任务被阻塞并等待通知值变为非零时，从 ulTaskGenericNotifyTake() 中调用的宏。 | tasks.c |
| traceTASK_NOTIFY_WAIT( uxIndexToWait ) | 在读取和返回通知值时从 xTaskGenericNotifyWait() 中调用的宏。该值可能不变。  | tasks.c |
| traceTASK_NOTIFY_WAIT_BLOCK( uxIndexToWait ) | 当任务被阻塞并等待通知值时，从 xTaskGenericNotifyWait() 中调用的宏。 | tasks.c |
| traceTASK_PRIORITY_DISINHERIT( pxTCBOfMutexHolder, uxOriginalPriority ) | 在降低一个已经解除互斥锁阻塞的任务的优先级之前，从 xTaskPriorityDisinherit() 中调用的宏。 | tasks.c |
| traceTASK_PRIORITY_INHERIT( pxTCBOfMutexHolder, uxInheritedPriority ) | 在提高保存被高优先级任务等待的互斥锁的任务的优先级后，从 xTaskPriorityInherit() 中调用的宏。 | tasks.c |
| traceTASK_PRIORITY_SET(xTask,uxNewPriority) | 从 vTaskPrioritySet() 中调用的宏。 | tasks.c |
| traceTASK_RESUME(xTask) | 从 vTaskResume() 中调用的宏。 | tasks.c |
| traceTASK_RESUME_FROM_ISR(xTask) | 从 xTaskResumeFromISR() 中调用的宏。 | tasks.c |
| traceTASK_SUSPEND(xTask) | 从 vTaskSuspend() 中调用的宏。 | tasks.c |
| traceTASK_SWITCHED_IN() |  在选择要运行的任务之后调用的宏。此时，pxCurrentTCB 包含即将进入运行状态的任务句柄。  | tasks.c |
| traceTASK_SWITCHED_OUT() |  在选择要运行的新任务之前调用的宏。此时，pxCurrentTCB 包含即将离开运行状态的任务句柄。  | tasks.c |
| traceTIMER_COMMAND_RECEIVED(pxTimer, xCommandID, xCommandValue) |  每次定时器服务任务接收到命令后，实际处理该命令之前从该定时器服务任务中调用的宏。  | timers.c |
| traceTIMER_COMMAND_SEND(pxTimer, xCommandID, xOptionalValue, xStatus) |  从向定时器服务任务发送命令的任何 API 函数（例如 xTimerReset()、xTimerStop() 等）中调用的宏。如果命令未成功发送到定时器命令队列，则 xStatus 将为 pdFAIL。  | timers.c |
| traceTIMER_CREATE(pxNewTimer) |  定时器创建时从 xTimerCreate() 中调用的宏。  | timers.c |
| traceTIMER_CREATE_FAILED() |  由于可用堆内存不足而导致定时器创建失败时，从 xTimerCreate() 中调用的宏。  | timers.c |
| traceTIMER_EXPIRED(pxTimer) |  在软件定时器到期，执行定时器回调之前调用的宏。  | timers.c |
| traceSTREAM_BUFFER_CREATE( xIsMessageBuffer ) | 在成功分配和初始化一个新的流缓冲区后，从 xStreamBufferGenericCreate() 中调用的宏。 | stream_buffer.c |
| traceSTREAM_BUFFER_CREATE_FAILED( xIsMessageBuffer ) | 当无法分配一个新的流缓冲区时，从 xStreamBufferGenericCreate() 中调用的宏。 | stream_buffer.c |
| traceSTREAM_BUFFER_CREATE_STATIC_FAILED( xReturn, xIsMessageBuffer ) | 当未能指定流句柄或存储区域的位置时，从 xStreamBufferGenericCreateStatic() 中调用的宏。  | stream_buffer.c |
| traceSTREAM_BUFFER_DELETE( xStreamBuffer ) | 在尝试删除流缓冲区之前，从 vStreamBufferDelete() 中调用的宏。 | stream_buffer.c |
| traceSTREAM_BUFFER_RECEIVE( xStreamBuffer, xReceivedLength ) | 当成功收到任何字节时，从 xStreamBufferReceive() 中调用的宏。 | stream_buffer.c |
| traceSTREAM_BUFFER_RECEIVE_FAILED( xStreamBuffer ) | 当没有收到字节时，从 xStreamBufferReceive() 中调用的宏。 | stream_buffer.c |
| traceSTREAM_BUFFER_RECEIVE_FROM_ISR( xStreamBuffer, xReceivedLength ) | 在处理完接收请求后，从 xStreamBufferReceiveFromISR() 中调用的宏。 | stream_buffer.c |
| traceSTREAM_BUFFER_RESET( xStreamBuffer ) | 在成功重置流缓冲区后，从 xStreamBufferReset() 中调用的宏。 | stream_buffer.c |
| traceSTREAM_BUFFER_SEND( xStreamBuffer, xBytesSent ) | 当任何字节被成功发送时，在通知任何在流缓冲区上等待的任务之前，从 xStreamBufferSend() 中调用的宏。 | stream_buffer.c |
| traceSTREAM_BUFFER_SEND_FAILED( xStreamBuffer ) | 当没有发送字节时，从 xStreamBufferSend() 中调用的宏。 | stream_buffer.c |
| traceSTREAM_BUFFER_SEND_FROM_ISR( xStreamBuffer, xBytesSent ) | 在处理完发送请求后，从 xStreamBufferSendFromISR() 中调用的宏。 | stream_buffer.c |

