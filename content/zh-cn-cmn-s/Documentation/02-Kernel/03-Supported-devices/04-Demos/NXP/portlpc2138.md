---
title: "飞利浦LPC2138 (ARM7) RTOS Rowley CrossFire LPC2138 的移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

|  |
| --- |
| <br />![](/media/2018/crossfirelpc2138.gif)<br /> |

本页演示了在FreeRTOSCrossFire LPC2138 嵌入式评估套件上运行的[Rowley CrossWorks (GCC) LPC2000 移植](http://www.rowley.co.uk/crossfire/crossfire_lpc2138.htm)
（如果您希望使用替代开发板，我们也提供相关[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）。

CrossFire LPC2138 是一个低成本的评估平台，包括机载 USB CrossConnect JTAG 调试接口。评估版本
[CrossWorks (http://www.rowley.co.uk/)]嵌入式开发工具的评估版本可用于为 CrossFire 开发板开发软件，
无编译代码大小或时间限制。

---

### 重要提示！使用 [LPC2138](https://www.nxp.com/docs/en/data-sheet/LPC2131_32_34_36_38.pdf) RTOS移植的注意事项

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示所需的多得多。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，了解
下载文件的描述和有关创建新项目的信息。

适用于 Philips LPC2138 ARM7 微控制器的 Rowley CrossWorks / GCC 演示文件名为 RTOSDemo.hzp，位于
FreeRTOS/Demo/ARM7_LP2138_Rowley 目录中。

---

### 演示应用程序

#### 构建配置

如下图所示，提供了四个构建配置。

![](/media/2018/configselect.gif)
在 CrossWorks IDE 中选择构建配置

#### RTOS 演示应用程序硬件设置

使用随附的 USB 电缆将 CrossFire 主板连接到您的开发主机。如您之前没有安装，则会提示您[安装
CrossConnect 驱动程序](http://www.rowley.co.uk/arm/CrossConnect_Install/ReadMe.htm)。

演示应用程序使用内置在 CrossFire 评估板上的 LED ，因此不需要特定的硬件设置。

#### 构建并执行 RTOS 演示应用程序

通过从 "Build" 菜单中选择 "Build and Debug" ，或者直接按 F5 ，一步即可构建和下载 RTOS演示应用程序。项目
构建时应该不会报错或出现警告。

![](/media/2018/buildanddebug.gif)
构建和下载演示应用程序

#### 功能

演示应用程序包含以下任务：

* **“标准演示”任务集**
包括轮询队列、阻塞队列、信号量、数学任务和动态优先级任务。请参阅
 [RTOS演示页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)，了解详细信息。
* **打印任务**

 可从 CrossFire 评估板写入消息，以便在 CrossStudio 终端 IO 窗口中显示。为了确保对此功能的独占访问，
 只允许一个任务（打印任务）写入终端。其他想要显示消息的任务不直接执行此操作，
 而是将消息发送到打印任务。如果没有消息等待，打印任务将
 阻塞。
* **检查任务**

 检查任务定期执行。它监控标准演示任务，如果所有任务都
 顺利执行没有出错，则会通过打印任务写入"Pass" 到终端 IO ，如果在任何时候检测到错误，则写入“FAIL”。
* **按钮处理程序任务**
 按钮处理程序任务响应于 CrossFire 主板上标有 “BUT” 的按钮生成的中断而取消阻塞。每次执行按钮处理程序任务
 都会在终端 IO 窗口中显示任务状态信息表。包含按钮处理程序任务，
 以演示从中断服务程序内切换任务上下文。
* **LED 任务**
 该任务使 CrossFire LED 每秒闪烁一次。

正确执行时：
* LED 每秒闪烁一次。
* 每 5 秒打印 "PASS" 到终端IO。
* 每次按下 'BUT' 时，向终端 IO 打印任务状态信息。

示例输出：

```c

PASS
PASS
PASS
PASS

Task          State  Priority  Stack	#
************************************************
Button		R	3	99	21
PolSEM2		R	0	97	4
SUSP_RX		R	0	93	11
CNT_INC		R	0	102	7
QProdB2		R	0	94	13
QProdB3		R	0	94	14
QConsB6		R	0	94	17
QProdB5		R	0	94	16
IDLE		R	0	104	22
IntMath		R	0	102	0
Print		R	0	93	20
PolSEM1		R	0	97	3
C_CTRL		B	0	98	9
SUSP_TX		B	0	102	10
QProdNB		B	2	99	2
LED		B	2	102	18
BlkSEM1		B	1	90	5
BlkSEM2		B	1	96	6
QConsB1		B	2	99	12
QConsB4		B	2	99	15
Check		B	3	99	19
QConsNB		B	2	99	1
LIM_INC		S	1	103	8

PASS
PASS

```

### 配置和用法详情

本演示使用标准 FreeRTOS LPC2000 GCC 移植文件。请阅读 LPC2106 演示文件页面上的[配置与
使用](portlpc2106.md#ConfigAndUsage)部分，了解更多信息。
注意：RTOS调度器未安装默认中断处理程序（以处理虚假中断）。应确保应用程序已安装适当的处理程序。
