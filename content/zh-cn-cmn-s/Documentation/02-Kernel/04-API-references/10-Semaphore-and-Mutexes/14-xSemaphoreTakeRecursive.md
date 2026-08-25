---
title: xSemaphoreTakeRecursive
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[信号量](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

semphr. h 

```c
xSemaphoreTakeRecursive( SemaphoreHandle_t xMutex,
                         TickType_t xTicksToWait );
```


递归地获得或“获取”一个互斥锁型信号量的*宏*。
此互斥锁必须已经事先通过调用
xSemaphoreCreateRecursiveMutex() 完成创建；

必须在 FreeRTOSConfig.h 中将 configUSE_RECURSIVE_MUTEXES 设置为 1，
此宏才可用。

不得在使用 xSemaphoreCreateMutex() 创建的互斥锁上使用此宏。

所有者可以反复“获取”递归使用的互斥锁。在所有者
为每个成功的“获取”请求调用
xSemaphoreGiveRecursive() 之前，该互斥锁不会再次变得可用。例如，
如果一个任务成功地“获取”了同一个互斥锁 5 次，
那么任何其他任务都无法使用此互斥锁，
直到任务也把这个互斥锁“解锁”5 次。


**参数：**

+ *xMutex* 

  正在获得的互斥锁的句柄。这是由 xSemaphoreCreateRecursiveMutex() 返回的句柄。

+ *xTicksToWait* 

  等待信号量变为可用的时间（以滴答为单位）。可以使用 portTICK_PERIOD_MS 宏 
  将其转换为实际时间。可以用一个为零的阻塞时间来轮询信号量。如果 
  任务已有信号量，则无论 xTicksToWait 的值是多少， 
  xSemaphoreTakeRecursive() 都将立即返回。


**返回：**

如果获得信号量，则返回 pdTRUE；如果 xTicksToWait 过期，信号量不可用，则返回 pdFALSE。


**用法示例：**

```c
 SemaphoreHandle_t xMutex = NULL;

 // A task that creates a mutex.
 void vATask( void * pvParameters )
 {
    // Create the mutex to guard a shared resource.
    xMutex = xSemaphoreCreateRecursiveMutex();
 }

 // A task that uses the mutex.
 void vAnotherTask( void * pvParameters )
 {
    // ... Do other things.

    if( xMutex != NULL )
    {
        // See if we can obtain the mutex. If the mutex is not available
        // wait 10 ticks to see if it becomes free. 
        if( xSemaphoreTakeRecursive( xMutex, ( TickType_t ) 10 ) == pdTRUE )
        {
            // We were able to obtain the mutex and can now access the
            // shared resource.

            // ...
            // For some reason due to the nature of the code further calls to 
            // xSemaphoreTakeRecursive() are made on the same mutex. In real
            // code these would not be just sequential calls as this would make
            // no sense. Instead the calls are likely to be buried inside
            // a more complex call structure.
            xSemaphoreTakeRecursive( xMutex, ( TickType_t ) 10 );
            xSemaphoreTakeRecursive( xMutex, ( TickType_t ) 10 );

            // The mutex has now been 'taken' three times, so will not be 
            // available to another task until it has also been given back
            // three times. Again it is unlikely that real code would have
            // these calls sequentially, but instead buried in a more complex
            // call structure. This is just for illustrative purposes.
            xSemaphoreGiveRecursive( xMutex );
            xSemaphoreGiveRecursive( xMutex );
            xSemaphoreGiveRecursive( xMutex );

            // Now the mutex can be taken by other tasks.
        }
        else
        {
            // We could not obtain the mutex and can therefore not access
            // the shared resource safely.
        }
    }
 }
```
