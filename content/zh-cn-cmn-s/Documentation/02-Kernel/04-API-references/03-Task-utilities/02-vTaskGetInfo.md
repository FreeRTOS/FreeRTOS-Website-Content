---
title: vTaskGetInfo()
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
void vTaskGetInfo( TaskHandle_t xTask,
                   TaskStatus_t *pxTaskStatus,
                   BaseType_t xGetFreeStackSpace,
                   eTaskState eState );
```

`configUSE\_TRACE\_FACILITY` 必须在 FreeRTOSConfig.h 中定义为 1，才可使用 `vTaskGetInfo()`。

[uxTaskGetSystemState](/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState)() 会为系统中的每个任务填充 [TaskStatus_t](#taskstatus_t-定义) 结构体，
而 `vTaskGetInfo()` 只为单个任务填充 `TaskStatus\_t` 结构体 
。`TaskStatus_t` 结构体包含任务句柄成员、 
任务名称、任务优先级、任务状态以及任务消耗的总运行时间等。

注意：使用该函数会导致调度器长时间处于挂起状态， 
因此该函数仅用于调试。


**参数：** 

- *xTask*

  正在查询的任务的句柄。将 xTask 设置为 NULL 将返回调用任务的信息。
  
- *pxTaskStatus*

  `pxTaskStatus` 指向的 `TaskStatus\_t` 结构体中将填入 
  `xTask` 参数中传递的句柄引用的任务信息。
  
- *xGetFreeStackSpace* 

  `TaskStatus\_t` 结构体包含一个成员，用于报告所查询任务的 
  堆栈高水位线。堆栈高水位线是指堆栈中曾存在的最小可用空间， 
  因此数值越接近零，任务堆栈溢出的风险越高。计算 
  堆栈高水位线需要的时间相对较长，并且可能会导致系统暂时无响应， 
  因此特提供 `xGetFreeStackSpace` 参数，可用于跳过高水位线检查。 
  高水位线值写入 `TaskStatus\_t` 结构体的前提是，`xGetFreeStackSpace` 
  未设置为 `pdFALSE`。
  
- *eState*

  `TaskStatus\_t` 结构体包含一个成员，用于报告所查询任务的状态。获取 
  任务状态并不像简单赋值那样快，因此特提供 `eState` 参数，可用于 
  忽略 `TaskStatus\_t` 结构体中的状态信息。要获取状态信息， 
  请将 eState 设置为 `eInvalid`，否则 `eState` 中传递的值将被报告为 
  `TaskStatus\_t` 结构体中的任务状态。


**用法示例：**

```c
void vAFunction( void )
{
    TaskHandle_t xHandle;
    TaskStatus_t xTaskDetails;

    /* Obtain the handle of a task from its name. */
    xHandle = xTaskGetHandle( "Task_Name" );

    /* Check the handle is not NULL. */
    configASSERT( xHandle );

    /* Use the handle to obtain further information about the task. */
    vTaskGetInfo( /* The handle of the task being queried. */
                  xHandle,
                  /* The TaskStatus_t structure to complete with information
                     on xTask. */
                  &xTaskDetails,
                  /* Include the stack high water mark value in the
                     TaskStatus_t structure. */
                  pdTRUE,
                  /* Include the task state in the TaskStatus_t structure. */
                  eInvalid );
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

    /* The total run time allocated to the task so far, as defined by the run
       time stats clock. Only valid when configGENERATE_RUN_TIME_STATS is
       defined as 1 in FreeRTOSConfig.h. */
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

