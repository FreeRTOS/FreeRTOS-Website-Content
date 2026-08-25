---
title: "不依赖于特定硬件的 FreeRTOS 示例"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[另请参阅[快速入门指南](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview)和 [FreeRTOS 简单项目入门](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
文档页面。]

## 简介

[RTOS 下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)包含大量
预配置的[示例项目](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)，
开箱即用。这可确保用户在很短的时间内就让有效 RTOS 项目在
真实硬件上运行。然而，不可能支持
微控制器、编译器和开发板的所有组合，
并且我们经常需要提供一个不依赖于任何这些变量的示例。本页
提供的代码就是为实现此目的。由于其中的代码十分简单，
此示例对于那些还没有完全
熟悉 FreeRTOS 的人来说也是一个很好的入门项目。

源代码不访问任何特定于硬件的 IO。例如，源代码只是
增加变量，而不是尝试切换 LED。但是，
与预打包的示例不同，源代码确实要求用户
[创建自己的
编译器项目](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)。步骤如下：

1. 从工作（非 RTOS）项目开始，以确保
   使用的启动文件和链接器脚本正确。

2. 添加正确的 [RTOS 源文件](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)。使用
   现有官方 RTOS 演示项目作为参考。

3. 添加正确的编译器 include 路径，必须包括
   RTOS 内核头文件（RTOS 下载中的 FreeRTOS/Source/include）
   和可移植层头文件（FreeRTOS/Source/[compiler]/[architecture]/portmacro.h，
   位于 RTOS 下载中）。

4. 定义 FreeRTOSConfig.h 文件，或至少复制 FreeRTOSConfig.h
   （从与正在创建的项目非常匹配的官方 RTOS 演示中）。

另请参阅[创建新的 FreeRTOS 项目](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)文档，了解详细信息。

## 独立于硬件的 RTOS 演示功能

以下是示例功能的描述：

### main() 函数

main() 用于在启动调度程序之前创建本节中
描述的任务和软件定时器。

### 队列发送任务

队列发送任务由 prvQueueSendTask() 函数实现。
该任务使用 FreeRTOS [vTaskDelayUntil()](/Documentation/02-Kernel/04-API-references/02-Task-control/02-vTaskDelayUntil)
和 [xQueueSend()](/Documentation/02-Kernel/04-API-references/06-Queues/03-xQueueSend) API 函数
周期性地发送队列上的数字 100。周期设置为 200 毫秒。请参阅
函数中的注释以获取更多详细信息。

### 队列接收任务

队列接收任务由 prvQueueReceiveTask() 函数实现。
任务使用 FreeRTOS [xQueueReceive()](/Documentation/02-Kernel/04-API-references/06-Queues/09-xQueueReceive) API 函数
从队列中接收值。接收的值是由队列发送任务
发送的值。队列接收任务每次接收到值 100 时，
都会递增 ulCountofItemsReceivedOnQueue 变量。因此，由于每 200 毫秒就会向队列发送一次值，
因此 ulCountofItemsReceivedOnQueue 的值将每秒
增加 5。

### 软件定时器示例

创建了一个[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)，
其自动重新加载周期为 1000 毫秒。每次调用
定时器的回调函数时都会
递增 ulCountOfTimerCallbackExecutions 变量。因此，
ulCountOfTimerCallbackExecutions 的值为数秒。

### FreeRTOS RTOS 滴答钩子（或回调）函数

滴答钩子函数在 FreeRTOS 滴答中断的上下文中执行。
该函数每执行 500 次就“发送”一个信号量。信号量
用于与事件信号量任务同步，这将在后面介绍。
在本例中，优先使用滴答中断而非
外围设备生成的中断，以确保维持硬件的独立性。

### 事件信号量任务

事件信号量任务使用 FreeRTOS [xSemaphoreTake()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)
API 函数来等待由 RTOS 滴答钩子函数发出的信号量。
每次收到信号量时，
该任务都会递增 ulCountOfReceivedSemaphores 变量。由于信号量每 500 毫秒给出一次（假设滴答频率为 1KHz），
因此 ulCountOfReceivedSemaphores 的值将每秒增加 2。

**注意：**信号量用于示例目的。在实际的应用程序中，
最好使用
[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore)，
这样速度更快，占用的 RAM 更少。

### 空闲钩子（或回调）函数

空闲钩子函数查询可用的空闲 FreeRTOS 堆空间。
请参阅代码中的 vApplicationIdleHook()。

### malloc 失败和堆栈溢出钩子（或回调）函数。

这两个钩子函数作为示例提供，但不包含任何
功能。

## 源代码

在源文件中搜索 TODO，查找可能
需要修改的地方。

```c
/* Kernel includes. */
#include "FreeRTOS.h" /* Must come first. */
#include "task.h" /* RTOS task related API prototypes. */
#include "queue.h" /* RTOS queue related API prototypes. */
#include "timers.h" /* Software timer related API prototypes. */
#include "semphr.h" /* Semaphore related API prototypes. */

/* TODO Add any manufacture supplied header files can be included here. */
#include "hardware.h"

/* Priorities at which the tasks are created. The event semaphore task is
   given the maximum priority of ( configMAX_PRIORITIES - 1 ) to ensure it runs as
   soon as the semaphore is given. */
#define mainQUEUE_RECEIVE_TASK_PRIORITY ( tskIDLE_PRIORITY + 2 )
#define mainQUEUE_SEND_TASK_PRIORITY ( tskIDLE_PRIORITY + 1 )
#define mainEVENT_SEMAPHORE_TASK_PRIORITY ( configMAX_PRIORITIES - 1 )

/* The rate at which data is sent to the queue, specified in milliseconds, and
   converted to ticks using the pdMS_TO_TICKS() macro. */
#define mainQUEUE_SEND_PERIOD_MS pdMS_TO_TICKS( 200 )

/* The period of the example software timer, specified in milliseconds, and
   converted to ticks using the pdMS_TO_TICKS() macro. */
#define mainSOFTWARE_TIMER_PERIOD_MS pdMS_TO_TICKS( 1000 )

/* The number of items the queue can hold. This is 1 as the receive task
   has a higher priority than the send task, so will remove items as they are added,
   meaning the send task should always find the queue empty. */
#define mainQUEUE_LENGTH ( 1 )

/*-----------------------------------------------------------*/

/*
 * TODO: Implement this function for any hardware specific clock configuration
 * that was not already performed before main() was called.
 */
static void prvSetupHardware( void );

/*
 * The queue send and receive tasks as described in the comments at the top of
 * this file.
 */
static void prvQueueReceiveTask( void *pvParameters );
static void prvQueueSendTask( void *pvParameters );

/*
 * The callback function assigned to the example software timer as described at
 * the top of this file.
 */
static void vExampleTimerCallback( TimerHandle_t xTimer );

/*
 * The event semaphore task as described at the top of this file.
 */
static void prvEventSemaphoreTask( void *pvParameters );

/*-----------------------------------------------------------*/

/* The queue used by the queue send and queue receive tasks. */
static QueueHandle_t xQueue = NULL;

/* The semaphore (in this case binary) that is used by the FreeRTOS tick hook
 * function and the event semaphore task.
 */
static SemaphoreHandle_t xEventSemaphore = NULL;

/* The counters used by the various examples. The usage is described in the
 * comments at the top of this file.
 */
static volatile uint32_t ulCountOfTimerCallbackExecutions = 0;
static volatile uint32_t ulCountOfItemsReceivedOnQueue = 0;
static volatile uint32_t ulCountOfReceivedSemaphores = 0;

/*-----------------------------------------------------------*/

int main(void)
{
TimerHandle_t xExampleSoftwareTimer = NULL;

    /* Configure the system ready to run the demo. The clock configuration
       can be done here if it was not done before main() was called. */
    prvSetupHardware();

    /* Create the queue used by the queue send and queue receive tasks. */
    xQueue = xQueueCreate( /* The number of items the queue can hold. */
                           mainQUEUE_LENGTH,
                           /* The size of each item the queue holds. */
                           sizeof( uint32_t ) );

    /* Create the semaphore used by the FreeRTOS tick hook function and the
       event semaphore task. **NOTE:** A semaphore is used for example purposes,
       using a direct to task notification will be faster! */
    xEventSemaphore = xSemaphoreCreateBinary();

    /* Create the queue receive task as described in the comments at the top
       of this file. */
    xTaskCreate( /* The function that implements the task. */
                 prvQueueReceiveTask,
                 /* Text name for the task, just to help debugging. */
                 "Rx",
                 /* The size (in words) of the stack that should be created
                    for the task. */
                 configMINIMAL_STACK_SIZE,
                 /* A parameter that can be passed into the task. Not used
                    in this simple demo. */
                 NULL,
                 /* The priority to assign to the task. tskIDLE_PRIORITY
                    (which is 0) is the lowest priority. configMAX_PRIORITIES - 1
                    is the highest priority. */
                 mainQUEUE_RECEIVE_TASK_PRIORITY,
                 /* Used to obtain a handle to the created task. Not used in
                    this simple demo, so set to NULL. */
                 NULL );

    /* Create the queue send task in exactly the same way. Again, this is
       described in the comments at the top of the file. */
    xTaskCreate( prvQueueSendTask,
                 "TX",
                  configMINIMAL_STACK_SIZE,
                  NULL,
                  mainQUEUE_SEND_TASK_PRIORITY,
                  NULL );

    /* Create the task that is synchronised with an interrupt using the
       xEventSemaphore semaphore. */
    xTaskCreate( prvEventSemaphoreTask,
                 "Sem",
                 configMINIMAL_STACK_SIZE,
                 NULL,
                 mainEVENT_SEMAPHORE_TASK_PRIORITY,
                 NULL );

    /* Create the software timer as described in the comments at the top of
       this file. */
    xExampleSoftwareTimer = xTimerCreate( /* A text name, purely to help debugging. */
                                          ( const char * ) "LEDTimer",
                                          /* The timer period, in this case
                                             1000ms (1s). */
                                          mainSOFTWARE_TIMER_PERIOD_MS,
                                          /* This is a periodic timer, so
                                             xAutoReload is set to pdTRUE. */
                                          pdTRUE,
                                          /* The ID is not used, so can be set
                                             to anything. */
                                          ( void * ) 0,
                                          /* The callback function that switches
                                             the LED off. */
                                          vExampleTimerCallback
                                        );

    /* Start the created timer. A block time of zero is used as the timer
       command queue cannot possibly be full here (this is the first timer to
       be created, and it is not yet running). */
    xTimerStart( xExampleSoftwareTimer, 0 );

    /* Start the tasks and timer running. */
    vTaskStartScheduler();

    /* If all is well, the scheduler will now be running, and the following line
       will never be reached. If the following line does execute, then there was
       insufficient FreeRTOS heap memory available for the idle and/or timer tasks
       to be created. See the memory management section on the FreeRTOS web site
       for more details. */
    for( ;; );
}
/*-----------------------------------------------------------*/

static void vExampleTimerCallback( TimerHandle_t xTimer )
{
    /* The timer has expired. Count the number of times this happens. The
       timer that calls this function is an auto re-load timer, so it will
       execute periodically. */
    ulCountOfTimerCallbackExecutions++;
}
/*-----------------------------------------------------------*/

static void prvQueueSendTask( void *pvParameters )
{
TickType_t xNextWakeTime;
const uint32_t ulValueToSend = 100UL;

    /* Initialise xNextWakeTime - this only needs to be done once. */
    xNextWakeTime = xTaskGetTickCount();

    for( ;; )
    {
        /* Place this task in the blocked state until it is time to run again.
           The block time is specified in ticks, the constant used converts ticks
           to ms. The task will not consume any CPU time while it is in the
           Blocked state. */
        vTaskDelayUntil( &xNextWakeTime, mainQUEUE_SEND_PERIOD_MS );

        /* Send to the queue - causing the queue receive task to unblock and
           increment its counter. 0 is used as the block time so the sending
           operation will not block - it shouldn't need to block as the queue
           should always be empty at this point in the code. */
        xQueueSend( xQueue, &ulValueToSend, 0 );
    }
}
/*-----------------------------------------------------------*/

static void prvQueueReceiveTask( void *pvParameters )
{
uint32_t ulReceivedValue;

    for( ;; )
    {
        /* Wait until something arrives in the queue - this task will block
           indefinitely provided INCLUDE_vTaskSuspend is set to 1 in
           FreeRTOSConfig.h. */
        xQueueReceive( xQueue, &ulReceivedValue, portMAX_DELAY );

        /* To get here something must have been received from the queue, but
           is it the expected value? If it is, increment the counter. */
        if( ulReceivedValue == 100UL )
        {
            /* Count the number of items that have been received correctly. */
            ulCountOfItemsReceivedOnQueue++;
        }
    }
}
/*-----------------------------------------------------------*/

static void prvEventSemaphoreTask( void *pvParameters )
{
    for( ;; )
    {
        /* Block until the semaphore is 'given'. **NOTE:**
           A semaphore is used for example purposes. In a real application it might
           be preferable to use a direct to task notification, which will be faster
           and use less RAM. */
        xSemaphoreTake( xEventSemaphore, portMAX_DELAY );

        /* Count the number of times the semaphore is received. */
        ulCountOfReceivedSemaphores++;
    }
}
/*-----------------------------------------------------------*/

void vApplicationTickHook( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
static uint32_t ulCount = 0;

    /* The RTOS tick hook function is enabled by setting configUSE_TICK_HOOK to
       1 in FreeRTOSConfig.h.

       "Give" the semaphore on every 500th tick interrupt. */
    ulCount++;
    if( ulCount >= 500UL )
    {
        /* This function is called from an interrupt context (the RTOS tick
           interrupt), so only ISR safe API functions can be used (those that end
           in "FromISR()").

           xHigherPriorityTaskWoken was initialised to pdFALSE, and will be set to
           pdTRUE by xSemaphoreGiveFromISR() if giving the semaphore unblocked a
           task that has equal or higher priority than the interrupted task.
           **NOTE:** A semaphore is used for example purposes. In a real application it
           might be preferable to use a direct to task notification,
           which will be faster and use less RAM. */
        xSemaphoreGiveFromISR( xEventSemaphore, &xHigherPriorityTaskWoken );
        ulCount = 0UL;
    }

 /* If xHigherPriorityTaskWoken is pdTRUE then a context switch should
    normally be performed before leaving the interrupt (because during the
    execution of the interrupt a task of equal or higher priority than the
    running task was unblocked). The syntax required to context switch from
    an interrupt is port dependent, so check the documentation of the port you
    are using.

    In this case, the function is running in the context of the tick interrupt,
    which will automatically check for the higher priority task to run anyway,
    so no further action is required. */
}
/*-----------------------------------------------------------*/

void vApplicationMallocFailedHook( void )
{
    /* The malloc failed hook is enabled by setting
       configUSE_MALLOC_FAILED_HOOK to 1 in FreeRTOSConfig.h.

       Called if a call to pvPortMalloc() fails because there is insufficient
       free memory available in the FreeRTOS heap. pvPortMalloc() is called
       internally by FreeRTOS API functions that create tasks, queues, software
       timers, and semaphores. The size of the FreeRTOS heap is set by the
       configTOTAL_HEAP_SIZE configuration constant in FreeRTOSConfig.h. */
    for( ;; );
}
/*-----------------------------------------------------------*/

void vApplicationStackOverflowHook( TaskHandle_t xTask, char *pcTaskName )
{
( void ) pcTaskName;
( void ) xTask;

    /* Run time stack overflow checking is performed if
       configconfigCHECK_FOR_STACK_OVERFLOW is defined to 1 or 2. This hook
       function is called if a stack overflow is detected. pxCurrentTCB can be
       inspected in the debugger if the task name passed into this function is
       corrupt. */
     for( ;; );
}
/*-----------------------------------------------------------*/

void vApplicationIdleHook( void )
{
volatile size_t xFreeStackSpace;

    /* The idle task hook is enabled by setting configUSE_IDLE_HOOK to 1 in
       FreeRTOSConfig.h.

       This function is called on each cycle of the idle task. In this case it
       does nothing useful, other than report the amount of FreeRTOS heap that
       remains unallocated. */
    xFreeStackSpace = xPortGetFreeHeapSize();

    if( xFreeStackSpace > 100 )
    {
        /* By now, the kernel has allocated everything it is going to, so
           if there is a lot of heap remaining unallocated then
           the value of configTOTAL_HEAP_SIZE in FreeRTOSConfig.h can be
           reduced accordingly. */
    }
}

/*-----------------------------------------------------------*/

static void prvSetupHardware( void )
{
 /* Ensure all priority bits are assigned as preemption priority bits
    if using a ARM Cortex-M microcontroller. */
 NVIC_SetPriorityGrouping( 0 );

 /* TODO: Setup the clocks, etc. here, if they were not configured before
    main() was called. */
}
```

