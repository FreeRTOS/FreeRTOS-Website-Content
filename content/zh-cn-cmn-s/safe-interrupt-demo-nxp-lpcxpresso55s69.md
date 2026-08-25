---
title: 适用于  NXP LPCXpresso55S69 开发板的更安全的中断处理演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 引言

[支持内存保护单元（MPU）的 FreeRTOS 移植](/Security/04-FreeRTOS-MPU-memory-protection-unit) 
通过在非特权模式下运行应用任务，增强微控制器应用程序的稳健性和安全性 
。这些非特权模式任务仅能访问自身堆栈和一些预配置内存区域。 
在支持 MPU 的微控制器上，可在特权模式下运行的应用程序代码只有 
中断服务程序 (ISR)。在大多数应用程序中，最佳做法是尽可能缩短 ISR 时间 
以保持实时响应。在带有 MPU 的微控制器上，尽可能缩短 ISR 时间 
可提高应用程序安全性，因为这可以最大限度地减少在特权模式下花费的时间。本演示展示了一种 
通过将大部分处理工作推迟到非特权任务来缩短 ISR 时间的方法。


## 源代码组织

FreeRTOS zip 文件下载内容包含所有 FreeRTOS 移植的源代码和 
所有演示应用程序。这意味着其包含的文件远多于使用 FreeRTOS ARMv8-M 
Cortex-M33 移植所需的文件。请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面 
了解 zip 文件的目录结构信息。

此演示的项目文件采用常见的 Eclipse 项目名称 .project， 
位于 `FreeRTOS/Demo/Safe_Interrupts_M33F_NXP_LPC55S69_MCUXpresso/MCUXpresso` 目录中。本项目中编译的 
FreeRTOS ARMv8-M Cortex-M33 移植文件位于 
`FreeRTOS/Source/portable/GCC/ARM_CM33_NTZ/non_secure` 目录中。


## 概念

应用程序将创建中断队列（标准 FreeRTOS 队列），所有 ISR 都可向该队列发布请求。 
这些请求稍后由非特权中断处理程序任务处理。中断处理程序任务 
以最高优先级运行，以确保中断请求不会因其他任务而延迟。 
ISR 可解除对高优先级中断处理程序任务的阻塞，然后直接返回到中断处理程序任务， 
而不是先前执行的任务。 

[\![](/media/2021/concept-interrupt-1.jpg)](/media/2021/concept-interrupt-1.jpg)

增加中断队列和不同优先级的相应中断处理程序任务， 
即可轻松扩展设计模式，模拟中断嵌套。 

[\![](/media/2021/concept-interrupt-2.jpg)](/media/2021/concept-interrupt-2.jpg)

在上述示例图中，UART 中断由优先级较低的中断处理程序处理，因此 
可以被优先级较高的中断处理程序处理的 GPIO 中断打断 
。 


## 演示应用程序

本项目包括两项演示： 

1. GPIO 演示
2. UART 演示


### GPIO 演示

GPIO 演示包含的任务为定期切换板载 RGB LED。用户按下 
LPC55S69-EVK 上的 USER 按钮时，GPIO 中断会被置位，相应的中断处理程序 
会向中断队列发出请求。中断处理程序任务会处理此请求并更改 
LED 的颜色。

```c
void userButtonPressedHandler( void )  
{  
    UserIrqRequest_t xIrqRequest;  
    BaseType_t xHigherPriorityTaskWoken;  

    /* We have not woken a task at the start of the ISR. */  
    xHigherPriorityTaskWoken = pdFALSE;  
  
    /* Post a request to the interrupt queue which will be later processed by  
     * the unprivileged interrupt handler task. */  
    xIrqRequest.xHandlerFunction = vButtonPressedIRQHandler;  
    xIrqRequest.ulData = 0; /* Not used. */  
    xQueueSendFromISR( xUserIrqQueueHandle, &( xIrqRequest ), &( xHigherPriorityTaskWoken ) );  

    /* Posting the above request might have unblocked the interrupt handler task.  
     * Make sure to always return to the interrupt handler task instead of the  
     * previously executing task. */  
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );  
}  
```
**按下 USER 按钮的 ISR**


### UART 演示


UART 演示包含的任务为在串行控制台上打印命令菜单并等待用户 
输入。用户在串行控制台上提供输入时，UART Rx 中断会被置位， 
相应的中断处理程序会向中断队列发出请求。中断处理程序任务负责处理此请求 
并将请求命令的结果发布到串行控制台。 

```c
void uartRxInterruptHandler( void )  
{  
    UserIrqRequest_t xIrqRequest;  
    BaseType_t xHigherPriorityTaskWoken;  
  
    /* We have not woken a task at the start of the ISR. */  
    xHigherPriorityTaskWoken = pdFALSE;  
  
    /* Post a request to the interrupt queue which will be later processed by  
     * the unprivileged interrupt handler task. */  
    xIrqRequest.xHandlerFunction = vUartDataReceivedIRQHandler;  
    xIrqRequest.ulData = ( uint32_t ) USART_ReadByte( USART0 );  
    xQueueSendFromISR( xUserIrqQueueHandle, &( xIrqRequest ), &( xHigherPriorityTaskWoken ) );  

    /* Posting the above request might have unblocked the interrupt handler task.  
     * Make sure to return to the interrupt handler task in case it was not already  
     * running. */  
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );  
}  
```
**UART Rx ISR**


## 构建并运行 RTOS 演示应用程序

1. 启动 the MCUXpresso IDE。请注意，MCUXpresso IDE 需要10.3.1或更高版本才能 
   构建并运行此演示。

2. 选择工作区目录，然后点击 "**Launch**"。

   [\![](/media/2021/launch-workspace.jpg)](/media/2021/launch-workspace.jpg)

3. 点击 "**File -> Import...**"，打开导入项目对话框。

   [\![](/media/2021/import-project.jpg)](/media/2021/import-project.jpg)

4. 选择 "**General -> Existing Projects into Workspace**"，然后点击 "**Next**"。

   [\![](/media/2021/existing-project.jpg)](/media/2021/existing-project.jpg)

5. 点击 "**Select root directory**" 旁边的 "**Browse...**"，然后选择
   `FreeRTOS/Demo/Safe_Interrupts_M33F_NXP_LPC55S69_MCUXpresso` 目录。Projects 窗格中随即可显示 
   名为 FreeRTOSDemo 的项目，如下所示。点击 "**Finish**"。

   [\![](/media/2021/select-root-dir.jpg)](/media/2021/select-root-dir.jpg)

6. 右击 FreeRTOSDemo，选择 "**Build Project**"，即可构建项目。

   [\![](/media/2021/interrupt-build-project.jpg)](/media/2021/interrupt-build-project.jpg)

7. 使用 "Debug Link (P6)" 微型 USB 端口为主板供电。

8. 点击 "**FreeRTOSDemo**"，选择项目。转到快速启动面板中的 "**Debug your project**"， 
   然后点击下拉菜单中的 "**Program flash action using LinkServer**"， 
   如下所示。

   [\![](/media/2021/program-flash-action.jpg)](/media/2021/program-flash-action.jpg)

9. 随即 "Probes Discovered" 窗口中会显示 LPC-LINK2 探针。点击 "**OK**"。

   [\![](/media/2021/connect-to-target.jpg)](/media/2021/connect-to-target.jpg)

10. 在 "**SWD Configuration**" 窗口中选择 SWD Device 0。点击 "**OK**"。

   [\![](/media/2021/swd-configuration.jpg)](/media/2021/swd-configuration.jpg)

11. 此时日志中会显示 "Finished writing Flash successfully" 字样。点击 "**OK**"。

   [\![](/media/2021/file-into-flash.jpg)](/media/2021/file-into-flash.jpg)

12. 转到快速启动面板中的 "**Debug your project**"，然后点击下拉菜单中的 "**Debug using LinkServer probes**" 
   （如下所示），以启动调试会话。

   [\![](/media/2021/debug-using.jpg)](/media/2021/debug-using.jpg)


## RTOS 配置和使用详情

另请参阅  [介绍在 ARMv8-M 核心上运行 FreeRTOS 的页面](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers.md)， 
以及介绍[设置 ARM Cortex-M 中断优先级以便与 FreeRTOS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4) 配合使用的页面。 


* 此演示的相关配置项目位于 
 `FreeRTOS/Demo/Safe_Interrupts_M33F_NXP_LPC55S69_MCUXpresso/Projects/MCUXpresso/Config/FreeRTOSConfig.h`。 
 您可以根据应用程序的需求，编辑该文件中定义的常量。以下配置选项 
 适配于 ARM Cortex-M33 移植：

	+ `configENABLE_MPU` - 启用/禁用内存保护单元 (MPU)。
	+ `configENABLE_FPU` - 启用/禁用浮点单元 (FPU)。
	+ `configENABLE_TRUSTZONE` -启用/禁用 TrustZone。

* 该演示在安全端运行 FreeRTOS，因此请将 `configENABLE_TRUSTZONE` 
  设置为 0，并将 `configRUN_FREERTOS_SECURE_ONLY` 设置为 1（在 `FreeRTOSConfig.h` 文件中设置）。此演示使用 
  `FreeRTOS/Source/portable/GCC/ARM_CM33_NTZ` 目录中的 FreeRTOS 移植文件。

* `Source/Portable/MemMang/heap_4.c` 包含在项目中，以提供 
  RTOS 内核所需的内存分配。请参阅 API 文档的“内存管理”部分， 
  以获取完整信息。

* `vPortEndScheduler()` 尚未实现。

