---
title: MPS2 (AN385) 上的 QEMU 仿真 ARM Cortex-M3 快速连接演示
---
由 FreeRTOS 提供

FreeRTOS 团队使用 MPS2 (AN385) 上的 QEMU 仿真 ARM Cortex-M3 创建了一个快速连接演示。该演示使用 AWS 服务来创建 AWS 账户和进行 AWS IoT 配置，以便将仿真设备连接到 [AWS IoT](https://aws.amazon.com/iot/)。连接完成后，将发送包含 1 和 0 交替的消息，从而可以模拟 AWS IoT 应用程序。


### 要开始 Quick Connect 演示，请执行以下操作：

**第 1 步：** [下载 QEMU](https://www.qemu.org/download)，并在 shell 路径中包含 `qemu-system-arm` 仿真器。要检查路径，请运行：“`which qemu-system-arm`” ，它应生成有效路径。  

 **Linux**：根据您的 Linux 发行版，您或许可以通过系统的软件包管理器获取 QEMU。如果您使用的是 Ubuntu，请运行 “`sudo apt install qemu-system`”。  

 **Mac**：您可以通过 Homebrew 获取 QEMU。如果尚未安装，请安装 [Homebrew](https://brew.sh/)，然后运行 “`brew install qemu`”。  

 **Windows**：在 powerhell 中运行 "`winget install qemu`" 命令。(如果你的机器上还没有安装 winget，请按照[以下说明](https://learn.microsoft.com/en-us/windows/package-manager/winget/#install-winget)操作。）接下来，确保已将 QEMU 添加到 PATH。您可以将目录添加到 PATH，方法是进入设置，搜索“编辑系统环境变量”。然后，点击右下角的“环境变量”按钮，双击名为“路径”的变量。最后，点击“新建”，将 qemu 目录（应位于程序文件中）添加到 PATH。  

**第 2 步：**要设置 QEMU 仿真板，请为要使用的计算机下载 Quick Connect 设置包。  

 对于 Windows：下载 [Quick_Connect_QEMU-windows.x64\.zip](https://qc-qemu-distribution.s3.us-west-2.amazonaws.com/Quick_Connect_QEMU-windows.x64.zip)  

 对于 Apple Silicon Macs：下载 [Quick_Connect_QEMU-macos(Arm).x64\.zip](https://qc-qemu-distribution.s3.us-west-2.amazonaws.com/Quick_Connect_QEMU-macos(Arm).x64\.zip)  

 对于 Intel Macs：下载 [Quick_Connect_QEMU-macos(Intel).x64\.zip](https://qc-qemu-distribution.s3.us-west-2.amazonaws.com/Quick_Connect_QEMU-macos(Intel).x64\.zip)  

 对于 Linux：下载 [Quick_Connect_QEMU-linux.x64\.zip](https://qc-qemu-distribution.s3.us-west-2.amazonaws.com/Quick_Connect_QEMU-linux.x64.zip)  

**第 3 步：**解压 Quick Connect 压缩包。在终端中，转到创建的文件夹（解压压缩包的位置），然后直接调用文件 "Start_Quick_Connect"（运行 "`./Start_Quick_Connect`"）。  

 **注意**：如果在尝试运行应用程序时收到警告，请参阅下面的故障排除部分。    

**第 4 步：**遵循并完成命令行界面中的所有提示。

**第 5 步：**"Start_Quick_Connect" 完成后，在同一个目录中创建一份名为 "CLICK-ME.html" 的文件。双击 "CLICK-ME.html" 以打开自定义 URL ，可以在其中查看仿真 ARM CM3 板上传感器的数据。
  **注意：**请忽略打开的 URL 中的“添加传感器图形”部分，并按照以下说明操作。   

### 要开始 Quick Connect 演示，请执行以下操作：


**第 1 步：** [下载 QEMU](https://www.qemu.org/download)，并在 shell 路径中包含 `qemu-system-arm` 仿真器。然后运行 “`which qemu-system-arm`” 以确保产生有效路径。  

 **注意**：按照上一节第 1 步中的说明在您的系统中安装 QEMU。  

**第 2 步：**下载 [ARM GNU 嵌入式工具链](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)，并在 shell 路径中包含 ARM 编译器 `arm-none-eabi-gcc`。然后运行 “`which arm-none-eabi-gcc`” 以确保产生有效路径。
  **注意**：这一步是最困难的，因为 ARM GNU 嵌入式工具链的最新版本目前不在任何软件包管理系统中。您需要在系统中下载嵌入式工具链 (arm-none-eabi)，将压缩包解压缩到您选择的目录中，然后将该目录添加到系统路径中。在 MacOS/Linux 系统中，将 “`export PATH=$PATH:<ARM toolchain directory>`” 添加到 shell 的配置文件中（通常是 `~/.bashrc` 或 `~/.zshrc`，但这取决于您自己的系统定制），然后运行 "`source <profile path>`"。  

 在 Windows 系统中，请参阅上一节“将 QEMU 添加到路径”中第 1 步的说明，按照相同步骤将此目录添加到系统路径中。  

**第 3 步：**下载[演示源代码](https://qc-qemu-distribution.s3.us-west-2.amazonaws.com/Quick_Connect_QEMU-source.zip)。源代码压缩文件包含二进制源（设备代码）。 


**第 4 步：**下载[ FreeRTOS 存储库](https://github.com/FreeRTOS/FreeRTOS/releases)，并提取存档。将下载的源代码压缩包(上一步)移至 FreeRTOS-Plus/Demo 文件夹,并提取存档。 


**第 5 步：**进入解压缩后的演示文件夹，按照其中 "README.md" 文件的说明来定制演示。完成自定义后，按照演示 "README.md" 中的说明重建演示。 


**第 6 步**：将生成的可执行文件（QuickConnect-Demo）从 "Quick_Connect_QEMU-source/build" 复制到 "Quick_Connect_QEMU-platformName.x64/Demo"，替换当前演示文件夹中的二进制文件。 


**第 7 步：**通过终端直接调用 "Start_Quick_Connect" 文件，重新运行该文件，查看所作更改。 

规格


QEMU 是一款通用的开源机器模拟器和虚拟器。该演示使用 QEMU 在使用 AN385 的 MPS2 上模拟 ARM Cortex-M3 MPU。


**硬件架构**
ARM (Cortex-M3)

**网络连接**
仅以太网

**安装/形状系数**
模拟

**操作系统**
FreeRTOS

**编程语言**
C/C++

### 故障排除：

**若运行应用程序时出现权限问题，可执行以下操作：**  

**Mac：**双击 “Quick Connect” 可执行文件后，根据您的安全设置，可能会看到一个弹出窗口，上面显示 "Start_Quick_Connect cannot be opened because it is from an unidentified developer" （无法打开 Start_Quick_Connect，因为它来自身份不明的开发商）。右键单击 Finder 应用程序中的 Start_Quick_Connect 文件，然后选择 "Open" （打开）选项。然后在弹出窗口中点击 "Open" （打开）按钮。  

**Windows：**双击 “Quick Connect” 可执行文件后，根据您的安全设置，可能会看到一个弹出页面，上面显示 "Windows protected your PC" （Windows 保护您的 PC）。请点击 "More Info" （更多信息）链接，查看 "Run anyway" （仍然运行）按钮。然后点击 "Run anyway" （仍然运行）按钮。

**杀毒软件问题：**  
您可能会遇到杀毒软件认为 `Start_Quick_Connect` 可执行文件是恶意软件的问题。这可能是因为演示将配置文件写入 `Demo` 文件夹中造成的。如果您的演示因为杀毒软件而被隔离，请将演示标记为可信任或在演示期间禁用杀毒软件。  
