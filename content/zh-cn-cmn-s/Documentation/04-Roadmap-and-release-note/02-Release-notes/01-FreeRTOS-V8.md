---
title: 从 FreeRTOS V7.x.x 升级到 FreeRTOS V8.x.x
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### FreeRTOS V8 向后兼容 FreeRTOS V7

FreeRTOS V8.x.x 是 FreeRTOS V7.x 的直接兼容替代品，
尽管如果更改用于引用字符串的类型，可能会在升级后导致应用程序
代码生成一些易于清除的编译器警告，
而且更新后的 typedef 命名规范表明目前不推荐使用旧的 typedef
名称（请参阅 config [configENABLE_BACKWARD_COMPATIBILITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configenable_backward_compatibility)）。


### FreeRTOS V8 中的新特性和更新

* [直达任务通知简介（V8.2.0 版）](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [事件组简介](#事件组或事件标志简介)
* [集中延迟中断处理](#集中延迟中断处理)
* [使用 stdint.h](#使用-stdinth)
* [字符指针](#字符指针)
* [跟踪和可视化](#跟踪和可视化)
* 由新 FreeRTOS 定义的 typedef 名称


#### 事件组（或事件*标志*）简介

FreeRTOS V8 包含一个全新的功能——事件组。事件组实现包含于
名为 event_groups.c 的新源文件中。与现有 timers.c 源文件一样，event_groups.c
是可选的，只有在应用程序使用事件组时才需要将其包含到项目中。

阅读更多：

* [关于事件组](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)
* [事件组 API](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)


#### 集中延迟中断处理

理想情况下，中断服务程序 (ISR) 需尽可能短，但有时 ISR 需要执行
大量的处理，或需要执行非确定性的处理。按照传统做法，这种情况下，
通常会利用信号量将高优先级应用程序任务从中断中解除阻塞，
将实际处理延迟到应用程序任务（所谓的延迟中断处理）。 FreeRTOS
允许中断直接返回未阻塞的任务，以确保立即执行处理。

FreeRTOS V8 提供了集中延迟中断处理机制——允许
在 RTOS 守护进程任务（正式称为定时器守护进程任务）中执行延迟的处理，消除了
用户实现延迟中断机制的负担。

阅读更多：

* [xTimerPendFunctionCallFromISR() API 文档](/Documentation/02-Kernel/04-API-references/11-Software-timers/18-xTimerPendFunctionCallFromISR)


#### 使用 stdint.h

除下述字符指针外，所有标准 C 类型均替换为
stdint.h 头文件中的等效 typedef。  例如，unsigned long 已替换为 uint32_t，short
已替换为 int16_t, etc。


#### 字符指针

字符指针用于引用文本字符串，例如分配给任务的名称。

以前，根据良好软件工程实践的要求，FreeRTOS 编码标准不
允许使用未明确限定为有符号或无符号的字符类型。因此，
用于引用字符串的字符指针需要进行强制转换，使用任何标准字符串处理函数时也应如此
。转换确保编译器不会生成编译器警告。这些编译器将非限定的
字符类型默认为有符号或无符号。

根据后来的 MISRA 标准的规定，此规则已经放宽了，现在允许使用非限定的字符类型，
仅限于以下情况：

* 字符用于指向人类可读文本字符串。
* 字符用于保存单个 ASCII 字符。


#### 跟踪和可视化

目前，跟踪功能已增强，涵盖了堆使用和新的事件组功能。

**注意：**
FreeRTOS v8.0.0 需要 [FreeRTOS-Plus-Trace](/Documentation/03-Libraries/02-FreeRTOS-plus/05-FreeRTOS_plus_Trace/00-FreeRTOS_Plus_Trace) 版本 2.6 或更高版本。


#### 由新 FreeRTOS 定义的 typedef 名称

为了确保与新近推出的 FreeRTOS-Plus 软件组件保持一致，要与 stdint.h 定义的 typedef
保持一致，并满足多项用户请求。核心
FreeRTOS 代码中分配给 typedef 的名称按照下表进行了更改。现在所有 typedefed 类型都以 '_t' 结尾。

**注意：**为了确保向后兼容，代码中保留了旧名称，但我们非常
不建议使用旧名称（请参阅
config [configENABLE_BACKWARD_COMPATIBILITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configenable_backward_compatibility)）。


|  旧名称  |  新名称  |  说明  |
| --- | --- | --- |
|  xTaskHandle  |  TaskHandle_t  |  用于引用任务。  |
|  xQueueHandle  |  QueueHandle_t  |  用于引用队列。  |
|  xSemaphoreHandle  |  SemaphoreHandle_t  |  用于引用二进制信号量、计数信号量、递归信号量和互斥型信号量。  |
|  xTimerHandle  |  TimerHandle_t  |  用于引用软件定时器。  |
|  xCoRoutineHandle  |  CoRoutineHandle_t  |  用于引用协程。  |
|  portTickType  |  TickType_t  |  用于保存 tick 计数值。  |
|  portBASE_TYPE  |  BaseType_t  |  定义为架构的最有效的有符号类型。  |
|  无符号的 portBASE_TYPE  |  UBaseType_t  |  定义为架构的最有效的无符号类型。  |
|  xQueueSetHandle  |  QueueSetHandle_t  |  用于引用[队列集](/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)。  |
|  xQueueSetMemberHandle  |  QueueSetMemberHandle_t  |  用于引用队列集的成员，该成员可以是队列或任何信号量类型。  |
|  xMemoryRegion  |  MemoryRegion_t  |  与支持内存保护的端口一起使用。  |
|  xTaskParameters  |  TaskParameters_t  |  与支持内存保护的端口一起使用。  |
|  xTaskStatusType  |  TaskStatus_t  |  与 [uxTaskGetSystemState()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState) 函数一起使用。  |
|  pdTASK_HOOK_CODE  |  TaskHookFunction_t  |  与任务标签函数一起使用（例如 [vTaskSetApplicationTag()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/06-vTaskSetApplicationTag)）  |
|  pdTASK_CODE  |  TaskFunction_t  |  与 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 函数一起使用。  |
|  tmrTIMER_CALLBACK  |  TimerCallbackFunction_t  |  与 [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/) 函数一起使用。  |
|  xTimeOutType  |  TimeOut_t  |  仅适用于高级用户。  |
