---
title: xTaskCreateRestricted
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
BaseType_t xTaskCreateRestricted(
                            TaskParameters_t *pxTaskDefinition,
                            TaskHandle_t *pxCreatedTask );
```

创建一个新的内存保护单元 (MPU) 受限任务并将其添加到准备运行的任务列表中。

xTaskCreateRestricted() 适用于 [FreeRTOS-MPU](/Security/04-FreeRTOS-MPU-memory-protection-unit)，
其[演示应用程序](/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos)包含
使用 xTaskCreateRestricted() 的全面且有记录的示例。


**参数：**

* *pxTaskDefinition*

  指向定义任务的结构体的指针。本页描述了该结构体。

* *pxCreatedTask*

  用于传回可以引用所创建任务的句柄。


**返回：**

如果任务已成功创建并添加到就绪列表中，则为 pdPASS，否则为 projdefs.h 文件中定义的错误代码

相较不包含 MPU 支持的任务，包含它的任务需要更多参数进行创建。将每个参数单独传递给
xTaskCreateRestricted () 不明智，因此使用结构体 TaskParameters_t，
以便允许在编译时静态配置这些参数。该结构体在 task.h 中定义为：

---

```c
typedef struct xTASK_PARAMETERS
{
    TaskFunction_t pvTaskCode;
    const signed char * const pcName;
    unsigned short usStackDepth;
    void *pvParameters;
    UBaseType_t uxPriority;
    portSTACK_TYPE *puxStackBuffer;
    MemoryRegion_t xRegions[ portNUM_CONFIGURABLE_REGIONS ];
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

---

如下是对每个结构体成员的描述：

* pvTaskCode 到 uxPriority

  这些成员与 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 的同名参数完全相同。
  特别是，uxPriority 用来设置任务的优先级，以及将执行任务的模式。
  例如，如需创建优先级为 2 的用户模式任务，只需将 uxPriority 设置为 2；如需创建优先级为 2 的特权模式任务，
  则需将 uxPriority 设置为 ( 2 | portPRIVILEGE_BIT )。

* puxStackBuffer

  每次在 MPU 中切换任务时，它都会动态重新配置以定在其自身堆栈上义提供任务
  读写访问权限的区域。
  MPU 区域必须满足许多约束——特别是
  每个区域的尺寸和对齐，必须均等于两个值的相同幂函数。

  每次创建任务时，标准 FreeRTOS 端口都使用 pvPortMalloc () 分配新堆栈。可以提供
  pvPortMalloc() 实现，以满足 MPU 数据对齐要求，但
  也将导致使用 RAM 的复杂性和低效率。为消除这种复杂需求，FreeRTOS-MPU
  允许在编译时静态声明堆栈。这允许使用编译器扩展托管对齐，
  扩展和 RAM 使用效率。例如，如果使用 GCC，
  可以使用以下代码声明并正确对齐堆栈：

  ```c
  char cTaskStack[ 1024 ] __attribute__((aligned(1024));
  ```

  puxStackBuffer 通常设置为静态声明的堆栈的地址。作为替代方案
  可以将 puxStackBuffer 设置为 NULL——在这种情况下，将调用 pvPortMallocAligned () 来分配任务
  堆栈，并且提供
  符合 MPU的对齐要求的 pvPortMallocAligned () 实现是应用程序编写者的责任。

* xMemoryRegions

  xRegions 是 MemoryRegion_t 结构体的数组，每个结构体定义正在创建的任务使用的单个用户可定义
  内存区域，以供正在创建的任务使用。ARM Cortex-M3 FreeRTOS-MPU 移植将
  portNUM_CONFIGURABLE_REGIONS 定义为 3。

  PvBaseAddress 和 ulLengthInBytes 成员分别自行解释为
  内存区域的开始和内存区域的长度。ulParameters 定义了
  如何可以访问内存区域，并且可以采用以下值中的按位 OR：

  ```c
  portMPU_REGION_READ_WRITE
  portMPU_REGION_PRIVILEGED_READ_ONLY
  portMPU_REGION_READ_ONLY
  portMPU_REGION_PRIVILEGED_READ_WRITE
  portMPU_REGION_CACHEABLE_BUFFERABLE
  portMPU_REGION_EXECUTE_NEVER
  ```

---

使用示例（请参阅 FreeRTOS-MPU [ 演示应用程序](/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos)
了解更完整、更全面的示例）：

```c
/* Declare the stack that will be used by the task. The stack alignment must
   match its size and be a power of 2, so if 128 words are reserved for the stack
   then it must be aligned to ( 128 * 4 ) bytes. This example used GCC syntax. */
static portSTACK_TYPE xTaskStack[ 128 ] __attribute__((aligned(128*4)));

/* Declare an array that will be accessed by the task. The task should only
   be able to read from the array, and not write to it. */
char cReadOnlyArray[ 512 ] __attribute__((aligned(512)));

/* Fill in a TaskParameters_t structure to define the task - this is the
   structure passed to the xTaskCreateRestricted() function. */
static const TaskParameters_t xTaskDefinition =
{
    vTaskFunction, /* pvTaskCode */
    "A task", /* pcName */
    128, /* usStackDepth - defined in words, not bytes. */
    NULL, /* pvParameters */
    1, /* uxPriority - priority 1, start in User mode. */
    xTaskStack, /* puxStackBuffer - the array to use as the task stack. */

    /* xRegions - In this case only one of the three user definable regions is
       actually used. The parameters are used to set the region to read only. */
    {
        /* Base address Length Parameters */
        { cReadOnlyArray, mainREAD_ONLY_ALIGN_SIZE, portMPU_REGION_READ_ONLY },
        { 0, 0, 0 },
        { 0, 0, 0 },
    }
};

void main( void )
{
    /* Create the task defined by xTaskDefinition. NULL is used as the second
       parameter as a task handle is not required. */
    xTaskCreateRestricted( &xTaskDefinition, NULL );

    /* Start the RTOS scheduler. */
    vTaskStartScheduler();

    /* Should not reach here! */
}
```
