---
title: "xTaskCreate"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: xTaskCreate 函数使用方法。
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---

task.h

```c
 BaseType_t xTaskCreate( TaskFunction_t pvTaskCode,
                         const char * const pcName,
                         const configSTACK_DEPTH_TYPE uxStackDepth,
                         void *pvParameters,
                         UBaseType_t uxPriority,
                         TaskHandle_t *pxCreatedTask
                       );
```

创建一项新[任务](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines/) 
并将其添加到准备运行的任务列表中。[configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation)
必须在 FreeRTOSConfig.h 中设置为 1，或处于未定义状态（默认为 1），
才可使用此 RTOS API 函数。

每项任务都需要 RAM 来保存任务状态，并由任务用作其堆栈。如果
使用 xTaskCreate() 创建任务，则所需的 RAM 会自动 
从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)分配。如果使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 创建任务，
则 RAM 由应用程序编写者提供，因此可以在编译时静态分配。
有关详细信息，请参阅[静态分配与动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面。

如果使用的是 [FreeRTOS-MPU](/Security/04-FreeRTOS-MPU-memory-protection-unit)，建议 
使用 [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted)，而不是 xTaskCreate()。


**参数：**

+ *pvTaskCode*

  指向任务入口函数的指针（即实现任务的函数名称，请参阅如下示例）。
  任务通常[以无限循环的形式实现](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/05-Implementing-a-task)；实现任务的函数
  绝不能尝试返回或退出。但是，任务可以 
  [自行删除](/Documentation/02-Kernel/04-API-references/01-Task-creation/03-vTaskDelete/)。

+ *pcName*

  任务的描述性名称。此参数主要用于方便调试，但也可用于 
  [获取任务句柄](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle)。任务名称的最大长度
  由 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中的 configMAX_TASK_NAME_LEN 定义。

+ *uxStackDepth*

  要[分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)用作任务堆栈的字数（不是字节数！）。例如，如果
  堆栈宽度为 16 位，uxStackDepth 为 100，则将分配 200 字节用作任务
  堆栈。再举一例，如果堆栈宽度为 32 位，uxStackDepth 为 400，
  则将分配 1600 字节用作任务堆栈。堆栈深度与堆栈宽度的乘积不得超过
  size_t 类型变量所能包含的最大值。请参阅 
  常见问题：[堆栈应该多大？](/Why-FreeRTOS/FAQs/Memory-usage-boot-times-context#how-big-should-the-stack-be)。

+ *pvParameters*

  作为参数传递给所创建任务的值。如果 pvParameters 设置为某变量的地址，
  则在创建的任务执行时，该变量必须仍然存在，
  因此，不能传递堆栈变量的地址。

+ *uxPriority*

  创建的任务将以该指定[优先级](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities)执行。支持 MPU 的系统
  可以通过在 uxPriority 中设置 portPRIVILEGE_BIT 位来选择以特权（系统）模式创建任务。
  例如，要创建优先级为 2 的特权任务，请将 uxPriority 设置为 ( 2 | portPRIVILEGE_BIT )。应断言优先级
  低于 configMAX_PRIORITIES。如果 configASSERT 未定义，则优先级默认上限为
  (configMAX_PRIORITIES - 1)。

+ *pxCreatedTask*

  用于将句柄传递至由 xTaskCreate() 函数创建的任务。pxCreatedTask 是可选参数，
  可设置为 NULL。


**返回：**

+ 如果任务创建成功，则返回 pdPASS，
+ 否则返回 errCOULD_NOT_ALLOCATE_REQUIRED_MEMORY。


**用法示例：**

```c
/* Task to be created. */
void vTaskCode( void * pvParameters )
{
    /* The parameter value is expected to be 1 as 1 is passed in the
       pvParameters value in the call to xTaskCreate() below. */

    configASSERT( ( ( uint32_t ) pvParameters ) == 1 );

    for( ;; )
    {
        /* Task code goes here. */
    }
}

/* Function that creates a task. */
void vOtherFunction( void )
{
    BaseType_t xReturned;
    TaskHandle_t xHandle = NULL;

    /* Create the task, storing the handle. */
    xReturned = xTaskCreate(
                    vTaskCode,       /* Function that implements the task. */
                    "NAME",          /* Text name for the task. */
                    STACK_SIZE,      /* Stack size in words, not bytes. */
                    ( void * ) 1,    /* Parameter passed into the task. */
                    tskIDLE_PRIORITY,/* Priority at which the task is created. */
                    &xHandle );      /* Used to pass out the created task's handle. */

    if( xReturned == pdPASS )
    {
        /* The task was created. Use the task's handle to delete the task. */
        vTaskDelete( xHandle );
    }
}
```
