---
title: AWS Quick Connect 演示
---
**这是一个旨在进行短期演示的应用程序，不提供数据隐私方面的保障。注册 AWS 账户后，您将能够使用包括数据隐私在内的众多新特性与功能。了解有关[注册 AWS 账户](https://docs.aws.amazon.com/accounts/latest/reference/accounts-welcome.html)的更多信息。**

借助 Quick Connect 演示，可以轻松设置合作伙伴提供的 FreeRTOS 认证的开发板并将其连接到 
[AWS IoT](https://aws.amazon.com/iot/)，只需短短几分钟，无需安装和配置工具链， 
无需安装依赖项，无需下载和构建源代码，也无需设置和配置 AWS 账户 
和 AWSIoT。设备连接后，即可 
向 AWS IoT 发送消息，进而模拟 IoT 应用程序。此外，可以选择修改 
演示源代码，然后使用所选开发板的构建系统和工具构建并刷新演示， 
并立即看到代码更改对演示应用程序的影响。 

这些模拟可在 7 天内用于非生产性应用程序，以探索 IoT 空间。 
使用 Quick Connect 连接设备，即表示您同意 
[AWS 客户协议](https://aws.amazon.com/agreement/) 和 
[隐私声明](https://aws.amazon.com/privacy/)。 

受支持的开发板如下所示。新的开发板一经推出，会陆续添加。 

LTS：使用 FreeRTOS LTS 库的开发板。[了解有关 LTS 的更多信息。](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries)


### 支持的板

| 板名称 | 制造商 | LTS 库 | Quick Connect |
| ---------- | ------------ | ------------- | ------------- |
| [STM32L4+ Discovery Kit IoT Node](/Why-FreeRTOS/Quick-connect/stm32l4-demo) |  STMicroelectronics  | [coreMQTT](https://github.com/FreeRTOS/coreMQTT/tree/v1.1.0)、[backoffAlgorithm](https://github.com/FreeRTOS/backoffAlgorithm/tree/v1.0.0) | [连接板](/Why-FreeRTOS/Quick-connect/stm32l4-demo) |
| [ESP32-C3-DevKitC-02](/Why-FreeRTOS/Quick-connect/esp32c3-demo) |  Espressif  | [coreMQTT](https://github.com/FreeRTOS/coreMQTT/tree/v1.1.0) | [连接板](/Why-FreeRTOS/Quick-connect/esp32c3-demo) |
| [QEMU MPS2-AN385](/Why-FreeRTOS/Quick-connect/qemu-mps2-an385-demo) | FreeRTOS | [coreMQTT](https://github.com/FreeRTOS/coreMQTT/tree/v1.1.0)、[backoffAlgorithm](https://github.com/FreeRTOS/backoffAlgorithm/tree/v1.0.0) | [启动仿真器](/Why-FreeRTOS/Quick-connect/qemu-mps2-an385-demo) |
