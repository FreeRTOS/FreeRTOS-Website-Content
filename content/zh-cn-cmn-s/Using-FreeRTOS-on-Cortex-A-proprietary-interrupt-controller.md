---
title: 在 ARM Cortex-A9 嵌入式处理器上使用 FreeRTOS
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**使用专有中断控制器**

## 引言

有的 ARM Cortex-A 处理器集成了 ARM 自带的通用中断控制器（GIC）， 
而有的则采用专有的中断控制器。我们提供了单独的网页， 
介绍在两个场景中使用 RTOS 的方法。此页面提供有关在未集成 ARM 的自带通用中断控制器（GIC）的 ARM Cortex-A 嵌入式处理器上运行 RTOS 的信息
。另请参阅 
介绍在包含 ARM GIC 的 ARM Cortex-A 嵌入式处理器上[运行 RTOS 的网页](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors)。


### FreeRTOS ARM Cortex-A RTOS 移植的功能

适用于使用专有中断控制器的微处理器的 FreeRTOS ARM Cortex-A 移植：

* 将常见、小型、简单、确定性的实际标准标准 FreeRTOS 内核的使用 
  扩展到微控制器市场之外。

* 支持中断嵌套（需要注意的是，与针对集成了 GIC 的 ARM Cortex-A 处理器的 [RTOS 版本不同](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors)， 
  针对具有专有中断控制器的处理器的版本 
  不会永久启用中断优先级子集，这是因为不会对使用中的中断控制器做出假设） 
  。

* 包括硬件浮点支持。

* 使用平面/线性内存模型（不支持 MMU ）。


### 使用浮点单元 (FPU)

使用硬件浮点单元的任务在执行任何浮点计算之前必须调用 portTASK_USES_FLOATING_POINT()
。每个任务只需要调用一次
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
*在执行任何浮点运算之前调用 portTASK_USES_FLOATING_POINT(）*

需要注意的是，默认情况下， Cortex-A9
移植不支持在中断中使用浮点单元。如果必须在中断中使用浮点单元，
则还需要在进入每个（可能嵌套的）
中断时将整个浮点上下文保存到堆栈。


### ARM Cortex-A 特定的 FreeRTOSConfig.h 设置

以下设置必须包含在 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中。请注意这些设置
专用于使用专有中断控制器的处理器的 ARM Cortex-A RTOS 移植
。使用 ARM GIC 的 ARM Cortex-A 处理器的 RTOS 移植采用不同的设置
，因为他们还配置有 GIC。

* configFPU_D32

  如果 FPU 有 16 个 "d" 寄存器，则将 configFPU_D32 设置为 0。如果 FPU 有 32 个 "d" 寄存器， 
  则将 configFPU_D32 设置为 1。

* configINTERRUPT_VECTOR_ADDRESS

  大多数中断控制器都包含一个寄存器，可从中读取当前断言（执行） 
  中断处理程序的地址。如果存在这样的寄存器，则将 configINTERRUPT_VECTOR_ADDRESS
  设置为其地址。如果不存在这样的寄存器，则将 configINTERRUPT_VECTOR_ADDRESS 
  设置为指向中央中断处理程序的变量的地址。

* configEOI_ADDRESS

  大多数中断控制器都包含一个中断结束（EOI）寄存器， 
  必须在中断处理例程结束时写入该寄存器。如果存在这样的寄存器，则将 configEIO_ADDRESS 设置为其 
  地址。如果不存在这样的寄存器，则将 configEIO_ADDRESS 设置为 
  写入不会造成损害的变量的地址。

* configCLEAR_TICK_INTERRUPT()

  如下文“配置和安装 RTOS 滴答中断”部分所述，RTOS 滴答 
  中断可由任何方便的定时器来源产生。如果所选定时器产生的中断
  必须在其处理函数中清除，则定义 configCLEAR_TICK_INTERRUPT() 清除 
  中断。如果所选定时器产生的中断不需要显式清除，
  则可以将 configCLEAR_TICK_INTERRUPT() 定义为空（因此它不会生成任何代码）。

**注意：**如果您使用的 Cortex-A9 处理器有官方演示，那么演示提供的 FreeRTOSConfig.h 
文件已经包含正确的设置。


### 配置和安装 RTOS 滴答中断

每个针对基于 ARM Cortex-A 的嵌入式处理器的官方 FreeRTOS 演示 
都包含配置定时器以生成 RTOS 滴答中断和安装 FreeRTOS 滴答中断处理程序的代码。仅当您需要更改提供的实现时， 
才需要以下信息。

宏 configSETUP_TICK_INTERRUPT() 由 RTOS 内核移植层调用。configSETUP_TICK_INTERRUPT() 
必须在 FreeRTOSConfig.h 中 #defined（定义）才能配置外围设备 
按 configTICK_RATE_HZ FreeRTOSConfig.h 设置的频率产生周期性中断。然后必须安装 FreeRTOS_Tick_Handler()
作为中断处理函数。例如：

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


### 中断处理

[官方 RTOS 演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)包括中断处理程序示例。 
请参阅所用处理器的官方 RTOS 演示应用程序，以查找示例和参考 
源代码。

中断的进入、嵌套和退出由 RTOS 内核移植层管理， 
因此应用程序写入器提供的中断处理程序可以是标准 C 函数。不需要特定的中断相关编译指示、汇编代码 
包装器或属性限定符。

在**启用中断的情况下**，RTOS 会调用应用程序写入器提供的中断处理路由。

另请参阅上文关于 configINTERRUPT_VECTOR_ADDRESS FreeRTOSConfig.h 设置的说明。


### 安装 FreeRTOS IRQ 和 SWI (SVC) 中断处理程序

须将 FreeRTOS_IRQ_Handler() 安装为 Cortex-A 的 IRQ 处理程序。

须将 FreeRTOS_SWI_Handler() 安装为 Cortex-A 的 SWI (SVC) 处理程序。

如果无法编辑中断矢量代码，则 FreeRTOS
处理程序可通过 FreeRTOSConfig.h中的 #define 映射到所需的处理程序名称。例如，
如果安装的处理程序分别称为 IRQ_Handler() 和 SWI_Handler()，
则 FreeRTOS 处理程序可以通过将以下两行添加至
FreeRTOSConfig.h 修改。

```c
#define FreeRTOS_IRQ_Handler IRQ_Handler  
#define FreeRTOS_SWI_Handler SWI_Handler  
```
*将 FreeRTOS 中断处理程序名称映射为替代处理程序名称*


### Cortex-A 处理器模式和堆栈

C 启动代码至少必须为 Cortex-A 处理器的 IRQ 和监管器模式配置堆栈。
**main() 必须在特权模式下调用，最好是在
监管器模式**下。

除非 main() 从系统模式调用，
否则无需将堆栈分配给用户/系统模式（main() 不能从用户模式调用）。如果将堆栈
分配给用户/系统模式，则在 RTOS
内核启动后无法使用此堆栈。

RTOS 堆栈溢出检测功能仅检测任务堆栈中的溢出，
而非 IRQ 或监管器堆栈中的溢出。

