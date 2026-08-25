---
title: pvTaskGetThreadLocalStoragePointer
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---



[[任务实用程序](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)]

task. h

```c
void *pvTaskGetThreadLocalStoragePointer(
                                 TaskHandle_t xTaskToQuery,
                                 BaseType_t xIndex );
```

从任务的[线程本地存储数组](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/16-Thread-local-storage-pointers)中检索一个值。

此功能仅适用于高级用户。


**参数：**

+ *xTaskToQuery*

  正在读取线程本地数据的任务句柄。任务可以通过
  使用 NULL 作为参数值自行读取其线程本地数据。

+ *xIndex*

  读取数据的线程本地存储数组的索引。

  可用数组索引的数量由
  [configNUM_THREAD_LOCAL_STORAGE_POINTERS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#confignum_thread_local_storage_pointers)
  编译时配置常量（位于 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中）设置。


**返回：**

 存储在任务 xTaskToQuery 的线程本地存储数组的索引位置 xIndex 中的值。


**用法示例：**

请参阅[线程本地存储数组](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/16-Thread-local-storage-pointers)
文档页面。
