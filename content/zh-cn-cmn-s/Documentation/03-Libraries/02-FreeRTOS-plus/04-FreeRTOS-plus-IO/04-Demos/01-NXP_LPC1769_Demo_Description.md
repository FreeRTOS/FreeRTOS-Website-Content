---
title: FreeRTOS-Plus-IO 和 FreeRTOS-Plus-CLI 演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

使用 [LPCXpresso 基板 BSP](/Documentation/03-Libraries/03-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/BSP/NXP/LPCXpresso-LPC1769-Base-Board)

## 简介

本页介绍了使用 FreeRTOS-Plus-IO 和 FreeRTOS-Plus-CLI 的两个演示应用程序
（在 [LPCXpresso Base Board BSP](/Documentation/03-Libraries/03-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/BSP/NXP/LPCXpresso-LPC1769-Base-Board) 上使用）。第二个演示集成了
lwIP 和 FatFS，为存储在 SD 卡上的文件提供了 “类似” Telnet 的命令行界面。

这些演示非常全面；如需简单的代码片段，
请参阅[快速示例](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/02-Quick-examples)页面以及大多数 FreeRTOS-Plus-IO
和 FreeRTOS-Plus-CLI 文档页面。

这些演示使用标准 FreeRTOS Cortex-M3 GCC 移植。重要的是，
希望在不使用 FreeRTOS-Plus-IO 的情况下使用该移植的用户应首先查阅移植文档，
以了解使用 FreeRTOS 中断嵌套模型所需的中断配置设置。
在 Cortex-M 设备上使用多任务内核时[最常见错误的常见问题解答](/Why-FreeRTOS/FAQs/Troubleshooting)
是一个很好的开始。


## FreeRTOS-Plus-IO 和 FreeRTOS-Plus-CLI 演示 1 功能

![FreeRTOS-Plus-IO and FreeRTOS-Plus-CLI 用于在 UART 上创建命令控制台并使用 I2C、SPI 和 GPIO 外围设备](/media/2018/FreeRTOS_UART_Command_Console_SPI_I2C_GPIO.jpg)
*相关跳线配置*

跳线必须正确设置！相关跳线设置如下图所示。

![LPCXpresso 基板上的跳线设置，用于正确配置 SPI 和 I2C](/media/2018/FreeRTOS_IO_CLI_Demo_1_Jumper1.jpg)

![LPCXpresso 基板上的跳线设置，用于正确配置 OLED 显示](/media/2018/FreeRTOS_IO_CLI_Demo_1_Jumper2.jpg)

![LPCXpresso 基板上的跳线设置，用于正确配置 7 段显示](/media/2018/FreeRTOS_IO_CLI_Demo_1_Jumper3.jpg)

如果您使用的是 ISP 引导加载程序，设置 J62 后，  还须移除 J54（可能仅
适用于 Rev B  基板）。

在此演示中，[FreeRTOS-Plus-CLI](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI) 和
FreeRTOS-Plus-IO 用于创建以下示例：


**命令控制台**

+ FreeRTOS-Plus-IO 和 FreeRTOS-Plus-CLI 用于创建命令  控制台。UART3 用于输入
  和输出。

+ FreeRTOS-Plus-IO  [零拷贝传输模式](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode)用于传输
  字符，中断  驱动的[字符队列传输模式](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode)
  用于接收字符。

+ 使用 FreeRTOS-Plus-CLI 注册了六条命令。这些命令分别为 run-time-stats、task-stats、echo-parameters、
  echo-3-parameters、create-task 和 delete-task。

+ 在命令控制台中输入 “run-time-stats”，查看每个任务自创建以来
  在运行状态中花费的时间。

+ 在命令控制台中输入 “task-stats”，可查看任务状态信息快照，包括
  堆栈高水位线数据。

+ 输入“echo-parameters”，然后输入一个或多个命令行，
  就可以看到回显参数的（可变）数量。该命令演示了如何定义和实现
  可接受任意数量参数的命令。

+ 输入 “echo-3-parameters”，然后输入三个命令行参数，
  就可以看到回显参数的（固定）数量。该命令演示了如何定义和实现
  需要精确参数数量的命令。

+ 输入 “create-task”，然后输入一个数字参数，
  即可创建一个接受所输入数字作为任务参数的任务。该任务将在开始执行时打印（到命令控制台）
  参数值。“task-stats”命令  可用于查看正在运行的附加任务。

+ 输入“delete-task” 删除使用 “create-task” 命令创建的任务。

+ 交付时，UART3 设置为 115200 波特、无起始位、8 个数据位和 1 个停止位。在基板上，
  UART3 通过 UART 至 USB 转换器连接到标有 X3 的微型 USB 连接器。  **用于连接目标的终端程序
  必须配置 为发送带有换行符的行尾。精选演示的第 1 版
  要求终端程序在本地回显键入的字符，第 2 版则不需要。**


**显示驱动程序**

+ FreeRTOS-Plus-IO 用于实现 OLED 显示驱动程序。  I2C2 外围设备用于输出，因此
  必须设置基板跳线，以针对 I2C 操作配置 OLED。

+ 该示例演示了用于[轮询](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/07-Polled_Transfer_Mode)
  和中断驱动[零拷贝](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode)传输模式的 I2C 移植。


**串行 EEPROM 接口**

+ FreeRTOS-Plus-IO 用于向连接到 I2C2 外设的 EEPROM 写入，然后再从 EEPROM 读回
  。

+ 该示例演示了 I2C 移植在[轮询](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/07-Polled_Transfer_Mode)
  和中断驱动[零拷贝](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode)传输模式下用于写入 EEPROM，
  以及在轮询和中断驱动[循环缓冲区](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/09-Circular_Buffer_Transfer_Mode)
  传输模式下用于从 EEPROM 读回。


**7 段显示器**

+ 此时 FreeRTOS-Plus-IO 与配置为 SPI 模式的 SSP 外设配合使用。
  [轮询传输模式](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/07-Polled_Transfer_Mode)用于
  定期向 7 段显示器写入递增数字。


**GPIO**

+ FreeRTOS 软件定时器用于  定期切换多色 LED。


---

## FreeRTOS-Plus-IO 和 FreeRTOS-Plus-CLI 演示 2 功能

![FreeRTOS-Plus-IO 和 FreeRTOS-Plus-CLI 用于在 telnet 套接字上创建命令控制台以访问文件系统。此外，还创建了一个 Web 服务器。](/media/2018/FreeRTOS_File_System_Telnet_Web_Server.jpg)
*相关跳线配置*

跳线必须正确设置！相关跳线设置如下图所示。**请注意，第一张
图片中的设置与演示 1 中显示的设置不同！**

![LPCXpresso 基板上的跳线设置，用于正确配置 SPI 和 I2C 演示 2](/media/2018/FreeRTOS_IO_CLI_Demo_2_Jumper1.jpg)

![LPCXpresso 基板上的跳线设置，用于正确配置 OLED 显示 演示 2](/media/2018/FreeRTOS_IO_CLI_Demo_1_Jumper2.jpg)

![LPCXpresso 基板上的跳线设置，用于正确配置 7 段显示 演示 2](/media/2018/FreeRTOS_IO_CLI_Demo_1_Jumper3.jpg)

如果您使用的是 ISP 引导加载程序，设置 J62 后，还须移除 J54（可能仅
适用于 Rev B  基板）。

在此演示中，[FreeRTOS-Plus-CLI](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)、
FreeRTOS-Plus-IO、[lwIP](http://savannah.nongnu.org/projects/lwip) 
 和 [FatFS](http://elm-chan.org/fsw/ff/00index_e.html) 用于创建以下示例。**注意：
 必须插入 SD 卡 才能运行此演示**！


**适用于 FAT 文件系统的 SD 卡 MMC 驱动程序**

+ 使用 SPI 接口的 SD 卡上有一个 FAT 兼容文件系统。FreeRTOS-Plus-IO
  API 与 SSP 外围设备搭配使用，以提供必要的输入和输出。FatFS 用于
  提供文件系统功能。

+ 该示例演示了
  使用所有可用的  [FreeRTOS-Plus-IO 传输模式](/Documentation/03-Libraries/03-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes)向 SD 卡写入和从 SD 卡读取文件的过程。文件名
  用于表示创建文件时使用的模式，  每种模式创建 20 份文件
  。

+ 可  使用 FreeRTOS-Plus-CLI 列出和操作这些文件，详见下文。


**Telnet“类似”命令控制台**

+ FreeRTOS-Plus-CLI 在  标准 telnet TCP/IP 端口（端口 23）上创建命令控制台。lwIP 套接字
  API 用于提供 TCP/IP 实现。

+ 命令控制台使用 telnet 端口号，可以使用标准 telnet 客户端进行访问，
  但不是完整的 telnet 服务器。

+ 示例使用的是
  使用 FreeRTOSConfig.h 中定义的 configIP_ADDR0-configIP_ADDR3 常量配置的静态 IP 地址。

+ 使用 FreeRTOS-Plus-CLI 注册了五条命令。它们是用于操作
  文件系统的 dir、copy 和 del（见上文），以及用于查看 FreeRTOS 任务信息的 run-time-stats 和 task-stats。

+ 在命令控制台输入 “dir”，查看文件系统目录列表。

+ 在命令控制台输入 “del \\\<filename/>”，从 SD 卡中删除文件。

+ 在命令控制台输入 “copy \<source_file> \<destination_file>”，复制文件。

+ 在命令控制台中输入 “run-time-stats”，查看每个任务自创建以来
  在运行状态中花费的时间。

+ 在命令控制台中输入 “task-stats”，可查看任务状态信息快照，包括
  堆栈高水位线数据。

+ **用于连接目标的终端程序必须配置为在本地发送带有换行
  符和回显键入字符的行尾。**


**Web 服务器**

+ lwIP RAW API 用于创建一个简单的 Web 服务器。Web 服务器使用服务器端包含（SSI）
  来显示  任务状态和运行时间信息。


**GPIO**

+ FreeRTOS 软件定时器用于  定期切换多色 LED。


### 源文件和项目文件下载链接

构建这两个项目所需的所有源文件都包含在
[同一压缩文件](http://interactive.freertos.org/attachments/token/xupqqaau9ixtslj/?name=LPC1769_FreeRTOS_Plus_Featured_Demo_002.zip)中。


### 硬件平台和软件工具

这两个演示均配置为在装有 LPCXpresso 基板的 LPCXpresso LPC1769 CPU 板上运行。
[LPCXpresso IDE](https://www.nxp.com/design/design-center/development-boards-and-designs/lpcxpresso-boards:LPCXPRESSO-BOARDS) 用于构建、闪存和调试
应用程序。


### 构建说明

1. 启动 [LPCXpresso IDE](https://www.nxp.com/design/design-center/development-boards-and-designs/lpcxpresso-boards:LPCXPRESSO-BOARDS)。新建工作区，
   或在出现提示时选择现有工作区。

2. 在 IDE 的 "File" 菜单中选择 "Import"，然后选择 "Existing Projects Into Workspace"，
   如下图所示，然后点击 “Next”。

   ![在 LPCXpresso IDE 中选择 Existing Project Into Workspace](/media/2018/LPCXpresso_Existing_Project_Into_Workspace.jpg)
   *在 Import 对话框中选择 "Existing Projects Into Workspace"*

3. 单击 "Select Archive File" 单选按钮，**确保选中 "Copy projects into workspace" 复选框
   **，然后导航到并选择在第一步中下载的压缩文件。

   对话框将列出一些项目文件。确保选中所有项目，然后单击
   “Finish”。导入过程将尝试多次创建某些文件，因此会显示一个对话框，
   警告文件可能被覆盖。出现这种情况时，
   只需选择 “No to all” 选项即可。

   ![所有项目都需要导入。](/media/2018/LPCXpresso_Selecting_All_Projects.jpg)
   *确保选中每个项目，因为构建应用程序需要所有项目。*

4. 导入的项目将出现在 LPCXpresso IDE 的项目浏览器窗口中。要构建演示 1，
   请在项目浏览器中选择 “FreeRTOS-Plus-Demo-1”，然后从 IDE 的 “Project” 菜单中选择 “Build Project”
   。构建 FreeRTOS-Plus-Demo-1 将导致其所有从属项目也被构建。

    同样，要构建项目 2，请先在项目窗口中选择 “FreeRTOS-Plus-Demo-2”，
    然后再从 IDE 的 “Project” 菜单中选择 “Build Project”。

   ![构建项目 1 的方法：选择 FreeRTOS-Plus-Demo-1，然后选择 "Build Project"。](/media/2018/Building_Project_1.jpg)
   *在项目资源管理器中先选择 FreeRTOS-Plus-Demo-1，然后选择 "Build Project"*


### 连接硬件并启动调试会话

项目构建成功后：

1. 在 LPCXpresso 基板的 USB 接口和主机之间连接 USB 电缆。只有在首次连接完成后，
   才能在 LPCXpresso CPU 板上的调试 USB 接口和主机之间
   连接第二条 USB 电缆。**注意：**要成功启动调试会话，
   此连接顺序非常重要。

2. 每个演示需要的跳线设置稍微不同。跳线设置如图所示，
   紧挨着上面的演示说明。确保为所选演示正确设置跳线，如果选择的是演示 2，
   还要确保已将 SD 卡插入基板上的相关连接器
   （如果没有，演示将无法运行！）。

3. 单击 LPCXpresso IDE 中的调试速度按钮启动调试会话。

   ![LPCXpresso IDE 中的调试速度按钮](/media/2018/Debug-speed-button.jpg)
   *LPCXpresso IDE 中调试速度按钮的位置*


### 浏览项目和目录

工作区包含以下五个项目：

+ CMSISv2p00_LPC17xx

  NXP 为 LPC17xx 系列微控制器提供的  标准 CMSIS 库。

+ lpc17xx.cmsis.driver.library

  这是 NXP 为 LPC17xx 系列微控制器提供的外设驱动程序库。它
  部分由 FreeRTOS-Plus-IO LPC17xx 移植层使用。它对 NXP 自己发布的代码
  进行了极少的修改。

+ FreeRTOS-产品

  包含 FreeRTOS 实时内核、FreeRTOS-Plus-CLI 和 FreeRTOS-Plus-IO
  代码，分别放置在三个单独的目录中。请注意，此项目实际上  并不是直接构建的——
  它所包含的源代码只是被两个演示应用程序项目所引用。演示项目使用
  工作区相对路径引用文件，因此项目
  仅在位于工作区目录中时才会构建。

+ FreeRTOS-Plus-Demo-1

  该项目包含演示 1 应用程序代码本身，该代码又使用
  来自 FreeRTOS-Products 目录的源文件。

+ FreeRTOS-Plus-Demo-2

  该项目包含演示 2 应用程序代码本身，包括 FatFS 和 lwIP 源文件。
  该项目使用来自 FreeRTOS-Products 目录的源文件。


### 软件组件许可

FreeRTOS-Plus-IO 和 FreeRTOS-Plus-CLI 根据各自的开源
[许可](/Documentation/03-Libraries/03-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/05-FreeRTOS_Plus_IO_License) 提供。

lwIP 和 FatFS 是第三方开源产品，根据各自的许可条款提供。

