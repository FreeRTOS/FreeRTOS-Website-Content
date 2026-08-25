---
title: xSemaphoreGiveFromISR
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
xSemaphoreGiveFromISR
 (
 SemaphoreHandle_t xSemaphore,
 signed BaseType_t *pxHigherPriorityTaskWoken
 )
```

用于释放信号量的*宏*。释放前信号量必须已经
通过调用 xSemaphoreCreateBinary() 或 xSemaphoreCreateCounting() 创建。

互斥锁型信号量（那些调用 xSemaphoreCreateMutex() 创建的信号量）
不得与此宏一起使用。

此宏可在 ISR 中使用。


**参数：**

+ *xSemaphore* 

  要释放的信号量的句柄。这是创建信号量时返回的句柄。

+ *pxHigherPriorityTaskWoken* 

  如果给出信号量会导致任务解除阻塞，并且解除阻塞的任务的优先级高于当前正在运行的任务， 
  则 xSemaphoreGiveFromISR() 会将 *pxHigherPriorityTaskWoken 设置为 pdTRUE。 
  如果 xSemaphoreGiveFromISR() 将此值设置为 pdTRUE，则应在退出中断之前请求上下文切换。 
  从 FreeRTOS V7.3.0 开始，pxHigherPriorityTaskWoken 为可选参数， 
  可设置为 NULL。


**返回：**

如果成功给出信号量，则返回 pdTRUE，否则 errQUEUE_FULL。


**用法示例：**

请注意，
使用[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)代替信号量，
通常可以更有效地实现如下所示的功能。

```c
#define LONG_TIME 0xffff
#define TICKS_TO_WAIT 10

SemaphoreHandle_t xSemaphore = NULL;

/* Repetitive task. */
void vATask( void * pvParameters )
{
    /* We are using the semaphore for synchronisation so we create a binary
       semaphore rather than a mutex. We must make sure that the interrupt
       does not attempt to use the semaphore before it is created! */
    xSemaphore = xSemaphoreCreateBinary();

    for( ;; )
    {
        /* We want this task to run every 10 ticks of a timer. The semaphore
           was created before this task was started.

           Block waiting for the semaphore to become available. */
        if( xSemaphoreTake( xSemaphore, LONG_TIME ) == pdTRUE )
        {
            /* It is time to execute. */

             ...

            /* We have finished our task. Return to the top of the loop where
               we will block on the semaphore until it is time to execute
               again. Note when using the semaphore for synchronisation with an
               ISR in this manner there is no need to 'give' the semaphore
               back. */
        }
    }
}

/* Timer ISR */
void vTimerISR( void * pvParameters )
{
static unsigned char ucLocalTickCount = 0;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* A timer tick has occurred. */

    ... Do other time functions.

    /* Is it time for vATask() to run? */
    xHigherPriorityTaskWoken = pdFALSE;
    ucLocalTickCount++;
    if( ucLocalTickCount >= TICKS_TO_WAIT )
    {
        /* Unblock the task by releasing the semaphore. */
        xSemaphoreGiveFromISR( xSemaphore, &xHigherPriorityTaskWoken );

        /* Reset the count so we release the semaphore again in 10 ticks
           time. */
        ucLocalTickCount = 0;
    }

    /* Yield if xHigherPriorityTaskWoken is true. The 
       actual macro used here is port specific. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
