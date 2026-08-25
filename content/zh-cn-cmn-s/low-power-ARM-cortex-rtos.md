---
title: 适用于 ARM Cortex-M 的低功耗 RTOS
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

为 ARM Cortex-M 微控制器节省功耗


（**另请参阅 [SAM4L](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAM4L-EK_Low_Power_Tick-less_RTOS_Demo)、[RX100](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX100_RSK_Low_Power_Tick-less_RTOS_Demo) 和 [STM32L](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/STM32L-discovery-low-power-tickless-RTOS-demo) MCU** 上的无滴答演示）

本页面对主要的[低功耗无滴答空闲](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)页面进行了扩充，
具体做法是通过使用 ARM Cortex-M FreeRTOS 移植的微控制器的特定信息。

## 当 SysTick 频率不等于核心频率时，定义 SysTick 频率


默认情况下，FreeRTOS ARM Cortex-M 移植使用 24 位 SysTick 定时器生成滴答
中断。


### 当 SysTick 以核心速度计时时……

大多数 ARM Cortex-M 微控制器以与 ARM Cortex-M 核心相同的频率
对 SysTick 定时器进行计时。在这种情况下，高时钟速度
和 24 位分辨率的结合会导致
可实现的最大无滴答周期严重受限。要实现
非常高的省电收益，有必要用一个使用替代时间源的实现
来覆盖内置的无滴答空闲实现。

如果 SysTick 定时器的频率等于核心频率，那么必须将 configSYSTICK_CLOCK_HZ
定义为等于 FreeRTOSConfig.h中的 configCPU_CLOCK_HZ。或者，
可以干脆省略 configSYSTICK_CLOCK_HZ 的定义，在这种情况下，
它将默认为等于 configCPU_CLOCK_HZ。

 
### 当 SysTick 以低于核心速度的速度计时时……

当 SysTick 定时器的频率低于核心的频率时，
可以实现的最大无滴答周期会大幅增加。

如果 SysTick 定时器频率不等于核心频率，则
configSYSTICK_CLOCK_HZ 必须在 FreeRTOSConfig.h 中定义为等于 SysTick
频率（单位：赫兹）。

 
## 从 SysTick 以外的时钟生成滴答中断

7.3.0 之前的 FreeRTOS 版本总是从
SysTick 定时器生成滴答中断。从 FreeRTOS 7.3.0 版开始，
应用程序编写者可以选择提供自己的滴答中断源。应用程序编写者
可能想这样做，以延长可实现的最大无滴答周期，
或者从一个在微控制器处于深度睡眠模式时保持活动的定时器中
生成滴答中断。

要定义备用定时器源，请执行以下操作：

1. **设置定时器中断**

   定义一个函数来配置定时器以生成周期性中断。
   该函数必须具有以下名称和原型：

   ```c
   void vPortSetupTimerInterrupt( void );
   ```

   中断的频率必须等于 configTICK_RATE_HZ 的值
   （在 FreeRTOSConfig.h 中定义）。

2. **安装中断服务程序**

   FreeRTOS 滴答中断处理程序被称为 xPortSysTickHandler()。
   必须将 xPortSysTickHandler() 安装为
   定时器的处理程序，该定时器由应用程序定义的 vPortSetupTimerInterrupt() 函数配置。

3. **确保不使用 CMSIS 名称**

   一些 FreeRTOS 演示应用程序会将 FreeRTOS 滴答中断处理程序的名称映射到
   默认的 CMSIS SysTick 处理程序名称，即 SysTick_Handler()。这是
   通过在 FreeRTOSConfig.h 中包括以下行来实现的：

   ```c
   #define xPortSysTickHandler SysTick_Handler
   ```

   如果滴答中断是由 SysTick 以外的定时器生成的，
   则不能这样做。

   一些由第三方发布的 FreeRTOS 软件包更进一步，
   在
   FreeRTOS port.c 源文件中将 xPortSysTickHandler() 实际重命名为 SysTick_Handler()。在这种情况下，
   那么 FreeRTOSConfig.h 中的 #define 就可以用来扭转这种变化，
   如下所示：

   ```c
   #define SysTick_Handler xPortSysTickHandler
   ```

   在任何情况下，如果 SysTick 定时器不是中断源，都必须确保不要将 FreeRTOS 的滴答中断
   处理程序安装为 SysTick 处理程序
   。


## 使用微控制器特定的低功耗功能

内置的无滴答空闲实现使用
WFI（等待中断）指令，在停止滴答中断后暂停执行。以下
两个钩子宏允许在 WFI 指令的任何一侧插入应用程序特定的节能代码，
实际上是用应用程序特定的替代指令替换
WFI：

1. **configPRE_SLEEP_PROCESSING( xExpectedIdleTime )**

   configPRE_SLEEP_PROCESSING() 在即将执行 WFI
   指令之前执行。它可以用于关闭外设时钟，并激活
   任何微控制器特定的低功耗功能。传递预计的空闲时间（单位：滴答）作为唯一参数，
   可通过宏的实现进行修改。如果实现将
   xExpectedIdleTime 设置为 0，则不会调用 WFI。这使得
   宏的实现可以覆盖默认的睡眠模式。将
   xExpectedIdleTime 设置为 0 以外的任何值都是危险的！

2. **configPOST_SLEEP_PROCESSING( xExpectedIdleTime )**

   configPOST_SLEEP_PROCESSING() 在微控制器离开低功率状态后
   立即执行。它可以用来逆转
   configPRE_SLEEP_PROCESSING() 的动作，这样做
   可以使微控制器恢复到全面运转状态。传递预计的空闲时间（单位：滴答）作为唯一参数，
   可通过宏的实现进行修改。应只能由完全了解内置 ARM Cortex-M 低功率实现
   （通过查看源代码注释）的专家用户，
   来尝试修改微控制器离开低功率状态后
   的预计空闲时间。

configPRE_SLEEP_PROCESSING 和 configPOST_SLEEP_PROCESSING() 可在
FreeRTOSConfig.h 中定义。

 
## 示例配置


### 当 SysTick 频率等于核心频率时，使用内置的无滴答空闲实现

1. 在 FreeRTOSConfig.h中将 configUSE_TICKLESS_IDLE 设置为 1


### 当 SysTick 频率不等于核心频率时，使用内置的无滴答空闲实现

1. 在 FreeRTOSConfig.h中将 configUSE_TICKLESS_IDLE 设置为 1
2. 将 configSYSTICK_CLOCK_HZ 设置为等于 SysTick 时钟频率（单位：赫兹）。


### 当使用 SysTick 以外的时钟来生成滴答中断时，使用内置的无滴答空闲实现

这不是一个有效的配置。

 
### 使用 SysTick 以外的时钟生成滴答中断

1. 在 FreeRTOSConfig.h 中将 configUSE_TICKLESS_IDLE 设置为 2。
2. 提供 vPortSetupTimerInterrupt() 的实现，
   以 configTICK_RATE_HZ
   FreeRTOSConfig.h 常量指定的频率生成一个中断。
3. 安装 xPortSysTickHandler() 作为定时器中断的处理程序，
   并确保 xPortSysTickHandler() 没有被映射到
   FreeRTOSConfig.h 中的 SysTick_Handler()，或在 port.c 中被重命名为 SysTick_Handler()。
4. 按照[无滴答空闲](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)文档主页面的说明定义 portSUPPRESS_TICKS_AND_SLEEP()
   。


或者，这也可以通过覆盖弱定义的 vPortSetupTimerInterrupt() 和
vPortSuppressTicksAndSleep() 来实现。在这种情况下，configUSE_TICKLESS_IDLE 设置为 1。
用户需要提供 vPortSetupTimerInterrupt() 和 vPortSuppressTicksAndSleep() 的匹配实现。并且函数
定义不应有弱属性。用户还需要安装 xPortSysTickHandler()，
如上所述。
