---
title: STM32L4+ Quick Connect 演示
---

由 STMicroelectronics 提供


STM32L4+ 已配置为与 AWS Quick Connect 演示配套使用。此演示使用 AWS 服务 
创建 AWS 账户并配置 AWS IoT，以将设备连接到 
[AWS IoT](https://aws.amazon.com/iot/)。连接后，设备会发送包含从传感器收集的数据的消息， 
让您可以模拟 AWS IoT 应用程序。


### 要开始 Quick Connect 演示，请执行以下操作：

+ **第 1 步：**

  使用 USB 2.0 连接线 (Micro B) 将 STM32L4+ Discovery 套件连接到计算机。（请查看制造商随开发板一起提供的文档， 
  了解要使用的正确 USB 端口。）


+ **第 2 步：**

  针对要用来设置 STM32L4+ 开发板的计算机，下载相应的 Quick Connect 安装包：  

  + 下载 [quickconnect-st-windows.x64\.zip](https://www.st.com/content/dam/AME/2021/mdg/quickconnect-st-windows.x64.zip) 
    （如为 Windows 系统）。  

  + 下载 [quickconnect-st-linux.x64.tar.gz](https://www.st.com/content/dam/AME/2021/mdg/quickconnect-st-linux.x64.tar.gz) 
    （如为 Linux 系统）。  

  + 下载 [quickconnect-st-macos.x64.tar.gz](https://www.st.com/content/dam/AME/2021/mdg/quickconnect-st-macos.x64.tar.gz) 
    （如为 Mac 系统）。  

  注意：如果使用 DIS_L4S5VI (BL4S5IIO01A$CU2) 版本的 STM32L4+ Discovery 套件， 
  Mac 用户在更新设备上的凭据时可能会遇到问题。如果出现问题，请参阅下文故障排除部分。

+ **第 3 步：**

  如为 Windows 用户， 
  请点击[此处](https://os.mbed.com/teams/ST/wiki/ST-Link-Driver)下载并安装 ST-Link USB 驱动程序。  

  如果使用 Linux 系统，当前登录的用户可通过 USB 对串行端口进行读写访问 
  。在大多数 Linux 发行版中，如需执行读写操作，可使用以下命令 
  将用户添加到 dialout 组：  

  ```
  sudo usermod -a -G dialout $USER
  ```

  请确保重新登录，以启用对串行端口的读写权限。  
  

+ **第 4 步：**

  解压 Quick Connect 存档，然后运行 Start_Quick_Connect 文件。   

  注意：尝试运行应用程序时，您可能会收到警告。如果出现警告，请参阅下文故障排除部分 
  。


+ **第 5 步：**

  按照命令行界面中的所有提示进行操作。   

  注意：此开发板仅支持 2.4 GHz WiFi 连接。在配置过程中，设备将多次断开连接/重新连接， 
  这是正常现象。

+ **第 6 步：**

  Start_Quick_Connect 完成后，系统将在同一目录中创建一份名为 CLICK-ME.html 的文件。 
  双击 CLICK-ME.html 打开自定义 URL，查看 STM32L4+ 开发板上的传感器提供的数据 
  。 


### 规格

![](/media/2021/stm32l4.jpeg)   
B-L4S5I-IOT01A Discovery 套件 IoT 节点基于搭载 ARM® Cortex®-M4 核心的 STM32L4S5 构建， 
可 
为 AWS IoT 提供低功耗的安全通信、集成多路传感和开箱即用的支持，从而有助于开发各种互联应用程序。

**硬件架构**   
ARM

**网络连接**   
Bluetooth LE (BLE)、NFC、Sub-GHz、仅 2.4 GHz Wi-Fi

**安装/外形尺寸**   
嵌入式

**操作系统**   
FreeRTOS

**安全服务**   
防火墙、SSL/TLS

**电源**   
USB 供电

[了解更多](https://devices.amazonaws.com/detail/a3G0h0000087pwWEAQ/STM32L4-Discovery-Kit-IoT-Node)


**I/O 接口**   
ADC、Arduino、隔离式 GPIO、I2C、I2S、JTAG/SWD、Pmod、PWM、SDIO、传感器/MEMS、SPI、UART、USB


**环境**   
可扩展


**编程语言**   
C/C++


**存储**   
闪存/NVRAM


**可用地区**   
亚太地区、澳大利亚、加拿大、中国、欧洲、中东和非洲、欧盟、日本、韩国、拉丁美洲、新西兰、英国、美国


### 故障排除：

#### 如果运行应用程序时出现权限问题，请执行以下操作：

**Windows：**   
双击 Start_Quick_Connect.exe 启动实用程序后， 
根据其安全设置，Windows 10 用户可能会看到一个弹窗，提示“Windows 正在保护您的电脑”。解决方法是 
单击该窗口中的“更多信息”链接， 
然后单击显示的 "Run anyway"（仍然运行）按钮。  

**Mac：**  
双击 Start_Quick_Connect.exe 启动实用程序后， 
根据其安全设置，Mac 用户可能会看到一个弹窗，提示“Start_Quick_Connect 
来自身份不明的开发人员，无法打开”。解决方法是在 Finder 应用程序中右键单击 START_QUICK_CONNECT 文件， 
选择 "Open" （打开）选项，然后在弹出窗口中点击 "Open" （打开）按钮。  


#### 构建项目时出现“权限不足”错误：

`"../../prebuild.sh" "../.."
/bin/sh: ../../prebuild.sh: Permission denied
make[1]: ** [makefile:96: pre-build] Error 126*
*make:* * [makefile:64: all] Error 2
"make all" terminated with exit code 2. Build might be incomplete.`  

**解决方案：**   
`cd /Projects/B-L4S5I-IOT01A/Applications/BootLoader\_STSAFE/2\_Images\_SECoreBin
chmod +x STM32CubeIDE/*`
  

#### 构建错误：无法导入模块：

**解决方案：**  

1. 确保已安装以下模块：pycryptodomex、lief、ecdsa、numpy、argparse。如果 
   缺少任何模块，请运行以下命令进行下载：  `pip install <module_name>`   
  
2. 确保环境中使用的 Python 版本为 3.7 或更高版本。  

   如果不是，请将 Projects/B-L4S5I-IOT01A/Applications/BootLoader_STSAFE/2_Images_SECoreBin/STM32CubeIDE/prebuild.sh 中的 `cmd=python` 
   替换为 
   `cmd=python**3**`（或其他适当的命令）
   

#### STM32CubeProgrammer 错误：

`Generating the global elf file (SBSFU and userApp)
fix access path to STM32_Programmer_CLI
../../../../BootLoader_STSAFE/2_Images_SECoreBin/STM32CubeIDE/postbuild.sh: line 96: -ms: command not found`  

**解决方案：**  
通过以下任一方式将 STM32CubeProgrammer 添加到您的路径：  

1. 将以下行添加到 postbuild.sh：  

   `export PATH=$PATH:/Applications/STMicroelectronics/STM32Cube/STM32CubeProgrammer
   /STM32CubeProgrammer.app/Contents/MacOs/bin`  
   

2. 将其永久添加到 /etc/paths：  

   在文本编辑器中打开 /etc/paths。将 `/Applications/STMicroelectronics/STM32Cube/STM32CubeProgrammer
   /STM32CubeProgrammer.app/Contents/MacOs/bin` 附加到文件末尾。    


#### 无法连接到 AWS 或 WiFi：

**解决方案：**  

1. 断开开发板与计算机的连接，然后重新连接。   

2. 再次运行 Start_Quick_Connect。
  

#### 使用 WiFi 凭据配置开发板时出错：

**解决方案：**  

1. 断开/重新连接开发板，然后重试。   

2. 手动将 AWS_Config bin 复制/粘贴到设备文件夹，按照提示输入 
   WiFi SSID 和密码，然后再次运行 Start_Quick_Connect。
