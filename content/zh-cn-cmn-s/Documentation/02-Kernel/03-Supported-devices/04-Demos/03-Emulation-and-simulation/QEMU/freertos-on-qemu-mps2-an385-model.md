---
title: "FreeRTOS MPS2 QEMU 演示 (Arm Cortex-M3) 适用于 IAR 和 arm-none-eabi-gcc 编译器（makefile 和 Eclipse）"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]


![QEMU 上的 FreeRTOS](/media/2021/freertos-qemu.png)

本页记录了一个 FreeRTOS 内核演示，面向 Arm Cortex-M3 
 [mps2-an385 QEMU](https://qemu.readthedocs.io/en/latest/system/arm/mps2.html) 模型，还针对 
 [IAR
 Embedded Workbench](https://www.iar.com/products/architectures/arm/iar-embedded-workbench-for-arm/) 和 [arm-none-eabi-gcc](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) (GNU GCC) 编译器提供了预配置的构建项目。GCC 项目使用简单的 makefile，
 可通过命令行或提供的
 [Eclipse CDT IDE](https://www.eclipse.org/cdt/downloads.php) 项目构建。

---

#### *重要！QEMU Cortex-M3 RTOS 演示使用说明*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#mps2-an385-arm-cortex-m3-qemu-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题中的[“我的应用程序无法运行，问题可能出在哪里？”](/Why-FreeRTOS/FAQs/Troubleshooting)，
请特别注意，
建议在开发过程中定义 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
（在 FreeRTOSConfig.h 中定义），并将 [configCHECK_FOR_STACK_OVERFLOW](Stacks-and-stack-overflow-checking.md)
设置为 2。

---

### 源代码组织

本网站提供的 FreeRTOS 发行版包含所有 FreeRTOS 移植的源文件，
以及所有 FreeRTOS 演示应用程序的项目。因此，它所包含的文件数量远多于
使用 Cortex-M3 mps2-an385 QEMU 演示所需的文件数量。
请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)部分，
获取目录结构介绍以及创建
新 FreeRTOS 项目的信息。

mps2-an385 演示应用程序的 IAR Embedded Workbench for ARM 工作区名为
RTOSDemo.eww，位于 FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC/build/iar
目录中。

使用 arm-none-eabi-gcc (GNU GCC) 编译器构建项目的 makefile 和
构建相同 makefile 的 Eclipse 项目都位于
FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC/build/gcc 目录中。

---

### mps2-an385 Arm Cortex-M3 QEMU 演示应用程序

#### 功能

演示项目提供了简单的 blinky 和全面的测试/演示配置， 
详见 [FreeRTOS 演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
文档页面。针对本页所记录的演示，"check" 任务
会定期按以下格式打印信息：

```c

StatusMessageString : aaaa (bb)

```

其中 StatusMessageString 是描述性文本字符串，aaaa 是 RTOS 滴答
计数，bb 是应用程序检测到中断嵌套的
次数。

#### 构建并执行演示应用程序 - IAR

1. 打开 FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC/build/iar/RTOSDemo.eww
 （位于 IAR Embedded Workbench IDE）。
2. 打开 main.c，并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，
 根据需要生成[简单的 blinky 演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#simple-blinky-demo-configuration)或[全面的测试和演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#comprehensive-testdemo-configuration)应用程序
 。
3. 从 IDE 的 "**Project**" 菜单中选择 "**Rebuild All**"，
 构建 RTOS 演示项目时，不应出现任何错误或警告。
 成功构建后，
 会创建 elf 文件 FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC/build/iar/Debug/Exe/RTOSDemo.out。

**注意：**如果 QEMU 已在运行，则构建将失败，因为 QEMU 会阻止
 覆盖生成的 elf 文件。
4. 确保主机上已安装 QEMU。
5. 使用以下命令行启动 QEMU，将 [path-to] 替换为
 IAR 构建生成的 RTOSDemo.out 文件的正确路径。

```c

qemu-system-arm -machine mps2-an385 -cpu cortex-m3 -kernel [path-to]/RTOSDemo.out -monitor none -nographic -serial stdio -s -S  

```

QEMU 命令行

 如果只是
 希望在 QEMU 中运行 FreeRTOS 应用程序，而不连接调试器，
 请省略 "-s -S"。
6. 构建完成后，从 IDE 的 "**Project**" 菜单中选择 "**Download and Debug**"
 。IAR 调试器即会创建与 QEMU 的 GDB 连接，
 启动调试会话，并在进入 main() 函数时中断。

**注意：**请记住在调试会话结束时终止 QEMU 会话，
 否则 QEMU 将阻止
 在下次构建 IAR 项目时覆盖可执行映像， 
 从而导致链接器错误。

#### 构建并执行演示应用程序 - GCC Makefile

1. 确保主机上已安装 [arm-none-eabi-gcc](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) 编译器和 GNU make 实用程序
 。
2. 打开 FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC/main.c，并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，
 根据需要生成[简单的 blinky 演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#simple-blinky-demo-configuration)或[全面的测试和演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#comprehensive-testdemo-configuration)应用程序
 。
3. 打开命令提示符并导航到 FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC/build/gcc
 目录。
4. 在命令提示符中键入 "make"。构建项目时，
 不应出现任何编译器错误或警告。提示：使用 "-j" 参数，
 可在主机上使用更多核心，进而加快编译速度。例如，
 如果有四个核心可用，
 则输入 "make -j4" 可同时构建四个 C 文件。成功构建后，
 会创建 elf 文件 FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC/build/gcc/output/RTOSDemo.out。
5. 确保主机上已安装 QEMU。
6. 使用以下命令行启动 QEMU，将 [path-to] 替换为
 GCC 构建生成的 RTOSDemo.out 文件的正确路径。

```c

qemu-system-arm -machine mps2-an385 -cpu cortex-m3 -kernel [path-to]/RTOSDemo.out -monitor none -nographic -serial stdio -s -S  

```

QEMU 命令行

 如果只是
 希望在 QEMU 中运行 FreeRTOS 应用程序，而不连接调试器，
 请省略 "-s -S"。

8. 现在，可使用 arm-none-eabi-gdb 启动命令行调试会话，
 不过我更倾向于启动图形调试会话，
 步骤如下，这适用于使用 Eclipse IDE 的用户。

#### 构建并执行演示应用程序 - Eclipse

1. 确保主机上已安装 [arm-none-eabi-gcc](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) 编译器和 [Eclipse CDT IDE](https://www.eclipse.org/cdt/downloads.php)
 。如果 Eclipse 中未包含 GNU make 实用程序，则可能需要单独安装。
2. 从 Eclipse 的 "**File**" 菜单中选择 "**Import**"，
 在出现的窗口中选择 "**Existing Projects Into Workspace**"，然后单击 "Next" 按钮。

[\![](/media/2021/import-vanilla-eclipse.jpg)](/media/2021/import-vanilla-eclipse.jpg)
3. 在下一个窗口中，选择 /FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC/build/gcc
 作为根目录，勾选 FreeRTOSDemo 项目，
 务必**不要勾选** "Copy projects into workspace" 复选框，然后单击 "Finish" 按钮，即可将项目导入
 Eclipse。

[\![](/media/2021/import-project-vanilla-eclipse.jpg)](/media/2021/import-project-vanilla-eclipse.jpg)
4. 打开 main.c，并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，
 根据需要生成[简单的 blinky 演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#simple-blinky-demo-configuration)或[全面的测试和演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#comprehensive-testdemo-configuration)应用程序
 。
5. 从 Eclipse 的 "**Project**" 菜单中选择 "**Build All**"。成功构建后，
 会创建 elf 文件 FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC/build/gcc/output/RTOSDemo.out。
6. 确保主机上已安装 QEMU。
7. 打开命令提示符，然后使用以下命令行启动 QEMU， 
 将 [path-to] 替换为
 GCC 构建生成的 RTOSDemo.out 文件的正确路径。

```c

qemu-system-arm -machine mps2-an385 -cpu cortex-m3 -kernel [path-to]/RTOSDemo.out -monitor none -nographic -serial stdio -s -S  

```

QEMU 命令行

 如果只是
 希望在 QEMU 中运行 FreeRTOS 应用程序，而不连接调试器，
 请省略 "-s -S"。
8. 单击绿色 bug speed 按钮旁边的小箭头，然后从出现的菜单中选择 "Debug Configurations..."。

[\![](/media/2021/debug-configurations-vanilla-eclipse.jpg)](/media/2021/debug-configurations-vanilla-eclipse.jpg)
9. 在 Debug Configurations 窗口中，从 "GDB Hardware Debugging" 下选择 "FreeRTOSDemo Default"，
 然后单击 "Debug" 按钮。Eclipse 调试器即会创建与 QEMU 的 GDB 连接，
 启动调试会话，并在进入 main() 函数时中断。

[\![](/media/2021/debug-configuration-selected-vanilla-eclipse.jpg)](/media/2021/debug-configuration-selected-vanilla-eclipse.jpg)

---

### RTOS 配置和使用详情

#### ARM Cortex-M3 RTOS 移植特定配置

此演示特定的配置项位于 FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC/FreeRTOSConfig.h 中。
[您可以编辑此文件中定义的常量，确保适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。尤其是以下常量：

* **configTICK_RATE_HZ**

 此常量可用于设置 RTOS 滴答中断的频率。提供的值 (1000 Hz) 对于
 测试 RTOS 内核功能非常有用，但此频率比大多数应用程序所需的频率都要高。
 降低频率可提高生产应用程序的效率，
 但会导致综合测试中的自检失败。
* **configKERNEL_INTERRUPT_PRIORITY and configMAX_SYSCALL_INTERRUPT_PRIORITY**

 有关这些配置常量的完整信息，请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档。
 请注意，QEMU 模型有 8 个中断优先级位。

请注意！请参阅[专门介绍如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住，ARM Cortex-M 核心中，
数字越小，中断优先级越高。这
似乎有悖直觉，而且很容易忘记！如果希望
为中断分配低优先级，请勿将其优先级指定为 0（或其他较小数值），
因为这实际上可能会导致该中断在系统中具有最高优先级，
因此，如果此优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，则可能导致系统崩溃。另外，请勿忘记
分配中断优先级，因为默认情况下，中断优先级为 0，
这可能导致其处于最高优先级。

ARM Cortex-M 核心的最低优先级实际上是 255，但是不同的
ARM Cortex-M 微控制器制造商实现的优先级位数不同，
并且提供的库函数要求以不同的方式指定优先级。例如，
ST STM32F7 ARM Cortex-M7 微控制器上可以指定的最低优先级实际上为 15，
这是由 FreeRTOSConfig.h 中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义的。可指定的最高优先级
始终为零。

我们还建议确保将所有优先级位指定为
抢占式优先级位，不要将任何优先级位指定为子优先级位。

每个移植都将 "BaseType_t" 定义为对该处理器而言最有效的
数据类型。此移植将 BaseType_t 定义为长类型。

#### 中断服务程序

与许多 FreeRTOS 移植不同的是，引发上下文切换的中断服务程序
无特殊要求，可根据编译器文档编写。
宏 portEND_SWITCHING_ISR()（或 portYIELD_FROM_ISR()）可用于
在中断服务程序内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。

下列源代码片段仅作为示例提供。中断
使用[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
与任务（未显示）同步，并调用 portEND_SWITCHING_ISR
以确保中断直接返回任务。

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A task notification is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. */
    [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskToNotify, &lHigherPriorityTaskWoken );

    /* If the task with handle xTaskToNotify was blocked waiting for the notification
 then sending the notification will have removed the task from the Blocked
 state. If the task left the Blocked state, and if the priority of the task
 is higher than the current Running state task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE
 internally within vTaskNotifyGiveFromISR(). Passing pdTRUE into the
 portEND_SWITCHING_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portEND_SWITCHING_ISR() has no effect. */
    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );
}

```

只有以 "FromISR" 结尾的 FreeRTOS API 函数才能
从中断服务程序中调用，并且中断的优先级必须
小于或等于 configMAX_SYSCALL_INTERRUPT_PRIORITY
配置常量（或 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY）设置的优先级。

#### FreeRTOS 使用的资源

FreeRTOS 需要独占 SysTick 和 PendSV 中断，使用 SVC 编号 #0。

#### 在抢占式和协同式 RTOS 内核之间切换

在 FreeRTOSConfig.h 中将 configUSE_PREEMPTION 设置为 1，即可使用抢占式调度；设置为 0，
即可使用协同式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

ARM Cortex-M7 演示应用程序项目中包含的 Source/Portable/MemMang/heap_4.c 可用于提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

#### 其他事项

请注意，vPortEndScheduler() 尚未实现。

