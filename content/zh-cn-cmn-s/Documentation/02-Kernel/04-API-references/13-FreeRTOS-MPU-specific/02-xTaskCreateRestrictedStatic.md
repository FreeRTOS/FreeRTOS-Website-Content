---
title: xTaskCreateRestrictedStatic
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-MPU 特定](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/00-FreeRTOS-MPU-specific)]

task. h

```c
BaseType_t xTaskCreateRestrictedStatic( TaskParameters_t *pxTaskDefinition,
                                        TaskHandle_t *pxCreatedTask );
```

创建一个新的内存保护单元 (MPU) 受限任务并将其添加到准备运行的任务列表中。
[configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation) 必须
在 `FreeRTOSConfig.h` 中设置为 1，该 RTOS API 函数才可用。

在内部，在 FreeRTOS 实现中，每个任务需要两个内存块。第一个内存块
用于保存任务的数据结构体。第二个内存块用作任务的堆栈。如果
使用 xTaskCreateRestricted() 创建了任务，则任务堆栈的内存由应用程序编写者提供，并且
任务数据结构体所需内存会自动从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)分配。如果
使用 xTaskCreateRestrictedStatic() 创建了任务，那么应用程序写入器也必须为任务的数据结构体提供内存。
因此，xTaskCreateRestrictedStatic() 允许在不使用任何动态内存分配的情况下
创建受内存保护的任务。

xTaskCreateRestrictedStatic() 适用于 [FreeRTOS-MPU](/Security/04-FreeRTOS-MPU-memory-protection-unit)，
该[演示应用程序](/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos)包含
有关如何使用相似函数 xTaskCreateRestricted() 的全面和记录示例。


**参数：**

* *pxTaskDefinition*

  指向定义任务的结构体的指针。本页描述了该结构体。

* *pxCreatedTask*

  用于传回可以引用所创建任务的句柄。


**返回：**

如果任务已成功创建并添加到就绪列表中，则为 pdPASS，否则为 projdefs.h 文件中定义的错误代码


相较不包含 MPU 支持的任务，包含它的任务需要更多参数进行创建。将每个参数单独传递给
xTaskCreateRestrictedStatic() 并不明智，因此使用结构体 TaskParameters_t，
以允许在编译时静态配置参数。该结构体在 task.h 中定义为：


---

```c
typedef struct xTASK_PARAMETERS
{
    TaskFunction_t pvTaskCode;
    const char * const pcName;
    unsigned short usStackDepth;
    void *pvParameters;
    UBaseType_t uxPriority;
    portSTACK_TYPE *puxStackBuffer;
    MemoryRegion_t xRegions[ portNUM_CONFIGURABLE_REGIONS ];
    #if ( ( portUSING_MPU_WRAPPERS == 1 ) && ( configSUPPORT_STATIC_ALLOCATION == 1 ) )
        StaticTask_t * const pxTaskBuffer;
    #endif
} TaskParameters_t;
```

……其中 MemoryRegion_t 定义为：

```c
typedef struct xMEMORY_REGION
{
    void *pvBaseAddress;
    unsigned long ulLengthInBytes;
    unsigned long ulParameters;
} MemoryRegion_t;
```

如下是对每个结构体成员的描述：


* pvTaskCode 到 uxPriority

  这些成员与发送到 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate)的同名参数完全相同。
  特别是，uxPriority 用来设置任务的优先级，以及将执行任务的模式。
  例如，如需创建优先级为 2 的用户模式任务，只需将 uxPriority 设置为 2；如需创建优先级为 2 的特权模式任务，
  则需将 uxPriority 设置为 ( 2 | portPRIVILEGE_BIT )。

* puxStackBuffer

  每次有任务切入时，都会重新动态配置 MPU，以定义一个区域，为任务提供
  对自身堆栈的读写访问权限。
  MPU 区域必须满足许多约束，特别是
  所有这些区域的尺寸和对齐必须等于两个值的同底数幂。

  每次创建任务时，标准 FreeRTOS 移植都使用 pvPortMalloc() 分配新的堆栈。可以提供
  pvPortMalloc() 实现，以满足 MPU 数据对齐要求，但
  也将导致使用 RAM 的复杂性和低效率。为消除这种复杂需求，FreeRTOS-MPU
  允许在编译时静态声明堆栈。这允许使用编译器扩展托管对齐，
  以及由链接器托管 RAM 使用效率。例如，如果使用 GCC，
  可以使用以下代码声明并正确对齐堆栈：

  ```c
  char cTaskStack[ 1024 ] __attribute__((aligned(1024));
  ```

  puxStackBuffer 通常设置为静态声明的堆栈的地址。作为替代方案
  puxStackBuffer 可以设置为 NULL——在这种情况下，将调用 pvPortMallocAligned() 来分配任务
  堆栈，且应用程序编写者有责任提供
  符合 MPU的对齐要求的 pvPortMallocAligned() 实现。

* xRegions

  xRegions 是 MemoryRegion_t 结构体的数组，每个结构体定义一个单个用户可定义的
  内存区域，以供正在创建的任务使用。ARM Cortex-M3 FreeRTOS-MPU 移植将
  portNUM_CONFIGURABLE_REGIONS 定义为 3。

  PvBaseAddress 和 ulLengthInBytes 成员分别自行解释为
  内存区域的开始和内存区域的长度。ulParameters 定义了
  访问内存区域的方法，并且可以采用以下值中的按位 OR：

  ```c
    portMPU_REGION_READ_WRITE
    portMPU_REGION_PRIVILEGED_READ_ONLY
    portMPU_REGION_READ_ONLY
    portMPU_REGION_PRIVILEGED_READ_WRITE
    portMPU_REGION_CACHEABLE_BUFFERABLE
    portMPU_REGION_EXECUTE_NEVER
  ```

* pxTaskBuffer

  必须指向 `StaticTask_t` 类型的变量。该变量将用于保留新任务的
  数据结构体，因此必须是永久性的（而不是在函数的堆栈中声明）。


**用法示例：**

```c
/* Create an TaskParameters_t structure that defines the task to be created.
 * The StaticTask_t variable is only included in the structure when
 * configSUPPORT_STATIC_ALLOCATION is set to 1. The PRIVILEGED_DATA macro can
 * be used to force the variable into the RTOS kernel's privileged data area. */
static PRIVILEGED_DATA StaticTask_t xTaskBuffer;
static const TaskParameters_t xCheckTaskParameters =
{
    vATask,     /* pvTaskCode - the function that implements the task. */
    "ATask",    /* pcName - just a text name for the task to assist debugging. */
    100,        /* usStackDepth - the stack size DEFINED IN WORDS. */
    NULL,       /* pvParameters - passed into the task function as the function parameters. */
    ( 1UL | portPRIVILEGE_BIT ), /* uxPriority - task priority, set the portPRIVILEGE_BIT
                                    if the task should run in a privileged state. */
    cStackBuffer, /* puxStackBuffer - the buffer to be used as the task stack. */

    /* xRegions - Allocate up to three separate memory regions for access by
     * the task, with appropriate access permissions. Different processors have
     * different memory alignment requirements - refer to the FreeRTOS documentation
     * for full information. */
    {
        /* Base address Length Parameters */
        { cReadWriteArray,              32,     portMPU_REGION_READ_WRITE },
        { cReadOnlyArray,               32,     portMPU_REGION_READ_ONLY },
        { cPrivilegedOnlyAccessArray,   128,    portMPU_REGION_PRIVILEGED_READ_WRITE }
    }

    &xTaskBuffer; /* Holds the task's data structure. */
};

 int main( void )
 {
 TaskHandle_t xHandle;

    /* Create a task from the const structure defined above. The task handle
     * is requested (the second parameter is not NULL) but in this case just for
     * demonstration purposes as its not actually used. */
    xTaskCreateRestricted( &xRegTest1Parameters, &xHandle );

    /* Start the scheduler. */
    vTaskStartScheduler();

    /* Will only get here if there was insufficient memory to create the idle
     * and/or timer task. */
    for( ;; );
}
```
