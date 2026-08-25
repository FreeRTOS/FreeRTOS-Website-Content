---
title: vTaskSetThreadLocalStoragePointer
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
void vTaskSetThreadLocalStoragePointer( TaskHandle_t xTaskToSet,
                                        BaseType_t xIndex,
                                        void *pvValue )
```

设置任务的[线程本地存储数组](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/16-Thread-local-storage-pointers)中的值。

此功能仅适用于高级用户。


**参数：**

- *xTaskToSet*

  正在写入线程本地数据的任务句柄。使用 NULL 作为参数值，
  任务可以写入自己的线程本地数据。

- *xIndex*

  写入数据的线程本地存储数组的索引。可用数组索引的数量由
  [configNUM_THREAD_LOCAL_STORAGE_POINTERS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#confignum_thread_local_storage_pointers) 编译时配置常量
  （位于 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中）设置。

- *pvValue*

  要写入由 xIndex 参数指定的索引的值。


**用法示例：**

请参阅[线程本地存储数组](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/16-Thread-local-storage-pointers)
文档页面。
