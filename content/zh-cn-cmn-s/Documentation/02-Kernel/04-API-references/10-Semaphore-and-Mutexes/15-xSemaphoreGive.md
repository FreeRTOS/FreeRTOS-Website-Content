---
title: xSemaphoreGive
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[信号量](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

[**提示：在许多使用场景中，使用直达任务通知要比使用信号量的速度更快，内存效率更高。**](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)

semphr. h 

```c
xSemaphoreGive( SemaphoreHandle_t xSemaphore );
```

用于释放信号量的*宏*。释放前信号量必须已经
通过调用 `xSemaphoreCreateBinary()`、`xSemaphoreCreateMutex()` 或 `xSemaphoreCreateCounting()` 创建。

不得在 ISR 中使用此宏。请参阅 `xSemaphoreGiveFromISR()`，了解可以从 ISR 中使用的替代方案。

此宏也不得用于使用 `xSemaphoreCreateRecursiveMutex()` 创建的信号量。


**参数：**

- *xSemaphore*

  要释放的信号量的句柄。这是创建信号量时返回的句柄。 |


**返回：**

- 如果信号量被释放，则返回 *pdTRUE*。 

- 如果发生错误，则返回 *pdFALSE*。信号量是使用队列实现的。发布消息时，如果队列上没有空间， 
  那么可能会发生错误，这表明最初未能正确获取信号量。


**用法示例：**

```c
SemaphoreHandle_t xSemaphore = NULL;
void vATask( void * pvParameters )
{
    // Create the semaphore to guard a shared resource.  As we are using
    // the semaphore for mutual exclusion we create a mutex semaphore
    // rather than a binary semaphore.
    xSemaphore = xSemaphoreCreateMutex();

    if( xSemaphore != NULL )
    {
        if( xSemaphoreGive( xSemaphore ) != pdTRUE )
        {
            // We would expect this call to fail because we cannot give
            // a semaphore without first "taking" it!
        }
        // Obtain the semaphore - don't block if the semaphore is not
        // immediately available.
        if( xSemaphoreTake( xSemaphore, ( TickType_t ) 0 ) )
        {
            // We now have the semaphore and can access the shared resource.
            // ...
            // We have finished accessing the shared resource so can free the
            // semaphore.
            if( xSemaphoreGive( xSemaphore ) != pdTRUE )
            {
                // We would not expect this call to fail because we must have
                // obtained the semaphore to get here.
            }
        }
    }
}
```
