---
title: "FreeRTOS 堆栈使用和堆栈溢出检查"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 堆栈使用和堆栈溢出检查
relatedLinks:
  - title: API 引用 - uxTaskGetStackHighWaterMark
    link: /Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation/
  - title: API 引用 - xTaskCreate
    link: /Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate/
  - title: FreeRTOS 堆
    link: /Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management/
---

### 堆栈使用

[另请参阅[uxTaskGetStackHighWaterMark()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark) API 函数]

每个任务都拥有其独立维护的堆栈。如果 
使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate/) 创建任务，
则用作任务堆栈的内存会从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)中自动分配，
并通过传递至 xTaskCreate() API 函数的参数来确定内存大小。如果 
使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 创建任务，则用作任务堆栈的内存由 
应用程序编写者预先分配。堆栈溢出是应用程序不稳定的一个很常见的原因。因此 FreeRTOS 
提供两个可选机制，用于协助检测并纠正 
出现的堆栈溢出问题。使用的选项通过 [configCHECK_FOR_STACK_OVERFLOW 配置常量](/Documentation/02-Kernel/03-Supported-devices/02-Customization)来配置。

请注意，这些选项仅适用于内存映射未分段的架构。
此外，在 RTOS 内核溢出检查开始之前，某些处理器可能会因堆栈损坏而 
发生故障或异常。如果 cconfigCHECK_FOR_STACK_OVERFLOW 未设置为 0 ， 
则应用程序必须提供堆栈溢出钩子函数。钩子函数必须命名为 vApplicationStackOverflowHook()， 
并且具备以下原型：

```c
void vApplicationStackOverflowHook( TaskHandle_t xTask,
                                    char *pcTaskName );
```

xTask 和 pcTaskName 参数分别将违规任务的句柄和名称传递给该钩子函数。
但请注意，根据溢出的严重程度，这些参数本身可能会损坏，在这种情况下，
可直接检查 pxCurrentTCB 变量。

堆栈溢出检查会增加上下文切换的开销，因此建议只在开发或测试阶段使用 
此检查。


### 堆栈溢出检测——方法 1

在 RTOS 内核使任务退出运行状态后，堆栈可能达到其最大（最深）值， 
因为此时的堆栈会包含任务上下文。此时， 
RTOS 内核可以检查处理器堆栈指针是否仍处于有效堆栈空间内。如果堆栈指针 
包含超出有效堆栈范围的值，则将调用堆栈溢出钩子函数。

此方法很快，但不能保证可以捕获所有堆栈溢出。将 configCHECK_FOR_STACK_OVERFLOW 设置 
为 1 即可使用此方法。


### 堆栈溢出检测——方法 2

任务首次创建时，其堆栈会填充一个已知值。任务退出运行状态时， 
RTOS 内核可以检查最后 16 个字节是否处于有效堆栈范围内，以确保这些已知值 
未被任务或中断活动所覆盖。如果这 16 个字节中的任何一个不再为初始值， 
则调用堆栈溢出钩子函数。

这种方法比方法 1 效率低，但仍然相当快。它很可能会捕获堆栈溢出， 
但仍无法保证能够捕获所有溢出。

将 configCHECK_FOR_STACK_OVERFLOW 设置为 2 即可使用此方法。


### 堆栈溢出检测——方法 3

将 configCHECK_FOR_STACK_OVERFLOW 设置为 3 即可使用此方法。

此方法仅适用于选定的端口。如果可用，该方法将启用 ISR 堆栈检查。
检测到 ISR 堆栈溢出时，会触发断言。请注意，在这种情况下不会调用堆栈溢出钩子函数， 
因为它只针对任务堆栈，而不是针对 ISR 堆栈。

