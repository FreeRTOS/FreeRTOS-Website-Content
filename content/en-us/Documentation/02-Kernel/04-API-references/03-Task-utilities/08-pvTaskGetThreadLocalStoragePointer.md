---
title: pvTaskGetThreadLocalStoragePointer
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Task Utilities](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)]

task.h

```c
void *pvTaskGetThreadLocalStoragePointer(
                                 TaskHandle_t xTaskToQuery,
                                 BaseType_t xIndex );
```

Retrieves a value from a task's [thread local storage array](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/16-Thread-local-storage-pointers).

This function is intended for advanced users only.


**Parameters:**

+ *xTaskToQuery*

  The handle of the task from which the thread local data is being read. A task can read its own thread
  local data by using NULL as the parameter value.

+ *xIndex*

  The index into the thread local storage array from which data is being read.

  The number of available array indexes is set by
  the [configNUM\_THREAD\_LOCAL\_STORAGE\_POINTERS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#confignum_thread_local_storage_pointers)
  compile time configuration constant in [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization).


**Returns:**

 The values stored in index position xIndex of the thread local storage array of task xTaskToQuery.


**Example usage:**

See the examples provided on the [thread local storage array](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/16-Thread-local-storage-pointers)
documentation page.
