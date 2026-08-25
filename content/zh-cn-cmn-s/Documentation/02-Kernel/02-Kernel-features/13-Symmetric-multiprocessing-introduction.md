---
title: "FreeRTOS 的对称多处理 (SMP)"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 'FreeRTOS 的对称多处理 (SMP) 相关信息 '
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---

[FreeRTOS 内核中的 SMP 支持](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/smp)使得 
FreeRTOS 内核的实例可以在多个相同的处理器核心中调度任务。 
这些内核架构必须相同，并共享相同的内存。

## FreeRTOS 和 SMP 入门指南

最简单的入门方法是使用以下预配置
的示例项目之一：

* [XCORE AI](/Documentation/02-Kernel/03-Supported-devices/04-Demos/XMOS/smp-demo-for-xmos-xcore-ai-explorer-board)
* [Raspberry Pi Pico](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Raspberry-Pi/smp-demos-for-the-raspberry-pi-pico-board)


## 修改应用程序以使用 FreeRTOS SMP 功能

FreeRTOS API 单核版本和 SMP 版本之间基本相同，区别之处只有 
[这些额外功能](#smp-特定-api)。因此，为 FreeRTOS 单核版本编写的应用程序
应只需极少修改或无需修改就能用于编译 SMP 版本。但是，
一些适用于单核应用的假设可能不适用于多核应用，
因此可能会存在一些功能问题。

其中一个常见的假定是，在较高优先级的任务正在运行时，
较低优先级的任务无法运行。虽然这在单核上是正确的，但并不适用于多核，
因为多个任务可以
同时运行。如果应用程序依赖于相对任务优先级来提供
相互排斥，则可能在多核环境中观察到意想不到的结果。
应用程序编写者有以下几个选择来解决这一问题：

1. 最好的选择是更新应用程序，使其不依赖于任务优先级，
   而是使用同步基元。

2. 另一个选择是
   使用 `vTaskCoreAffinitySet` API 将所有不能同时运行的任务固定到一个核心。

3. 另一个选择是将 `configRUN_MULTIPLE_PRIORITIES` 定义为 `0`，
   这样可确保多个任务只有在具有相同优先级时
   才会同时运行。请注意，这可能会导致利用率不足，
   并使一些内核在可用于运行其他低优先级任务时处于空闲状态。

另一个常见的假定是， ISR 不能彼此或与其他任务同时运行。 
这在多核环境中不再适用，应用程序编写者 
需要在访问任务和 ISR 之间共享的数据时确保适当的互斥。可以在 ISR 中 `taskENTER_CRITICAL_FROM_ISR()` 
使用宏和 `taskEXIT_CRITICAL_FROM_ISR()`，而宏 `taskENTER_CRITICAL()` 
和 `taskEXIT_CRITICAL()` 可以在任务中使用，以提供这种互斥。


## SMP 特定 API

以下附加 API 可用于 FreeRTOS-SMP 内核：

* [vTaskCoreAffinitySet](#vtaskcoreaffinityset)
* [vTaskCoreAffinityGet](#vtaskcoreaffinityget)
* [vTaskPreemptionDisable](#vtaskpreemptiondisable)
* [vTaskPreemptionEnable](#vtaskpreemptionenable)


### vTaskCoreAffinitySet

```c
void vTaskCoreAffinitySet( const TaskHandle_t xTask, UBaseType_t uxCoreAffinityMask ); 
```

`configUSE_CORE_AFFINITY` 必须定义为 `1` 才可使用此函数。

设置任务的内核关联掩码，即可以运行任务的内核。

**参数：**

* `xTask`：内核关联掩码所针对的任务的句柄。传递此参数 `NULL`
  将设置调用任务的内核关联掩码。

* `uxCoreAffinityMask`：一个按位值，指示可以
  运行任务的内核。内核的编号范围为 `0` 到 `configNUM_CORES - 1`。例如，为确保任务
  可以在内核 `0` 和内核 `1` 上运行，需要将 `uxCoreAffinityMask` 设置为 `0x03`。


**用法示例：**

```c
/* The function that creates task. */  
void vAFunction( void )  
{  
TaskHandle_t xHandle;  
UBaseType_t uxCoreAffinityMask;  

    /* Create a task, storing the handle. */  
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &( xHandle ) );  

    /* Define the core affinity mask such that this task can only run on core 0  
     * and core 2. */  
    uxCoreAffinityMask = ( ( 1 << 0 ) | ( 1 << 2 ) );  

    /* Set the core affinity mask for the task. */  
    vTaskCoreAffinitySet( xHandle, uxCoreAffinityMask );  
}  
```


### vTaskCoreAffinityGet

```c
UBaseType_t vTaskCoreAffinityGet( const TaskHandle_t xTask ); 
```

`configUSE_CORE_AFFINITY` 必须定义为 `1` 才可使用此函数。

设置任务的内核关联掩码，即可以运行任务的内核。


**参数：**

* `xTask`：内核关联掩码所针对的任务的句柄。传递此参数 `NULL`
  将获取调用任务的内核关联掩码。


**返回：**

* 内核关联掩码，指示可以
  运行任务的内核的按位值。内核的编号范围为 `0` 到 `configNUM_CORES - 1`。
  例如，如果任务可以在内核 `0` 和内核 `1` 上运行，则内核关联掩码
  为 `0x03`。


**用法示例：**

```c 
/* Task handle of the networking task - it is populated elsewhere. */  
TaskHandle_t xNetworkingTaskHandle;  

void vAFunction( void )  
{  
TaskHandle_t xHandle;  
UBaseType_t uxNetworkingCoreAffinityMask;  

    /* Create a task, storing the handle. */  
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &( xHandle ) );  

    /* Get the core affinity mask for the networking task. */  
    uxNetworkingCoreAffinityMask = vTaskCoreAffinityGet( xNetworkingTaskHandle );  

    /* Here is a hypothetical scenario, just for the example. Assume that we  
     * have 2 cores - Core 0 and core 1. We want to pin the application task to  
     * the core that is not the networking task core to ensure that the  
     * application task does not interfere with networking. */  
    if( ( uxNetworkingCoreAffinityMask & ( 1 << 0 ) ) != 0 )  
    {  
        /* The networking task can run on core 0, pin our task to core 1. */  
        vTaskCoreAffinitySet( xHandle, ( 1 << 1 ) );  
    }  
    else  
    {  
        /* Otherwise, pin our task to core 0. */  
        vTaskCoreAffinitySet( xHandle, ( 1 << 0 ) );  
    }  
}  
```


### vTaskPreemptionDisable

```c
void vTaskPreemptionDisable( const TaskHandle_t xTask ); 
```

`configUSE_TASK_PREEMPTION_DISABLE` 必须定义为 `1` 才可使用此函数。

禁用任务抢占。


**参数：**

* `xTask`：禁用抢占功能的任务的句柄。传递此参数
  `NULL` 将禁用调用任务的抢占功能。


**用法示例：**

```c
void vTaskCode( void *pvParameters )  
{  
    /* Silence warnings about unused parameters. */  
    ( void ) pvParameters;  

    for( ;; )  
    {  
        /* ... Perform some function here. */  

        /* Disable preemption for this task. */  
        vTaskPreemptionDisable( NULL );  

        /* The task will not be preempted when it is executing in this portion ... */  

        /* ... until the preemption is enabled again. */  

        vTaskPreemptionEnable( NULL );  

        /* The task can be preempted when it is executing in this portion. */  
    }  
}  
```


### vTaskPreemptionEnable

```c
void vTaskPreemptionEnable( const TaskHandle_t xTask ); 
```

`configUSE_TASK_PREEMPTION_DISABLE` 必须定义为 `1` 才可使用此函数。

启用任务抢占。


**参数：**

* `xTask`：启用抢占功能的任务的句柄。传递此参数
  `NULL` 将启用调用任务的抢占功能。


**用法示例：**

```c
void vTaskCode( void *pvParameters )  
{  
    /* Silence warnings about unused parameters. */  
    ( void ) pvParameters;  

    for( ;; )  
    {  
        /* ... Perform some function here. */  

        /* Disable preemption for this task. */  
        vTaskPreemptionDisable( NULL );  

        /* The task will not be preempted when it is executing in this portion ... */  

        /* ... until the preemption is enabled again. */  
        vTaskPreemptionEnable( NULL );  

        /* The task can be preempted when it is executing in this portion. */  
    }  
}  
```


## SMP 特定钩子函数

### 空闲钩子函数

FreeRTOS SMP 内核有两种类型的闲置任务：

1. 空闲任务：单核 FreeRTOS 应用程序中使用的标准空闲任务。

2. 最小空闲任务：`configNUM_CORES - 1` 最小空闲任务，
   在空闲内核上运行，不执行任何操作。

最小空闲任务可以选择性地调用应用程序定义的钩子
（或回调）函数，即最小空闲钩子。最小空闲任务以最低优先级运行，
只有在无较高优先级任务运行时，
这种空闲钩子函数才会运行。

只有 `configUSE_MINIMAL_IDLE_HOOK`
在 `FreeRTOSConfig.h` 内设置为 `1` 时才会调用最小空闲钩子函数。设置后，应用程序必须为钩子函数
提供以下原型：

```c
void vApplicationMinimalIdleHook( void ); 
```

只要最小空闲任务中的任何一个正在运行，
最小空闲任务就会重复调用最小空闲钩子函数。**最重要的是，最小空闲钩子
函数不调用任何可能导致其阻塞的 API 函数。**


## SMP 特定配置选项

以下附加配置选项可用于 FreeRTOS-SMP 内核：

* [configNUM_CORES](#confignum_cores)
* [configRUN_MULTIPLE_PRIORITIES](#configrun_multiple_priorities)
* [configUSE_CORE_AFFINITY](#configuse_core_affinity)
* [configUSE_TASK_PREEMPTION_DISABLE](#configuse_task_preemption_disable)


#### configNUM_CORES

设置可用的处理器内核数。


#### configRUN_MULTIPLE_PRIORITIES

在单核 FreeRTOS 应用程序中，
如果存在能够运行的较高优先级任务，则较低优先级任务永远不会运行。在 SMP FreeRTOS应用程序中，
RTOS 内核将运行与可用内核数量一样多的任务，在一个内核上运行优先级较低的任务的同时，
较高优先级的任务可能同时
在另一个内核上运行。如果您的应用程序或库
为单核环境编写，并且因此对任务执行的顺序做出假设，
这可能会导致问题。因此，提供 configRUN_MULTIPLE_PRIORITIES 来
控制此行为。

如果 `configRUN_MULTIPLE_PRIORITIES`定义为 `0`， 
只有具有相同优先级的多个任务才能同时运行，
保持这样的范例：如果存在能够运行的较高优先级任务，则较低优先级任务永远不会运行。 
如果 `configRUN_MULTIPLE_PRIORITIES`定义为 `1`， 
则具有不同优先级的多个任务可以同时运行，因此，较高和较低优先级的任务可以同时
在不同的内核上运行。


#### configUSE_CORE_AFFINITY

让应用程序编写者可以控制任务在哪些内核上运行。
如果 `configUSE_CORE_AFFINITY` 定义为 `1`，`vTaskCoreAffinitySet` 
可用于控制任务可以在哪些内核上运行，而 `vTaskCoreAffinityGet` 可 
用于查询任务可以在哪些内核上运行。如果 `configUSE_CORE_AFFINITY`为 0，
则 FreeRTOS 调度器可以在任何可用内核上自由运行任何任务。


#### configUSE_TASK_PREEMPTION_DISABLE

在单核 FreeRTOS 应用程序中，可以将 FreeRTOS 调度器配置为
抢占式或协作式。请参阅 configUSE_PREEMPTION 的定义。
在 SMP FreeRTOS 应用程序中，如果 `configUSE_TASK_PREEMPTION_DISABLE`定义为 `1`，
则可使用 `vTaskPreemptionDisable`
和 `vTaskPreemptionEnable` API 函数将单个任务设置为抢占或协同模式。
