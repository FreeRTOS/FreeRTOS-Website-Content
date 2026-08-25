---
title: "低功耗 RTOS 演示——Renesas RX100 包括 IAR 的移植，带 GCC 的 e2studio 和带 Renesas 工具的 e2studio"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/rsk_rl78g14.jpg)

**RX100 RSK（ 2013 年 6 月推出）** 

### 简介

此页面上记录的应用程序演示了如何使用 FreeRTOS的
[滴答抑制](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
来最大限度地
降低
在 [Renesas](http://eu.renesas.com/) RX100 微控制器上运行的应用程序的功耗。RX100 专为
需要低功耗的应用
而设计。

该演示提供了以下三个构建选项：

1. [IAR RX 嵌入式工作台](https://www.iar.com/products/architectures/renesas/iar-embedded-workbench-for-renesas-rx/)
2. Renesas [e2studio](http://www.renesas.com/e2studio) 基于 Eclipse 的 IDE
 （使用 [Renesas RX 编译器](http://www.renesas.com/products/tools/coding_tools/c_compilers_assemblers/rx_compiler/index.jsp)）
3. Renesas [e2studio](http://www.renesas.com/e2studio) 基于 Eclipse 的 IDE
 （使用 [GNU GCC 编译器](http://kpitgnutools.com/)）

这些项目已预先配置为在 RX100 的官方 Renesas 入门套件 (RSK) 上
运行。

---

### *重要提示！FreeRTOS RX100 低功耗演示项目使用说明*

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#renesas-rx100-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS zip 文件包含所有 FreeRTOS的源文件
移植的源文件以及所有演示应用程序。此项目只需要一小部分
文件。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
了解关于已下载文件的说明
和新项目创建的信息。

IAR Embedded Workbench 项目称为 RTOSDemo_IAR.eww，位于
FreeRTOS/Demo/RX100-RSK_IAR 目录中。

配置为使用 Renesas 编译器的 e2 studio 项目
位于 FreeRTOS/Demo/RX100-RSK_Renesas 目录中。
本页的[构建说明](#构建和执行演示应用程序---e2studio)部分
包含有关准备 Eclipse 项目
目录的重要信息。

配置为使用 GCC 编译器的 e2 studio 项目
位于 FreeRTOS/Demo/RX100-RSK_GCC 目录中。
本页的[构建说明](#构建和执行演示应用程序---e2studio)部分
包含有关准备 Eclipse 项目
目录的重要信息。

---

### Renesas RX100 演示应用程序

#### 硬件设置

演示使用 RX100 RSK 内置的 LED、按钮和电位计，
因此无需进行硬件设置。

#### 功能

configCREATE_LOW_POWER_DEMO 常量
在 FreeRTOSConfig.h 的顶部定义。构建项目时，如 configCREATE_LOW_POWER_DEMO 设置为 1，
则会创建低功耗演示。如 configCREATE_LOW_POWER_DEMO 设置为 0，
则会创建一个标准的仅内核演示
（不包含滴答抑制）。

#### ConfigCREATE_LOW_POWER_DEMO 设置为 1 时的功能

当 configCREATE_LOW_POWER_DEMO 设置为 1 时，main() 会调用 main_low_power()。
main_low_power() 会创建一个非常简单的演示如下：

* 该演示会创建两个任务，一个 Rx 任务和一个 Tx 任务。
* Rx 任务在 RTOS 队列中阻塞以等待数据，每当收到数据时，
 都会切换 LED 0。
 然后在队列中再次返回阻塞状态。请注意，LED 开启时的电流测量值
 将高于 LED 关闭时的电流测量值。
* Tx 任务反复进入阻塞状态，保持一段时间，
 该时间由内置在 RSK 硬件上的电位计的
 位置决定。解除阻塞状态时，
 Tx 任务通过 RTOS 队列向 Rx 任务发送一个值（使
 Rx 任务解除阻塞状态并切换 LED 0）。

 常量 mainSOFTWARE_STANDBY_DELAY 定义
 在 main_low_power.c 的顶部。如果从电位器读取的值小于或等于
 mainSOFTWARE_STANDBY_DELAY ，
 则 Tx 任务会阻塞相同的毫秒数。例如，
 如果从电位计采样的模拟值为 2000，
 则 Tx 任务会阻塞 2000 毫秒。阻塞一段有限时间，
 RTOS 内核将停止滴答中断，并将 RX100 置于
 其“深度睡眠”低功耗模式。

 如果从电位计读取的值大于
 mainSOFTWARE_STANDBY_DELAY ，则 Tx 任务在信号量上阻塞的
 超时时间为无限长（无限期阻塞）。无限超时阻塞时，RTOS 内核将停止滴答中断
 ，并将 RX100 置于其软件待机
 低功耗模式。按下任何用户按钮都会产生中断，
 使 RX100 退出软件待机模式。中断服务程序
 “给出”阻塞 Tx 任务所在的信号量，
 以解除对 Tx 任务的阻塞。

#### 在 configCREATE_LOW_POWER_DEMO 设置为 1 时使用演示

**为了获得最佳的低功耗结果，RX100 必须与
调试器**断开连接（应用程序必须“独立”执行）。

1. 将 RX100 上的电位计逆时针旋转到底。
2. 使用应用程序对 RX100 进行编程，
 然后断开编程/调试硬件，
 以确保功率读数不受任何连接接口的影响。
3. 启动应用程序运行。LED 0 将快速切换，因为
 电位计已转到最低值。

 只有在 RX100 非节电模式时，LED 1 才会亮起。因为
 大部分执行时间都是在低功耗模式下度过的，而低功耗模式
 只会非常短暂地退出，
 所以人眼看起来是关闭的。

 LED 2 仅在 RX100 处于深度睡眠模式时开启。由于大部分执行时间用于深度睡眠模式，
 所以人眼看起来始终开启。

**注意：**在深度睡眠模式下测量的功耗
 受 LED 2 开启的影响。
4. 沿顺时针方向缓慢转动电位计。这将
 增加从电位器读取的值，也会
 增加 Tx 任务处于阻塞状态的时间，
 因此也将降低 Tx 任务向队列发送数据的频率
 （以及 LED 0 切换的速率）。
5. 继续顺时针转动电位计。最终，
 从电位计读取的值将超过
 mainSOFTWARE_STANDBY_DELAY，导致 Tx 任务阻塞信号量，
 并具有无限的超时。RTOS 将让 RX100 微控制器
 进入软件待机模式。

 LED 0 将停止切换，因为 Tx 任务
 不再发送到队列。LED 1 和 LED 2 都将熄灭，
 因为 RX100 既没有运行也没有处于深度睡眠模式
 （处于软件待机模式）。

**注意：**与深度睡眠模式不同，
 RX100 处于软件待机模式时，所有 LED 都会关闭。这样做是为了确保
 所测量的功耗不会
 受到 LED 的不利影响。
6. 再次逆时针旋转电位器以确保其值
 再次低于 mainSOFTWARE_STANDBY_DELAY。
7. 按下三个按钮中的任何一个以产生中断。中断
 将使 RX100 退出软件待机模式，
 中断服务程序将通过“给予”信号量来解除对 Tx 任务的阻塞。LED 0 将再次
 开始切换。

#### configCREATE_LOW_POWER_DEMO 设置为 1 时 RTOS 的实现

关闭滴答中断使微控制器保持在低功耗模式，
直到任务必须解除阻塞状态并执行。如果没有以这种方式
抑制 RTOS 滴答中断，则微控制器将必须
定期退出所述低功率模式以处理 RTOS 滴答。

* 在本演示中，LED 由应用程序定义的
 预休眠宏和后休眠宏打开和关闭
 （请参阅 FreeRTOSConfig.h 中的 configPRE_SLEEP_PROCESSING() 和 configPOST_SLEEP_PROCESSING() 的定义）。
 通过采取额外的节能步骤，
 可以扩展宏以进一步降低功耗。例如，
 预睡眠宏（在将 RX100 置于低功耗状态之前由 RTOS 调用）
 可以关闭用于
 读取电位计的模拟输入，
 并确保其他微控制器引脚处于优化功耗的状态。而后休眠宏
 （当 RX100 退出低功耗状态时，由 RTOS 调用）
 可用于将 RX100 返回到其休眠前状态。
* 标准 RTOS RX 移植默认使用比较匹配定时器 (CMT) 来
 生成 RTOS 滴答中断，但当 RX100 进入
 软件待机低功耗模式时，CMT 会暂停。因此，只有在所有应用程序任务无限期阻塞（无超时）时，
 演示才会进入软件待机模式。
 可以通过从外部时间源（例如晶体手表）
 而不是 CMT 生成滴答中断来消除此限制。
* 接收到中断时，
 RX100 将退出软件待机模式，
 （请参阅上面关于使用外部时间源代替 CMT 的要点），
 RTOS 不知道从进入到
 随后退出软件待机低功耗状态之间经历了多长时间。如上所述，
 使用外部时间源代替 CMT 将消除
 。此外，应用程序定义的后休眠宏
 用于将 RTOStick 计数调整为距离实时时钟 (RTC) 所维护的时间
 最接近的 第 1/64 秒。

#### configCREATE_LOW_POWER_DEMO 设置为 0 时的功能

当 configCREATE_LOW_POWER_DEMO 设置为 0 时，mail()
调用 main_full()。main_full() 创建一个全面的测试和演示应用程序
以展示：

* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。

创建的任务来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务
集。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。
这些任务没有特定的功能，创建它们仅为演示如何使用 FreeRTOS API，
以及测试 RTOS 移植。除标准演示任务外
，还创建了以下任务和定时器：

* 寄存器测试任务

 这些任务用已知值填充寄存器，
 然后反复检查每个寄存器
 在任务的生命周期内是否仍包含其预期值。每个任务使用不同的值。这些任务以
 非常低的优先级运行，因此经常被抢占。在测试循环的每次迭代中
 都会增加一个检查变量。包含意外值的寄存器
 表示上下文切换机制存在错误，
 并将导致转移到 NULL 循环，
 这又将防止校验变量进一步递增，
 并允许校验定时器（如下所述）确定已发生错误。寄存器测试任务的性质
 要求其必须使用汇编语言编写。
* “检查定时器”和回调函数

 检查定时器的周期最初
 设置为 3 秒。检查定时器回调函数会检查所有标准演示任务，
 不仅检查任务是否正在执行，而且在执行时
 是否报告任何错误。如果检查定时器发现某个任务已暂停，
 已停顿，或报告了错误，则会自行将周期
 仅 200 毫秒。检查定时器回调函数
 每次调用时也切换 LED 0。这可直观体现
 系统状态指示：如果 LED 每三秒切换一次，
 则表示未发现任何问题。如果 LED 每 200 毫秒切换一次，
 则已在至少一个任务中发现问题。

#### 构建和执行演示应用程序 - e2studio

1. 通过执行
 适当的 CreateProjectDirectoryStructure.bat 批处理文件，创建 Eclipse 托管的 make 系统所需的目录结构。

 如果将 e2studio 与 **Renesas 编译器**一起使用，则执行
 FreeRTOS/Demo/RX100-RSK_Renesas/CreateProjectDirectoryStructure.bat。

 如果将 e2studio 与 **GCC** 编译器一起使用，则执行
 FreeRTOS/Demo/RX100-RSK_GCC/CreateProjectDirectoryStructure.bat。
2. 打开 e2studio，根据提示新建工作区或选择现有工作区。
3. 从 e2studio 的 "File" 菜单中选择 "Import"，然后在 "Import" 对话框中
 选择 "General | Existing Projects Into Workspace"，然后单击 "Next"。

![选择将现有 RTOS 项目导入 Eclipse IDE](/media/2018/E2Studio_import.jpg)

**选择 "Existing Project Into Workspace"**
4. 在导入对话框中，浏览到 FreeRTOS/Demo/RX100-RSK_Renesas 目录
 以使用 Renesas 编译器，或浏览到 FreeRTOS/Demo/RX100-RSK_GCC 目录
 以使用 GCC 编译器，请确保在
 “项目“窗口中选中项目，并单击 "结束" 完成导入过程。

![将嵌入的 RTOS 项目导入 E2Studio IDE](/media/2018/E2Studio_import2.jpg)

**浏览到要导入的项目（显示 GCC 项目）**
5. 打开 FreeRTOSConfig.h，并将 configCREATE_LOW_POWER_DEMO 设置为生成
 低功耗无滴答模式演示，或完整测试和演示应用程序，
 根据需求操作。
6. 在 e2studio 的 "Project" 菜单中选择 "Build All"。
7. 确保目标硬件
 使用 E1 USB 接口（可能作为 RSK 的一部分，或可能需要
 单独购买）连接到主计算机。
8. 单击"调试"速度按钮，启动调试会话。

![使用 CDT 在 Eclipse 中开始调试](/media/2018/Debug-speed-button.jpg)

**速度按钮用于从 Eclipse 内部启动

 调试会话**

#### 构建并执行演示应用程序 - IAR

1. 打开 /FreeRTOS/Demo/RX100-RSK_IAR/RTOSDemo_IAR.eww
 （位于 IAR Embedded Workbench IDE 中）。
2. 打开 FreeRTOSConfig.h，并将 configCREATE_LOW_POWER_DEMO 设置为生成
 低功耗无滴答模式演示，或完整测试和演示应用程序，
 根据需求操作。
3. 在 IDE 的 "Project" 菜单中选择 "Build All"。
4. 确保目标硬件
 使用 E1 USB 接口（可能作为 RSK 的一部分，或可能需要
 单独购买）连接到主计算机。
5. 在 IDE 的 "Project" 菜单中选择 "Download and Debug"，
 以启动调试会话。

---

### RTOS 配置和使用详情

#### RX100 RTOS 移植特定配置

此演示特定的配置项包含在项目目录下的 FreeRTOSConfig.h
中。编辑本文件中定义的常量，
确保适合您的应用程序。尤其是以下常量：

* **configTICK_RATE_HZ**
 可通过该常量设置 RTOS tick 的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但此频率高于大多数应用程序的需要。降低该频率有助于提高效率。
* **configKERNEL_INTERRUPT_PRIORITY**
 定义了 RTOS 内核用于定时器和软件中断的中断优先级。应始终将其设置为
 最低中断优先级，在 RX100 中为 1。请参阅[配置页面](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)了解更多信息。
* **configMAX_SYSCALL_INTERRUPT_PRIORITY**
 定义了可以调用 FreeRTOS API 函数的最高中断优先级。等于或低于该优先级的中断可以调用
 FreeRTOS API 函数 ，**前提是**该 API 函数以 "FromISR" 结尾。高于该优先级的中断
 无法调用任何 FreeRTOS API 函数，但不会受到 RTOS 内核正在执行的任何操作的影响。因此，
 它们适用于对时间精度要求极高的功能。请参[阅配置页面](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)，了解详细信息。

RX100 移植层使用 #define 将 "BaseType_t" 定义长整型。

#### 编写中断服务程序 (ISR)

可以使用标准编译器语法编写中断。有关所使用编译器的特定示例，
请参见 main_low_power.c 中的函数 vButtonInterrupt1()
。

通常， ISR 希望触发上下文切换，这样，
ISR 完成时返回的任务就与 ISR 中断的任务不同。如果 ISR 导致某个任务解除阻塞，
并且被解除阻塞的任务与已处于运行状态的任务相比具有更高的优先级，
就属于这种情况。这
可以通过调用 portYIELD_FROM_ISR() 来实现，该函数采用单个参数。
如果不需要上下文切换，则参数应当为 0 ；
如果需要上下文切换，则该参数必须为非零值。下列代码演示了上述内容，

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearInterruptPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. */
    xSemaphoreGiveFromISR( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the
 semaphore caused the task to unblock, and the unblocked task has a priority
 higher than the current Running state task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE
 internally within xSemaphoreGiveFromISR(). Passing pdTRUE into the
 portYIELD_FROM_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portYIELD_FROM_ISR() has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}

```

#### FreeRTOS使用的资源

FreeRTOS 需要独占软件中断。

默认情况下， RTOS 内核使用比较匹配定时器 (CMT) 来生成 RTOS 滴答。
应用程序编写者可以定义 configSETUP_TICK_INTRUP()
（位于 FreeRTOSConfig.h 中) ，以便使用自己的 Tick 中断配置
代替默认值。例如，如果应用程序写入器
创建了一个名为 MyTimerSetup() 的函数，该函数配置了一个备用定时器，
以按所需频率生成中断，则将以下代码添加到 FreeRTOSConfig.h 中
将导致调用 MyTimerSetup() 代替默认定时器配置：

```c

#define configSETUP_TICK_INTERRUPT() MyTimerSetup()

```

**注意 1：**默认的滴答抑制实现都假设
使用 CMT 定时器。

**注意 2：**滴答中断的安装方式取决于所使用的
编译器：

* 使用 GCC 编译器时：无论使用哪种中断来
 生成 RTOS Tick，都必须将 vPortTickISR() 安装为处理程序。在此演示中，安装 vPortTickISR() 作
 为 CMT0 中断处理程序。
* 使用 IAR 和 Renesas 编译器时：须将常量 configTICK_VECTOR 设置为
 生成滴答中断的外围设备使用的矢量。configTICK_VECTOR
 在 FreeRTOSConfig.h 中定义。在本演示配置中，使用 CMT0 外围设备生成滴答中断，
 因此将 configTICK_VECTOR 设置为 VECT_CMT0_CMI0。

#### 在抢占式和协作式 RTOS 内核之间切换

将 RTOSDemo/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式调度；
设置为 0 以使用协作式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 RX100 演示应用程序项目中，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

#### 其他事项

请注意，vPortEndScheduler() 尚未实现。
