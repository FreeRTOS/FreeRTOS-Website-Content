---
title: xTaskCreateStatic
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

```c
task. h
 TaskHandle_t xTaskCreateStatic( TaskFunction_t pxTaskCode,
                                 const char * const pcName,
                                 const uint32_t ulStackDepth,
                                 void * const pvParameters,
                                 UBaseType_t uxPriority,
                                 StackType_t * const puxStackBuffer,
                                 StaticTask_t * const pxTaskBuffer );
```

创建一项新[任务](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines/) 
并将其添加到准备运行的任务列表中。[configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation) 
必须在 `FreeRTOSConfig.h` 中设置为 1，才可使用此 RTOS API 函数。

每项任务都需要 RAM 来保存任务状态，并由任务用作其堆栈。如果 
使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate/) 创建任务， 
则所需的 RAM 将从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)自动分配。如果 
使用 `xTaskCreateStatic()` 创建任务，则 RAM 由应用程序编写者提供，这会产生更多的参数， 
但这样能够在编译时静态分配 RAM。有关详细信息，请参阅 
[静态分配与动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面。

如果使用的是 [FreeRTOS-MPU](/Security/04-FreeRTOS-MPU-memory-protection-unit)，建议 
使用 [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted)，而不是 `xTaskCreateStatic()`。


**参数：**
+ *pxTaskCode*     

  指向任务入口函数的指针（即实现任务的函数名称， 
  请参阅如下示例）。 

  任务通常[以无限循环的形式实现](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/05-Implementing-a-task)； 
  实现任务的函数绝不能尝试返回或退出。但是，任务可以 
  [自行删除](/Documentation/02-Kernel/04-API-references/01-Task-creation/03-vTaskDelete/)。

+ *pcName*  

  任务的描述性名称。此参数主要用于方便调试，但也可用于 
  [获取任务句柄](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle)。

  任务名称的最大长度由 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中的 `configMAX_TASK_NAME_LEN` 定义。                                                                                                                                                |
+ *ulStackDepth* 

  `puxStackBuffer` 参数用于将 `StackType_t` 变量的数组 
  传递至 `xTaskCreateStatic()`。`ulStackDepth` 必须设置为数组中的索引数。

  请参阅常见问题：[堆栈应该多大？](/Why-FreeRTOS/FAQs/Memory-usage-boot-times-context#how-big-should-the-stack-be)                                                                                                                                                                  |
+ *pvParameters*  

  作为参数传递给所创建任务的值。

  如果 `pvParameters` 设置为某变量的地址，则在创建的任务执行时，该变量必须仍然存在， 
  因此，不能传递堆栈变量的地址。                                                                                                                                                           |
+ *uxPriority* 

  创建的任务将以该指定[优先级](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities)执行。

  支持 MPU 的系统 
  可以通过在 `uxPriority` 中设置 `portPRIVILEGE_BIT` 位来选择以特权（系统）模式创建任务。例如，要创建优先级为 2 的特权任务， 
  请将 `uxPriority` 设置为 ( 2 | `portPRIVILEGE_BIT` )。

  应断言优先级低于 `configMAX_PRIORITIES`。如果 `configASSERT` 未定义，则优先级 
  默认上限为 (`configMAX_PRIORITIES` - 1)。

+ *puxStackBuffer* 

  必须指向至少包含 `ulStackDepth` 个索引的 `StackType_t` 数组（见上述 `ulStackDepth` 参数）， 
  该数组将用作任务堆栈，因此必须持久存在 
  （不能在函数的堆栈上声明）。                                                                                                                                                                                   |
+ *pxTaskBuffer* 

  必须指向 `StaticTask_t` 类型的变量。该变量将用于保存新任务的数据 
  结构体 (TCB)，因此必须持久存在（不能在函数的堆栈上声明）。


**返回：**

如果 `puxStackBuffer` 和 `pxTaskBuffer` 均不为 NULL，则创建任务， 
并返回任务的句柄。如果 `puxStackBuffer` 或 `pxTaskBuffer` 为 NULL，则不会创建任务， 
并返回 NULL。


**用法示例：**

```c
    /* Dimensions of the buffer that the task being created will use as its stack.
       NOTE: This is the number of words the stack will hold, not the number of
       bytes. For example, if each stack item is 32-bits, and this is set to 100,
       then 400 bytes (100 * 32-bits) will be allocated. */
    #define STACK_SIZE 200

    /* Structure that will hold the TCB of the task being created. */
    StaticTask_t xTaskBuffer;

    /* Buffer that the task being created will use as its stack. Note this is
       an array of StackType_t variables. The size of StackType_t is dependent on
       the RTOS port. */
    StackType_t xStack[ STACK_SIZE ];


    /* Function that implements the task being created. */
    void vTaskCode( void * pvParameters )
    {
        /* The parameter value is expected to be 1 as 1 is passed in the
           pvParameters value in the call to xTaskCreateStatic(). */
        configASSERT( ( uint32_t ) pvParameters == 1UL );

        for( ;; )
        {
            /* Task code goes here. */
        }
    }

    /* Function that creates a task. */
    void vOtherFunction( void )
    {
        TaskHandle_t xHandle = NULL;

        /* Create the task without using any dynamic memory allocation. */
        xHandle = xTaskCreateStatic(
                      vTaskCode,       /* Function that implements the task. */
                      "NAME",          /* Text name for the task. */
                      STACK_SIZE,      /* Number of indexes in the xStack array. */
                      ( void * ) 1,    /* Parameter passed into the task. */
                      tskIDLE_PRIORITY,/* Priority at which the task is created. */
                      xStack,          /* Array to use as the task's stack. */
                      &xTaskBuffer );  /* Variable to hold the task's data structure. */

        /* puxStackBuffer and pxTaskBuffer were not NULL, so the task will have
           been created, and xHandle will be the task's handle. Use the handle
           to suspend the task. */
        [vTaskSuspend](/Documentation/02-Kernel/04-API-references/02-Task-control/06-vTaskSuspend)( xHandle );
    }
```
