---
title: "QEMU LM3S6965 模型移植的 FreeRTOS演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

\![QEMU [paused]](/media/2020/FreeRTOS_Cortex-M_QEMU.jpg)

此页面描述了在 LM3S6965 QEMU 模型上构建和运行 FreeRTOS ARM Cortex-M3 GCC 移植的预配置 Eclipse 项目
。

---

#### 重要提示！使用 ARM Cortex-M3 移植的注意事项

_使用此 RTOS 移植前,请阅读下述所有要点。_

1. [在 ARM Cortex-M3 核心上使用 FreeRTOS 的说明](#配置和使用详情)
2. [源代码组织](#源代码组织)
3. [演示应用程序功能](#lm3s6965-qemu-演示应用程序)
4. [在 QEMU 仿真器中使用 LM3S6965 构建和运行 RTOS演示应用程序](#构建-rtos-演示应用程序)
5. [RTOS 配置和使用详情](#配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)”。

---

### 在 ARM Cortex-M3 核心上使用 FreeRTOS

如果您不满足于仅仅运行本页所描述的演示，或者您想创建自己的 ARM Cortex-M
FreeRTOS项目，还可以参阅在 ARM Cortex-M 上运行[ FreeRTOS内核的一般信息](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。

### 源代码组织

FreeRTOS 内核和演示的代码可从 FreeRTOS.org 上的[主下载页面](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)获取。
FreeRTOS zip 文件下载内容包含所有 FreeRTOS 移植和演示应用程序的源代码——因此包含的文件比此项目所需文件多得多。请参加[源
代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)页面，了解有关目录结构的信息。

LM3S6965 QEMU 项目位于`/Demo/CORTEX_LM3S6965_GCC_QEMU`目录。
[构建说明](#构建-rtos-演示应用程序)部分提供详细信息。

---

### LM3S6965 QEMU 演示应用程序

#### 功能

由于 QEMU 主要作为开发目标，该演示中（尚）不包含简单的 "blinky" 项目（
在其他项目中可找到）。但是，`main()`会直接创建一个全面的测试和演示应用程序。该演示
将测试（除此之外）：

- [流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
- [消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
- [任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
- [事件组](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)
- [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
- [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)
- [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers/)
- [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)

创建的任务来自 [标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/)任务集。标准演示
任务被所有 FreeRTOS 移植演示应用程序使用。它们没有特定的功能，仅用于演示
如何使用 FreeRTOS API，并测试 RTOS 移植。

[tick 钩子](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)函数会定期检查标准演示任务（其中包含自我监控
代码），以确保所有任务都正常运行。然后，它会向任务发送状态消息，该任务会
在仿真 OLED 显示屏上打印状态消息，并将状态消息打印到仿真 UART。如果状态消息为 "PASS"（通过），
则所有任务都按预期执行。否则，状态消息会显示报错的任务。

**注意：** 如果您在 Windows 主机上（可能在Linux上）执行演示数小时，可能会报错
。这可能是一个假阳性，显然是由于写入仿真 IO 引起的。如果删除对仿真 OLED 显示屏和 UART 的写入，
则该演示可以运行数周而不报错。

![](/media/2020/Screen-Shot-2020-08-19-at-5.34.52-PM.png)
QEMU 控制台输出。

#### 构建 RTOS 演示应用程序

该项目与带有 Eclipse Embedded CDT 插件的基本 Eclipse 版本配合使用。打开并构建演示项目：

1. 下载并安装 [Eclipse Embedded CDT（C/C + + 开发工具）](https://projects.eclipse.org/projects/iot.embed-cdt/downloads)，该工具将 Eclipse IDE 
   for C/C++ Developers 标准版与 Eclipse Embedded CDT 插件打包在一起。

2. 下载并安装
   [GNU Arm 嵌入式工具链](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)

3. 按照在 Eclipse(/Documentation/02-Kernel/03-Supported-devices/04-Demos/Device-independent-demo/building-demos-in-eclipse)中[导入和构建演示项目页面上的] “先决条件”部分进行操作 ，以确保您已正确设置环境。该演示使用的 GCC 编译器
   属于
   前一步骤中安装的[GNU Arm 嵌入式工具链](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)的一部分。

4. 按照在 Eclipse 中[导入和构建演示项目](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Device-independent-demo/building-demos-in-eclipse)页面上的“导入并构建演示项目”部分进行操作。导入位于
   ``/Demo/CORTEX_LM3S6965_GCC_QEMUGit 存储库FreeRTOS或 FreeRTOS 发布版 zip 文件的目录中的项目。

#### 在 QEMU 仿真器中运行 RTOS 演示应用程序

**在 Windows 环境中：**

1. [下载并安装预建的 QEMU Windows 二进制文件。](https://www.qemu.org/download/#windows)

2. 在开启 Eclipse 之前，请确保含有 QEMU 可执行文件的目录包含在 PATH 环境变量中
   。

3. 导入并构建项目，如上所述。

4. 在 Eclipse 项目资源管理器中右键单击 "``start_quem_and_debug.launch" 文件，然后
   从弹出菜单中选择 "Debug As->start_quem_and_debug"。QEMU 会启动，然后 GDB 调试器会启动并连接
   至 QEMU。

![](/media/2020/Screen-Shot-2020-08-19-at-5.00.48-PM.png)
运行调试会话 (Windows)。

**所有其他环境（也适用于 Windows ）：**

1. 按照 [安装并启动 QEMU 仿真器页() ] /Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/QEMU/Install-and-start-QEMU-emulator面上的说明进行操作，
   并从 CORTEX_LM3S6965_GCC_QEMU 演示项目目录中输入以下命令以启动 QEMU：

   ```c
   qemu-system-arm -kernel ./Debug/RTOSDemo.elf -S -s -machine lm3s6965evb
   ```

2. 右键单击 Eclipse 项目资源管理器中的 "RTOSDemo Debug.launch" 文件，然后从弹出菜单中选择 "Debug As->RTOSDemo Debug"
   。调试器将启动并连接到 QEMU（假设前一步骤已运行 QEMU）。

   ![](/media/2020/Screen-Shot-2020-08-19-at-4.37.15-PM.png)
   运行调试会话。

### 配置和使用详情

#### RTOS 移植特定配置

本节内容与[在 ARM Cortex-M 核心上RTOS ](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4运行文档)页面提供的信息相关联。此演示的特定配置项目位于 `FreeRTOS/Demo/CORTEX_LM3S6965_GCC_QEMU/FreeRTOSConfig.h` 中。
[您可以根据应用程序的需求，/Documentation/02-Kernel/03-Supported-devices/02-Customization()]编辑该文件中定义的常量。特别是：

- **configKERNEL_INTERRUPT_PRIORITY**

  `configKERNEL_INTERRUPT_PRIORITY` 应设置为最低优先级。请记住，ARM Cortex-M 核心
  使用低数值的优先级数字表示逻辑上的高优先级中断。在
  ARM Cortex-M 核心上的最低优先级实际上是 255，不同的 ARM Cortex-M 微控制器制造商会采用不同数量的
  优先级位。但是，QEMU 不对优先级位进行建模，因此 LM3S6965 微控制器实际只有三个
  优先级位，而 QEMU 模型有八个优先级位，所以将`configKERNEL_INTERRUPT_PRIORITY`设置为 255。

- **configMAX_SYSCALL_INTERRUPT_PRIORITY**

  `configMAX_SYSCALL_INTERRUPT_PRIORITY`必须设置为零。请参阅
  [在ARM Cortex-M 核心上运行 RTOS ](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。

其他注意事项：

- `vPortEndScheduler()` 尚未实现。

- QEMU LM3S6965 演示项目会构建`Source/Portable/MemMang/heap_4.c`，
  以提供 RTOS 内核所需的内存分配。请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
  以获取完整信息。
