---
title: 在 ARM Cortex-A9 嵌入式处理器上使用 FreeRTOS
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**其中包括一个通用中断控制器 (GIC)**


## 引言

本页信息适用于 32 位 ARMv7-A 和 64 位 ARMv8-A RTOS 移植。

有的 ARM Cortex-A 处理器集成了 ARM 自带的通用中断控制器 (GIC)，而其他处理器 
则采用专有中断控制器。有关 
这两种情况下 RTOS 的使用说明，另有专门网页进行介绍。本页信息介绍如何在使用 ARM GIC 的 ARM Cortex-A 嵌入式处理器上运行 RTOS 
。另请参阅 
介绍[在使用专有中断控制器的 ARM Cortex-A 嵌入式处理器上运行 RTOS](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller.md) 的网页。

## FreeRTOS ARM Cortex-A 内核移植的功能

FreeRTOS ARM Cortex-A 移植：

* 将广为熟知、体积小巧、简单易用、确定性强的实际标准 FreeRTOS 内核的使用范围 
  扩展到微控制器市场之外
* 实现了完整的中断嵌套模型
* 允许中断子集保持启用状态，即使在 RTOS 临界区内也是如此[^1]
* 包括硬件浮点支持
* 使用平面/线性内存模型（不支持 MMU ）。

[^1]: The ARM Cortex-A 硬件会在发生中断时自行全局禁用中断， 
并规定在执行某些操作时全局禁用中断 。 此时
是唯一全局禁用中断的时候，并且中断总是会尽快 
重新启用。


## 在中断中使用浮点单元 (FPU)

默认情况下，Cortex-A9 移植不支持在中断中使用浮点单元。如果 
必须在中断中使用浮点单元，则还需要 
在进入每个（可能嵌套的）中断时将整个浮点上下文保存到堆栈。自 
FreeRTOS V9.0.0 开始，FreeRTOS GCC Cortex-A 移植可以自动执行此操作，请参阅 
下文[中断处理](#中断处理)部分中关于 vApplicationFPUSafeIRQHandler() 回调函数的 
描述。


## 在任务中使用浮点单元 (FPU)

为防止处理器寄存器损坏，任务只能在具有浮点上下文的情况下 
才能使用浮点寄存器。默认情况下，RTOS 任务是否以浮点上下文创建， 
取决于使用的编译器，以及 FreeRTOSConfig.h 中的 configUSE_TASK_FPU_SUPPORT 设置。

在下列情况下，新建任务将不含浮点上下文：

* 使用的 FreeRTOS 版本低于 V9.0.0；****
* 使用的编译器不是 GCC；****
* configUSE_TASK_FPU_SUPPORT 在 FreeRTOSConfig.h 中设置为 1；****
* configUSE_TASK_FPU_SUPPORT 未定义。

在下列情况下，新建任务将含有浮点上下文：

* 使用 FreeRTOS V9.0.0 **或** 更高版本；****
* 使用 GCC 编译器；****
* configUSE_TASK_FPU_SUPPORT 在 FreeRTOSConfig.h 中设置为 2。

没有浮点上下文的任务必须在执行浮点计算之前，
通过调用 portTASK_USES_FLOATING_POINT() 为自己创建浮点上下文
。每项任务只需要调用一次
portTASK_USES_FLOATING_POINT()。例如：

```c
void vATaskFunction( void *pvParameters )  
{  
double x, y;  

    /* This task is going to use floating point operations. Therefore it calls  
       portTASK_USES_FLOATING_POINT() once on task entry, before entering the loop  
       that implements its functionality. From this point on the task has a floating  
       point context. */  
    portTASK_USES_FLOATING_POINT();  

    /* Enter the loop that implements the task's function. */  
    for( ;; )  
    {  
        /* portTASK_USES_FLOATING_POINT() has already been called, so it is safe  
           to use the floating point x and y variables here... */  
        x = [whatever];  
        y = [whatever];  
    }  
}  
```
*在执行浮点计算之前调用 portTASK_USES_FLOATING_POINT()*


## 针对 GCC（可能还有其他编译器）用户的重要提示：

一些 GCC 库通过利用宽浮点寄存器
来优化内存拷贝和内存集（可能还有其他）函数。因此，默认情况下，
**任何**使用 memcpy()、memcmp() 或 memset() 等函数的任务
或使用 FreeRTOS API 函数（例如 xQueueSend()，而该函数本身使用 memcpy()）的任务
都会在无意中破坏浮点寄存器。此外，**任何**
调用 FreeRTOS 队列或信号量函数的中断也会
因使用 memcpy() 而破坏浮点上下文。

要避免这种情况，可以选择以下任何一种方法：

* 利用不使用浮点寄存器的库函数，
  如果无法实现，提供自己的 memcpy()、memcmp() 和 memset() 实现，
  以确保不使用库提供的版本。

* 使用本页所述的 portTASK_USES_FLOATING_POINT() 和 vApplicationFPUSafeIRQHandler()
  函数。


## 关于中断优先级的基本信息

RTOS Cortex-A 移植实现了完整的中断嵌套方案，
其行为取决于 configMAX_API_CALL_INTERRUPT_PRIORITY 设置。
configMAX_API_CALL_INTERRUPT_PRIORITY [必须在 FreeRTOSConfig.h 中定义](#arm-cortex-a-特定的-freertosconfigh-设置)。

如果被分配的优先级等于或低于 configMAX_API_CALL_INTERRUPT_PRIORITY 设置的优先级，
则中断可以调用中断安全 FreeRTOS API 函数，并进行嵌套。中断安全
FreeRTOS API 函数是指以 "FromISR" 结尾的函数（FreeRTOS 维护单独的
中断 API，以确保尽可能高效、简单地进入中断）。

如果被分配的优先级高于 configMAX_API_CALL_INTERRUPT_PRIORITY 设置的优先级，
则中断不会受到 RTOS 临界区的影响，并且会进行嵌套，**但无法调用
 FreeRTOS API 函数**。

**特别说明 1：**在 ARM 中断控制器中，
中断优先级数值越高，逻辑中断优先级越低。因此，
中断优先级 5 低于中断优先级 4。
如果 configMAX_API_CALL_INTERRUPT_PRIORITY 设置为 5，
则为调用中断安全 API 函数的中断处理程序分配优先级 5 或 6 是正确做法，
为其分配优先级 4 是**错误做法**。

**特别说明 2：**可以忽略
中断控制器的优先级位内部表示。如果中断控制器
实现了 32 个唯一优先级，
则 configMAX_API_CALL_INTERRUPT_PRIORITY 的唯一有效值是 1 到 30。同样，如果中断
控制器实现了 16 个唯一优先级，则有效值为 1 到 14。

**特别说明 3：**如果中断控制器
可以将中断优先级位细分为抢占式优先级和子优先级，
则应将所有位配置为抢占式优先级。在 ARM 通用
中断控制器 (GIC) 中，这意味着中断控制器的二进制点寄存器
必须设置为 0。


## ARM Cortex-A 特定的 FreeRTOSConfig.h 设置

FreeRTOSConfig.h 中必须包含以下设置：

* configINTERRUPT_CONTROLLER_BASE_ADDRESS

  必须设置为 ARM 通用中断控制器 (GIC) 的基地址

* configINTERRUPT_CONTROLLER_CPU_INTERFACE_OFFSET

  GIC 的 CPU 接口从 configINTERRUPT_CONTROLLER_BASE_ADDRESS 开始的
  偏移量。通常为 0x1000。

* configUNIQUE_INTERRUPT_PRIORITIES

  可以在 GIC 中指定的唯一优先级数量。

* configMAX_API_CALL_INTERRUPT_PRIORITY

  请参阅[中断优先级](#关于中断优先级的基本信息)部分。

**注意：**如果您使用的 Cortex-A9 处理器有官方演示，
则演示提供的 FreeRTOSConfig.h 文件已经包含正确的设置。


## 配置和安装 RTOS 滴答中断

所有针对基于 ARM Cortex-A 的嵌入式处理器的官方 FreeRTOS 演示
都包含用于配置定时器以生成 RTOS 滴答中断的代码，以及安装
FreeRTOS 滴答中断处理程序的代码。仅当需要更改提供的实现时
才需要以下信息。

宏 configSETUP_TICK_INTERRUPT() 由 RTOS 内核移植层调用。
必须在 FreeRTOSConfig.h 中定义 configSETUP_TICK_INTERRUPT()，
以配置外围设备，使其
按 configTICK_RATE_HZ FreeRTOSConfig.h 设置的频率生成周期性中断。然后必须安装 FreeRTOS_Tick_Handler()
作为中断的处理程序函数。例如：


```c
/* Implement a function in a C file to generate a periodic interrupt at the  
   required frequency. */  
void vSetupTickInterrupt( void )  
{  
/* FreeRTOS_Tick_Handler() is itself defined in the RTOS port layer. An extern  
   declaration is required to allow the following code to compile. */  
extern void FreeRTOS_Tick_Handler( void );  

    /* Assume TIMER1_configure() configures a hypothetical timer peripheral called  
    TIMER1 to generate a periodic interrupt with a frequency set by its parameter. */  
    TIMER1_configure( configTICK_RATE_HZ );  

    /* Next assume Install_Interrupt() installs the function passed as its second  
       parameter as the handler for the peripheral passed as its first parameter. */  
    Install_Interrupt( TIMER1, FreeRTOS_Tick_Handler );  
}  
```
*定义配置定时器以生成周期性滴答的函数*


```c
/* Given the function definition above, add the following line to FreeRTOSConfig.h. */  
#define configSETUP_TICK_INTERRUPT() vSetupTickInterrupt()  
#defining configSETUP_TICK_INTERRUPT() to the function that generates the periodic tick  
```

## 中断处理

所有针对基于 ARM Cortex-A 的嵌入式处理器的官方 FreeRTOS 演示
都包含处理中断的代码。仅当需要更改提供的实现时
才需要以下信息。

中断进入、嵌套和退出代码由 RTOS 内核移植层提供。
进入中断后，RTOS 移植层会执行回调函数，
该函数必须由应用程序编写者提供。然后即可
通过回调函数调用各个中断服务程序。请参阅[以下](#中断处理)示例。

回调函数可以称为 vApplicationIRQHandler()，
在 GCC 和 FreeRTOS V9.0.0 或更高版本中，也可以称为 vApplicationFPUSafeIRQHandler()。

```c
/* The two callback function options. In both cases ulICCIAR is passed as the value  
   of the interrupt controller's ICCIAR (interrupt acknowledge register). */  
void vApplicationIRQHandler( uint32_t ulICCIAR );  
void vApplicationFPUSafeIRQHandler( uint32_t ulICCIAR );  
```

如果应用程序编写者提供的回调函数名为 vApplicationIRQHandler()，
则在进入中断时不会保存浮点寄存器，
并且中断不得使用任何浮点指令或寄存器。如果
应用程序编写者提供的回调函数名为
vApplicationFPUSafeIRQHandler()，
则在每次进入（可能嵌套的）中断时将保存浮点寄存器，这会使用更多堆栈空间
并减慢中断进入速度，但允许中断处理程序使用 FPU 寄存器。请参阅
上文“[在中断中使用浮点单元 (FPU)](#在中断中使用浮点单元-fpu)”部分。

回调函数（vApplicationIRQHandler() 或 vApplicationFPUSafeIRQHandler()）
在中断禁用的情况下调用，但可以
（并且在大多数情况下应该）启用中断。以下是实现示例：

```c
/* vApplicationIRQHandler() is just a normal C function. */  
void vApplicationIRQHandler( uint32_t ulICCIAR )  
{  
uint32_t ulInterruptID;  

    /* In the 64-bit Cortex-A RTOS port it is necessary to clear the source of  
       the interrupt BEFORE interrupts are re-enabled. */  
    ClearInterruptSource();  

    /* Re-enable interrupts. */  
    __asm volatile( "CPSIE I" );  

    /* The ID of the interrupt can be obtained by bitwise ANDing the ICCIAR value  
       with 0x3FF. */  
    ulInterruptID = ulICCIAR & 0x3FFUL;  

    /* On the assumption that handlers for each interrupt are stored in an array  
       called InterruptHandlerFunctionTable, use the interrupt ID to index to and  
       call the relevant handler function. */  
    InterruptHandlerFunctionTable[ ulInterruptID ]();  
}  
```
*vApplicationIRQHandler() 的实现示例* 


## 安装 FreeRTOS IRQ 和 SWI (SVC) 中断处理程序

必须安装 FreeRTOS_IRQ_Handler()，作为 Cortex-A 的 IRQ 处理程序。

必须安装 FreeRTOS_SWI_Handler()，作为 Cortex-A 的 SWI (SVC) 处理程序。

如果无法编辑中断向量代码，则将 FreeRTOS 处理程序
映射到所需的处理程序名称（使用 FreeRTOSConfig.h 中的宏定义）。例如，
如果安装的处理程序分别名为 IRQ_Handler() 和 SWI_Handler()，
则要将 FreeRTOS 处理程序映射到这些名称，
可向 FreeRTOSConfig.h 中添加以下两行代码。


```c
#define FreeRTOS_IRQ_Handler IRQ_Handler  
#define FreeRTOS_SWI_Handler SWI_Handler  
```
*将 FreeRTOS 中断处理程序名称映射到替代处理程序名称*


## ARMv7A 处理器模式和堆栈

C 启动代码必须至少为 Cortex-A 处理器的 IRQ 和监管器模式配置堆栈。
**main() 必须从特权模式调用，最好是在
监管器模式下**。

除非从系统模式调用 main()（main() 不能从用户模式调用），
否则无需将堆栈分配给用户/系统模式。如果将堆栈
分配给用户/系统模式，则在 RTOS 内核
内核启动后无法使用此堆栈。

RTOS 堆栈溢出检测功能仅检测任务堆栈中的溢出，
而非 IRQ 或监管器堆栈中的溢出。


## ARMv8A 异常等级

目前：

* RTOS 在 EL3（异常等级 3）执行，并使用 EL3 堆栈。
* RTOS 任务在 EL3 执行，并使用 EL1 堆栈。

