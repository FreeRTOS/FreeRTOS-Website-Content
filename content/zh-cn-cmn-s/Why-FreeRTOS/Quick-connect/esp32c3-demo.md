---
title: ESP32c3 快速连接演示
---

由 Espressif 提供

ESP32-C3 配置为与 AWS Quick Connect 演示配套使用。该演示使用 AWS 服务 
来创建 AWS 账户和进行 AWS IoT 配置，以便将您的设备 
连接到 [AWS IoT](https://aws.amazon.com/iot/)。连接后，将从设备发送包含从传感器收集的数据的消息， 
从而允许您模拟 AWS IoT 应用程序。


### 要开始 Quick Connect 演示，请执行以下操作：

+ **第 1 步：**

  使用 USB 2.0 连接线 (Micro B) 将 ESP32-C3 连接到计算机。 

+ **第 2 步：**

  下载用于设置 ESP32-C3 板的计算机的 Quick Connect 安装包：  

  + 下载 [QuickConnect_Espressif-ESP32C3_windows.x64\.zip](https://github.com/espressif/aws-quickconnect/raw/main/bin/QuickConnect_Espressif-ESP32C3_windows.x64.zip) 
    （Windows   
     支持的版本）
  + 下载 [QuickConnect_Espressif-ESP32C3_macos.x64.tar.gz](https://github.com/espressif/aws-quickconnect/raw/main/bin/QuickConnect_Espressif-ESP32C3_macos.x64.tar.gz) 
    （Mac   
     支持的版本）
  + 下载 [QuickConnect_Espressif-ESP32C3_linux.x64.tar.gz](https://github.com/espressif/aws-quickconnect/raw/main/bin/QuickConnect_Espressif-ESP32C3_linux.x64.tar.gz) 
    （Linux   
     支持的版本）

+ **第 3 步：**

  如您为 Windows 用户，请下载并安装 USB 转 UART 虚拟通信端口驱动程序， 
  该驱动程序可在[此处](https://www.silabs.com/documents/public/software/CP210x_Windows_Drivers.zip)找到。  

  对于 Linux 用户，当前登录的用户应具有通过 USB 对串行端口进行读写访问的权限 
  。对于大多数 Linux 发行版， 
  可通过以下命令将用户添加到拨出组来实现：  

  ```c
  sudo usermod -a -G dialout $USER
  ```
  请确保重新登录以启用对串行端口的读写权限。  
  

+ **第 4 步：**

  解压缩快速连接存档，然后运行 START_QUICK_CONNECT 文件。  

  注意：在尝试运行应用程序时，您可能会收到警告。如果出现警告，请参阅下面的故障排除部分 
  。


+ **第 5 步：**

  遵循并完成命令行界面中的所有提示。
  注意：此主板仅支持 2.4 GHz 无线网络连接。


+ **第 6 步：**

  "Start_Quick_Connect" 完成后，在同一个目录中创建一份名为 "CLICK-ME.html" 的文件。 
  双击 CLICK-ME.html 以打开自定义 URL ，可以在其中查看 ESP32-C3 板上传感器的数据 
  。 


### 规格

![](/media/2021/ESP32-C3.png)   
 ESP32-C3-DevKitC-02 
是基于 [ESP32-C3-WROOM-02](https://www.espressif.com/sites/default/files/documentation/esp32-c3-wroom-02_datasheet_en.pdf) 的入门级开发板， 
其中 ESP32-C3-WROOM-02 是带有 4 MB SPI 闪存的通用模块。这款主板集成了完整的 Wi-Fi 和蓝牙 LE 功能。 
ESP32-C3 专为实现简单、安全的连接应用而设计，是一款基于 RISC-V 的单核 32 位 MCU， 
具有 400 KB 的 SRAM，能够以 160MHz 的频率运行。它集成有 2.4 GHz Wi-Fi 和蓝牙 5 (LE) ， 
并提供远程支持。具有 22 个可编程 GPIO，并支持 ADC、SPI、UART、I2C、I2S、RMT、TWAI 和 PWM。


**硬件架构**   
RISC-V

**网络连接**   
仅支持 Bluetooth LE (BLE)、Sub-GHz、Wi-Fi 2.4 GHz

**安装/形状系数**   
嵌入式

**操作系统**   
FreeRTOS

**安全性**   
安全启动、闪存加密、数字签名和 HMAC 外设

**供电**   
USB 供电

[了解更多](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/hw-reference/esp32c3/user-guide-devkitc-02.html)

**I/O 接口**   
可编程 GPIOs、SPI、UART、USB、I2C、I2S、PWM、JTAG、GDMA、TWAI、ADC

**环境**   
扩展

**编程语言**   
C/C++

**存储**   
Flash/SRAM


### 故障排除：

#### 若运行应用程序时出现权限问题，可执行以下操作：

**Windows：**   
双击 “Quick Connect” 可执行文件后，根据您的安全设置， 
可能会看到一个弹出页面，上面显示 "Windows protected your PC" （Windows 保护您的 PC）。请点击 "More info" （更多信息）链接，查看 "Run anyway" （仍然运行） 
按钮。然后单击 "Run anyway" （仍然运行）按钮。  

**Mac：**   
双击 “Quick Connect” 可执行文件后，根据您的安全设置， 
可能会看到一个弹出窗口，上面显示 "Start_Quick_Connect cannot be opened because it is from an unidentified developer" （无法打开 Start_Quick_Connect，因为它来自身份不明的开发商） 
。右键单击 Finder 应用程序中的 Start_Quick_Connect 文件，然后选择 "Open" （打开）选项。 
然后在弹出窗口中点击 "Open" （打开）按钮。  
