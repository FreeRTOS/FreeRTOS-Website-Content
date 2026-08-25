---
title: "适用于 TI MSP430F5438 (MSP430X) 微控制器的 FreeRTOS 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 使用 Code Composer Studio IDE 和编译器

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

|  |
| --- |
| <br />![在 MSP 430F5438 实验板上运行的 FreeRTOS](/media/2018/FreeRTOS-running-on-an-MSP-430F5438-Experimenter-board.jpg)<br /> |

**本页记录的演示已过时，
 已由[使用更高硬件和工具版本的演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#TI)所取代。**

### 简介

本页记录的 FreeRTOS 演示应用程序适用于具有 MSP430X 核心的 [MSP430F5438 微控制器](http://focus.ti.com/docs/prod/folders/print/msp430f5438.html)
（由 [Texas Instruments](http://www.ti.com/) 提供）。本演示使用 [MSP430 Code Composer Studio](http://focus.ti.com/docs/toolsw/folders/print/ccstudio.html)
IDE 和编译器，针对 TI 提供的官方 [MSP-EXP430F5438](http://focus.ti.com/docs/toolsw/folders/print/msp-exp430f5438.html)
实验板（如需使用其他开发版，请参阅此处[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）
。

移植和演示项目使用“大”和“小”数据模型以及“大”和“小”代码模型进行开发和测试。

### 此演示项目演示的 FreeRTOS 功能

该项目演示了以下 FreeRTOS 功能和技术：
* “网关守卫”任务设计模式

 演示 LCD 任务是唯一允许访问 LCD 的任务，
 LCD 的“网关守卫”也是如此。要将字符串写入 LCD 的其他任务**和中断**
 不会直接访问 LCD，而是
 使用 FreeRTOS 队列将其希望显示的字符串
 发送到 LCD 任务。
* “控制器”任务设计模式

 LCD 任务还演示了“控制器”任务设计模式。
 发送到 LCD 的消息是包含
 消息类型和消息值参数的结构体。通过首先检查消息类型，LCD 任务
 了解如何处理消息值（可以是整数、字符指针
 或其他任何内容）。
* 受控（非自由运行）的输入轮询

 按钮轮询任务使用 vTaskDelay() FreeRTOS API 函数
 来控制读取按钮输入的速率。这
 消除了复合按钮反跳的需要，并防止
 任务利用所有可用的处理时间。
* （有效和间接地）从中断服务程序写入 LCD

 通常无法从中断服务程序有效地访问
 慢速输出设备（例如 LCD）。在本演示中，操纵杆选择按键
 用于生成外部中断，中断服务程序
 通过将字符串发送到一个消息队列中的 LCD 任务
 来将字符串间接发送到 LCD。这是将 LCD 任务用作上文所述的
 “网关守卫”任务。
* 空闲任务钩子函数

 该演示利用空闲任务钩子函数使处理器
 处于低功耗状态。但请注意，该演示使用许多不同演示使用的标准
 任务实现来实现，因此
 未针对低功耗操作进行优化。将轮询任务转换为事件驱动任务，
 降低滴答中断频率等，
 可以实现更低的功耗。
* 软件定时器回调函数

 演示使用软件定时器实现“看门狗”
 类型函数。该函数定期监视系统中的所有其他任务
 以查找任何意外行为，然后会向 LCD/控制器任务发送 PASS 或
 错误代码状态消息。LCD/控制器
 演示任务使用已接收消息的消息类型成员
 将消息转译为状态消息，然后使用同一消息的
 消息值成员来确定应该将哪个状态字符串
 写入 LCD。

 演示应用程序还会创建标准软件定时器测试任务，
 该任务是一组标准演示任务集的一部分。
* malloc() 失败的钩子函数

 调用 pvPortMalloc() 失败时会调用 malloc() 失败钩子函数，
 因为没有足够的可用 FreeRTOS 堆内存
 来完成分配。
 可以从应用程序任务中调用 pvPortMalloc()，也可以
 从创建任务、队列和信号量的 FreeRTOS API 函数中调用。
* 查询未分配的 FreeRTOS 堆内存量

 在 RTOS 调度器启动后从任务中调用 xPortGetFreeHeapSize()，
 并将未分配的 FreeRTOS 堆内存量
 （仍然可用的堆内存量） 输出到
 LCD。

---

### *重要！使用 MSP430X CCStudio 4 演示的注意事项*

*使用此 RTOS 移植之前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法
运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载内容包含所有 FreeRTOS 移植的源代码，因此
包含的文件比此演示所需更多的文件。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
获取下载文件的说明和有关创建新项目的
信息。

MSP430F5438 演示的 CCS 项目文件位于
FreeRTOS/Demo/MSP430X_MSP430F5438_CCS4 目录中。此项目是
应导入 CCS 工作区的项目。下文“[准备 Eclipse 项目](#构建和运行演示应用程序)”
部分包含有关设置演示项目目录
以及将演示项目导入 Code Composer Studio 的重要信息。

---

### 演示应用程序

### 演示应用程序硬件设置

演示应用程序包含中断驱动的 UART 测试。这会产生两个
任务，包括一个发送任务和一个接收任务。传输任务将字符发送到
UCA1 上，然后接收任务在同一个 UCA1 外围设备上接收字符。接收任务
接收任务期望接收发送任务发送的字符，但由于
没有外部 9 路连接器，硬件内部配置为使用
环回模式。因此，与其他 FreeRTOS 演示不同，无需
将外部环回连接器安装到 UART 即可进行 COM 端口测试。

**请注意**，UART 中断服务程序的实现是为了演示从
中断服务程序内部使用队列。这**并不是**
一个高效中断实现的示例。真正的应用程序应该
使用 DMA。或至少传送和接收可使用
简单的 RAM 环形缓冲区，并在接收或传送完整消息时
使用信号量与任务同步。

该移植使用 Texas Instruments MSP-FET430UIF USB 调试接口
进行开发和测试。

### 准备 CCS (Eclipse) 项目目录

Eclipse 项目既可以是标准 makefile 项目，也可以是托管 make 项目。
MSP430X CCS4 项目使用托管 make 项目。因此意味着
以下两种情况：

1. 构建项目所需的所有源文件必须位于
 包含项目文件本身的文件夹/目录下，或
2. 需要配置 Eclipse 工作区（注意是工作区，而非项目）
 来定位硬盘上其他位置的文件。

本示例采用第一种。为此，目录 FreeRTOS/Demo/MSP430X_MSP430F5438_CCS4
包含一个名为 CreateProjectDirectoryStructure.bat 的批处理文件，
该文件会将所有必需的 FreeRTOS 源文件复制到
演示项目目录内的子目录中。

**CreateProjectDirectoryStructure.bat 必须在将 Code Composer Studio
项目导入 Eclipse 工作区之前执行**。

CreateProjectDirectoryStructure.bat 不能
Code Composer Studio Eclipse IDE 内部执行。

### 将演示应用程序项目导入 CCS Eclipse 工作区

要将 MSP430X CCS 项目导入现有或新的 Eclipse 工作区：
1. 在 CCS 的 "File" 菜单中选择 "Import"。系统将显示
 如下对话框：

![将 MSP430X CCS 项目导入 Eclipse 工作区](/media/2018/Importing-the-MSP430X-CCS-project-into-the-Eclipse-workspace.jpg)

**首次点击 "Import" 时显示的对话框**
2. 在下一个对话框中，选择 FreeRTOS/Demo/MSP430X_MSP430F5438_CCS4
 作为根目录。然后，确保在 "Projects" 区域中已勾选 RTOSDemo 项目
 **并确保未勾选 "Copy Projects Into
 Workspace" 复选框**，
 然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态， 
 图片中不包含 "Finish" 按钮）。

![选择要导入Eclipse的 FreeRTOS MSP430X CCS 项目](/media/2018/selecting-the-FreeRTOS-MSP430X-CCS-project-to-import-into-Eclipse.jpg)

**确保已勾选 "RTOSDemo"，且未勾选 "Copy projects into workspace"**

### 构建和运行演示应用程序

1. 确保 CreateProjectDirectoryStructure.bat 已执行，
 并确保项目已正确导入到 Eclipse 工作区。
2. 选择所需的构建配置

 CCS4 项目包含四个构建配置。所有的构建配置
 都展示了相同的功能，但具有不同的运行时模型和优化
 设置，如下表所述。

|  |  |
| --- | --- |
| **构建配置** | **描述** |
| <br /> Debug_Large_Data_Model<br />  | <br /> 配置为使用大数据模型、大代码模型，零优化<br />  |
| <br /> Release_Large_Data_Model<br />  | <br /> 配置为使用大数据模型、大代码模型，并进行最大限度的优化。<br />  |
| <br /> Debug_Small_Data_Model<br />  | <br /> 配置为使用小型数据模型、大型代码模型，零优化。<br />  |
| <br /> Debug_Small_Data_Small_Code_Model<br />  | <br /> 配置为使用小数据模型、小代码模型，零优化。<br />  |
3. 在 IDE 的 "Project" 菜单中选择 "Rebuild All"。
4. 在 IDE 的 "Project" 菜单中选择 "Debug Active Project"。MSP430X 闪存将使用新建的二进制内存进行编程。然后调试器将启动并运行到 main() 函数的开始处。

### 功能

此网页顶部列出了 MSP430X5438 演示项目演示的 FreeRTOS
功能。main.c 源文件中包含的注释
提供了有关如何实现和实现此功能的
更多信息。

演示正确执行时，将观察到以下行为：

* 每次 COM 测试传输任务传输一个
 字符时，LED 2 都会切换。
* LED 1由滴答中断钩子函数控制，用于
 指示滴答中断正在运行。每 0xFF 毫秒
 切换一次。
* 每 5 秒将在 LCD 上 显示一条状态消息。如果
 演示正在执行且没有错误，则状态将显示
 为 PASS。在所有其他情况下，状态消息将指示
 哪个任务或测试报告了错误。
* 按下或释放操纵杆 "up" 按钮
 会在 LCD 上显示字符串。 该字符串指示按钮状态。
* 按下操纵杆 "select" 按钮
 （直接向下朝向其底部的 PCB 按下），
 会在 LCD 上显示一条消息，指示已生成
 按钮中断。

---

### RTOS 配置和使用详情

### 配置 RTOS 滴答中断

FreeRTOS 需要独占使用定时器，该定时器能够生成
称为 RTOS “滴答”中断的快速周期性中断。定时器在
用户可定义的钩子（或回调）函数中配置，因此应用程序编写者
可以灵活地决定实际使用哪个定时器外围设备。钩子函数的名称和原型
如下图所示：

void vApplicationSetupTimerInterrupt( void );

须将常量 configTICK_VECTOR
设置为所选外围设备的中断向量数量。configTICK_VECTOR 在 FreeRTOSConfig.h
头文件中定义。此演示项目包括
vApplicationSetupTimerInterrupt() 的实现，该实现配置时间 TA0 以生成滴答
中断，因此将 configTICK_VECTOR 设置为 TIMER0_A0_VECTOR。仅在正
开发的应用程序需要 TA0 空闲用于其他目的时，
才必须修改提供的代码。

### RTOS 端口特定配置

这些演示的特定配置项位于 FreeRTOS/Demo/MSP430X_MSP430F5438_CCS4/FreeRTOSConfig.h 中。可编辑
此文件中定义的常量，以适配您的应用程序。特别是以下常量：

* **configTICK_RATE_HZ**
 此常量可用于设置 RTOS 滴答中断的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值将提高效率。

每个移植都将 "BaseType_t" 定义为对该处理器而言最有效的数据类型
对处理器而言最有效的数据类型。此移植将 BaseType_t 定义为短整型。

请注意 vPortEndScheduler() 尚未实现。

### 中断服务程序

与大多数移植不同，导致上下文切换的中断服务程序
无特殊要求，可根据编译器文档编写。
宏 portYIELD_FROM_ISR() 可用于从 ISR 内请求上下文切换。
请注意，portYIELD_FROM_ISR() **必须**是 ISR 中的最后一个语句。

此演示项目提供了 FreeRTOS 中断服务程序示例，
即 main.c 中定义的 prvSelectButtonInterrupt() 和 serial.c 中
定义的 prvUSCI_A0_ISR()。请注意，实现 prvUSCI_A0_ISR() 是为了强调移植并
演示中断使用的队列，并不是为了演示
高效或通用的中断服务程序！

### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/MSP430X_MSP430F5438_CCS4/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1 即可使用抢占式内核，设置为 0 可
使用协同式内核。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

演示应用程序项目中内置 Source/Portable/MemMang/heap_2.c，
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。
