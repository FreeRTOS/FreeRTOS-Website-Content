---
title: uxTaskGetSystemState()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[任务实用程序](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)]

task.h


```c
UBaseType_t uxTaskGetSystemState(
                       TaskStatus_t * const pxTaskStatusArray,
                       const UBaseType_t uxArraySize,
                       unsigned long * const pulTotalRunTime );
```

`configUSE_TRACE_FACILITY` 必须在 FreeRTOSConfig.h 中定义为 1，才可使用 `uxTaskGetSystemState()`。


`uxTaskGetSystemState()` 为系统中的每个任务填充 [TaskStatus_t](#taskstatus_t-定义) 结构体。
`TaskStatus_t` 结构体包含任务句柄成员、任务名称、
任务优先级、任务状态以及任务消耗的总运行时间等。

如需为单一任务（而非每个任务）填充 `TaskStatus_t` 结构的版本，请参阅 [vTaskGetInfo()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/02-vTaskGetInfo)
。

**注意**：使用该函数会导致调度器长时间处于挂起状态，
因此该函数仅用于调试。


**参数：**

- *pxTaskStatusArray*

  指向 [TaskStatus_t](#taskstatus_t-定义) 结构体数组的指针。数组必须至少包含
  由 RTOS 控制的每个任务对应的一个 `TaskStatus_t` 结构体。由
  RTOS 控制的任务数量可以通过
  [uxTaskGetNumberOfTasks()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#ustaskgetnumberoftasks) API 函数确定。

- *uxArraySize*

  `pxTaskStatusArray` 参数指向的数组的大小。此大小指定为
  数组中的索引数量（数组中包含的 [TaskStatus_t](#taskstatus_t-定义) 结构体的数量），
  不是数组中的字节数。

- *pulTotalRunTime*

  如果 `configGENERATE_RUN_TIME_STATS` 在 FreeRTOSConfig.h 中设置为 1，则 `*pulTotalRunTime`
  由 `uxTaskGetSystemState()` 设置为目标启动以来的总运行时间
  （由[运行时统计时钟](/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics)定义）。`pulTotalRunTime` 可以
  设置为 NULL，以忽略总运行时间值。


**返回：**

- [TaskStatus_t](/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState#TaskStatus_t) 结构体（由
  `uxTaskGetSystemState()` 填充）的数量。这个数量应等于 `uxTaskGetNumberOfTasks()` API 函数返回的数字，
  但如果在 `uxArraySize` 参数中传递的值太小，则该数量将为零。


**用法示例：**

```c
/* This example demonstrates how a human readable table of run time stats
   information is generated from raw data provided by uxTaskGetSystemState().
   The human readable table is written to pcWriteBuffer. (see the vTaskList()
   API function which actually does just this). */
void vTaskGetRunTimeStats( char *pcWriteBuffer )
{
    TaskStatus_t *pxTaskStatusArray;
    volatile UBaseType_t uxArraySize, x;
    unsigned long ulTotalRunTime, ulStatsAsPercentage;

   /* Make sure the write buffer does not contain a string. */
   *pcWriteBuffer = 0x00;

   /* Take a snapshot of the number of tasks in case it changes while this
      function is executing. */
   uxArraySize = uxTaskGetNumberOfTasks();

   /* Allocate a TaskStatus_t structure for each task. An array could be
      allocated statically at compile time. */
   pxTaskStatusArray = pvPortMalloc( uxArraySize * sizeof( TaskStatus_t ) );

   if( pxTaskStatusArray != NULL )
   {
      /* Generate raw status information about each task. */
      uxArraySize = uxTaskGetSystemState( pxTaskStatusArray,
                                 uxArraySize,
                                 &ulTotalRunTime );

      /* For percentage calculations. */
      ulTotalRunTime /= 100UL;

      /* Avoid divide by zero errors. */
      if( ulTotalRunTime > 0 )
      {
         /* For each populated position in the pxTaskStatusArray array,
            format the raw data as human readable ASCII data. */
         for( x = 0; x < uxArraySize; x++ )
         {
            /* What percentage of the total run time has the task used?
               This will always be rounded down to the nearest integer.
               ulTotalRunTimeDiv100 has already been divided by 100. */
            ulStatsAsPercentage =
                  pxTaskStatusArray[ x ].ulRunTimeCounter / ulTotalRunTime;

            if( ulStatsAsPercentage > 0UL )
            {
               sprintf( pcWriteBuffer, "%stt%lutt%lu%%rn",
                                 pxTaskStatusArray[ x ].pcTaskName,
                                 pxTaskStatusArray[ x ].ulRunTimeCounter,
                                 ulStatsAsPercentage );
            }
            else
            {
               /* If the percentage is zero here then the task has
                  consumed less than 1% of the total run time. */
               sprintf( pcWriteBuffer, "%stt%lutt<1%%rn",
                                 pxTaskStatusArray[ x ].pcTaskName,
                                 pxTaskStatusArray[ x ].ulRunTimeCounter );
            }

            pcWriteBuffer += strlen( ( char * ) pcWriteBuffer );
         }
      }

      /* The array is no longer needed, free the memory it consumes. */
      vPortFree( pxTaskStatusArray );
   }
}
```

 
### TaskStatus_t 定义

```c
typedef struct xTASK_STATUS
{
   /* The handle of the task to which the rest of the information in the
      structure relates. */
   TaskHandle_t xHandle;

   /* A pointer to the task's name. This value will be invalid if the task was
      deleted since the structure was populated! */
   const char *pcTaskName;

   /* A number unique to the task. */
   UBaseType_t xTaskNumber;

   /* The state in which the task existed when the structure was populated. */
   eTaskState eCurrentState;

   /* The priority at which the task was running (may be inherited) when the
      structure was populated. */
   UBaseType_t uxCurrentPriority;

   /* The priority to which the task will return if the task's current priority
      has been inherited to avoid unbounded priority inversion when obtaining a
      mutex. Only valid if configUSE_MUTEXES is defined as 1 in
      FreeRTOSConfig.h. */
   UBaseType_t uxBasePriority;

   /* The total run time allocated to the task so far, as defined by the run time stats clock. 
      Only valid when configGENERATE_RUN_TIME_STATS is defined as 1 in FreeRTOSConfig.h. */
   unsigned long ulRunTimeCounter;

   /* Points to the lowest address of the task's stack area. */
   StackType_t *pxStackBase;

   #if ( configRECORD_STACK_HIGH_ADDRESS == 1 )
       /* Points to the top address of the task's stack area. */
       StackType_t * pxTopOfStack;

       /* Points to the bottom address of the task's stack area. */
       StackType_t * pxEndOfStack;
   #endif

   /* The minimum amount of stack space that has remained for the task since
      the task was created. The closer this value is to zero the closer the task
      has come to overflowing its stack. */
   configSTACK_DEPTH_TYPE usStackHighWaterMark;
} TaskStatus_t;
```
