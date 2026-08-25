---
title: xSemaphoreTake
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
 xSemaphoreTake( SemaphoreHandle_t xSemaphore,
                 TickType_t xTicksToWait );
```

用于获取信号量的*宏*。信号量必须在之前已经
通过调用 `xSemaphoreCreateBinary()`、`xSemaphoreCreateMutex()` 或
`xSemaphoreCreateCounting()` 创建。

不得从 ISR 调用此宏。如果需要，`xQueueReceiveFromISR()` 可用来从中断中获取一个信号量， 
尽管这不是正常操作。信号量使用队列作为 
其底层机制，因此函数在某种程度上可互操作。


**参数：**

- *xSemaphore*

  正在获取的信号量的句柄——在创建信号量时获得。


- *xTicksToWait*

  等待信号量变为可用的时间（以滴答为单位）。宏 `portTICK_PERIOD_MS` 可以 
  将其转换为实际时间。可以用一个为零的阻塞时间来轮询信号量。 
  如果 [INCLUDE_vTaskSuspend](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 设置为 1，则将阻塞时间指定为 `portMAX_DELAY` 
  会导致任务无限期地阻塞（没有超时限制）。


**返回：**

- 如果获得信号量，则返回 *pdTRUE*。 
- 如果 `xTicksToWait` 过期，信号量不可用，则返回 *pdFALSE*。


**用法示例：** 

```c
SemaphoreHandle_t xSemaphore = NULL;

/* A task that creates a semaphore. */
void vATask( void * pvParameters )
{
    /* Create the semaphore to guard a shared resource. As we are using
       the semaphore for mutual exclusion we create a mutex semaphore
       rather than a binary semaphore. */
    xSemaphore = xSemaphoreCreateMutex();
}

/* A task that uses the semaphore. */
void vAnotherTask( void * pvParameters )
{
    /* ... Do other things. */

    if( xSemaphore != NULL )
    {
        /* See if we can obtain the semaphore. If the semaphore is not
           available wait 10 ticks to see if it becomes free. */
        if( xSemaphoreTake( xSemaphore, ( TickType_t ) 10 ) == pdTRUE )
        {
            /* We were able to obtain the semaphore and can now access the
               shared resource. */

            /* ... */

            /* We have finished accessing the shared resource. Release the
               semaphore. */
            xSemaphoreGive( xSemaphore );
        }
        else
        {
            /* We could not obtain the semaphore and can therefore not access
               the shared resource safely. */
        }
    }
}
```
