---
title: AWS 参考集成
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么选择 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


AWS 参考集成指的是预集成的 FreeRTOS 项目，移植入基于微处理器的 
评估板，这些板能够演示与云端的端对端连接。AWS 参考集成帮助节省 
长达数月的开发工作，并缩短上市时间。   


### 选择 AWS 参考集成

下文的 AWS 参考集成演示了到 
[AWS IoT 核心](https://aws.amazon.com/iot-core/)的端对端连接。请参阅 
[AWS 合作伙伴设备目录](https://devices.amazonaws.com/search?sv=freertos)，了解更多详情。
如果您希望将主板认定为 AWS 参考集成，请参阅 
[AWS 设备认证程序](https://aws.amazon.com/partners/dqp/)。

LTS 这些是使用 FreeRTOS LTS 库的板。[进一步了解 LTS](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries)。

| 硬件合作伙伴 | 开发板 |
| ---------------- | ----------------- |
| A |
| 晶心科技股份有限公司 (Andes Technology Corporation) | * [Corvette-F1 N25](https://devices.amazonaws.com/detail/a3G0h0000077Y9QEAU/Corvette-F1-N25)<br/> |
| C |
| Cypress Semiconductor | * LTS[CYW943907AEVAL1F](https://devices.amazonaws.com/detail/a3G0L00000AAPg0UAH/CYW943907AEVAL1F)<br/>* LTS[CYW954907AEVAL1F](https://devices.amazonaws.com/detail/a3G0L00000AAPg5UAH/CYW954907AEVAL1F)<br/>* [PSoC 6 Wi-Fi BT 原型套件](https://devices.amazonaws.com/detail/a3G0h0000076tb9EAA/PSoC-6-Wi-Fi-BT-Prototyping-Kit)<br/>* [PSoC 6 Wi-Fi BT Pioneer 套件](https://devices.amazonaws.com/detail/a3G0h0000077kBoEAI/PSoC%C2%AE-6-WiFi-BT-Pioneer-Kit)<br/>* LTS[PSoC 64 标准安全 AWS Wi-Fi Bluetooth Pioneer 套件](https://devices.amazonaws.com/detail/a3G0h0000088AgXEAU)<br/> |
| E |
| 乐鑫科技 (Espressif Systems) | * [ESP32-PICO-KIT V4，适用于 FreeRTOS](https://devices.amazonaws.com/detail/a3G0L00000AANvnUAH/ESP32-PICO-KIT-V4-for-Amazon-FreeRTOS)<br/>* LTS[ESP-WROVER-KIT](https://devices.amazonaws.com/detail/a3G0L00000AANtlUAH/ESP-WROVER-KIT)<br/>* [ESP32-SOLO-1](https://devices.amazonaws.com/detail/a3G0h0000076lSMEAY/ESP32-SOLO-1)<br/>* LTS[ESP32-WROOM-32 DevKitC](https://devices.amazonaws.com/detail/a3G0L00000AANtjUAH/ESP32-WROOM-32-DevKitC)<br/>* [ESP-EYE](https://devices.amazonaws.com/detail/a3G0h0000077i2JEAQ/ESP-EYE)<br/>* LTS[ESP32-WROOM-32SE](https://devices.amazonaws.com/detail/a3G0h0000077nRtEAI/ESP32-WROOM-32SE)<br/>* LTS[ESP32-S2-SAOLA-1](https://devices.amazonaws.com/detail/a3G0h00000AkFngEAF/ESP32-S2-Saola-1)<br/>* [ESP32-Vaquita-DSPG](https://devices.amazonaws.com/detail/a3G0h0000087uKdEAI/ESP32-Vaquita-DSPG)<br/> |
| G |
| GigaDevice Semiconductor | * [GD32450Z-EVAL](https://devices.amazonaws.com/detail/a3G0h0000078ZAFEA2/GD32450Z-EVAL)<br/>* [GD32207i-EVAL](https://devices.amazonaws.com/detail/a3G0h00000882ahEAA/GD32207i-EVAL)<br/> |
| I |
| Infineon Technologies（英飞凌科技） | * LTS[XMC4800 IoT FreeRTOS 连接套件 WiFi](https://devices.amazonaws.com/detail/a3G0L00000AANsbUAH/XMC4800-IoT-Amazon-FreeRTOS-Connectivity-Kit-WiFi)<br/>* LTS[OPTIGA™ Trust X 安全解决方案](https://devices.amazonaws.com/detail/a3G0h000007712QEAQ/OPTIGA%E2%84%A2-Trust-X-Security-Solution)<br/>* [XENSIV™ 预测性维护套件](https://devices.amazonaws.com/detail/a3G0h00000Ak1uiEAB/XENSIV-Predictive-Maintenance-Kit-EVAL_XMC47_PREDMAIN_AA)<br/> |
| M |
| M5Stack Technology Co., Ltd | * [M5StickC](https://devices.amazonaws.com/detail/a3G0h0000077kOjEAI/M5StickC)<br/> |
| 联发科技 (MediaTek) | LTS* [MT7697Hx 开发套件](https://devices.amazonaws.com/detail/a3G0L00000AAOmPUAX/MT7697Hx-Development-Kit)<br/> |
| Microchip Technology | * LTS[Curiosity PIC32MZ EF FreeRTOS Bundle](https://devices.amazonaws.com/detail/a3G0L00000AANscUAH/Curiosity-PIC32MZ-EF-Amazon-FreeRTOS-Bundle)<br/>* [Curiosity PIC32MZ EF 2.0 开发板](https://devices.amazonaws.com/detail/a3G0h0000077I69EAE/Curiosity-PIC32MZ-EF-2.0-Development-Board)<br/>* [PIC32MZW1 Curiosity 板](https://devices.amazonaws.com/detail/a3G0h000007dl7rEAA/PIC32MZW1)<br/>* [SAM E54 Xplained Pro](https://devices.amazonaws.com/detail/a3G0h0000077I6kEAE/SAM-E54-Xplained-Pro)<br/>* [SAM E70 Xplained Ultra 评估套件](https://devices.amazonaws.com/detail/a3G0h0000077I6TEAU/SAM-E70-Xplained-Ultra-Evaluation-Kit)<br/>* [SAM G55 Xplained Pro 评估套件](https://devices.amazonaws.com/detail/a3G0h000007dnluEAA/SAMG55)<br/> |
| N |
| Nordic Semiconductor | * LTS[nRF52840 开发套件](https://devices.amazonaws.com/detail/a3G0L00000AANtrUAH/nRF52840-Development-Kit)<br/> |
| Nuvoton | * LTS[NuMaker-IoT-M487](https://devices.amazonaws.com/detail/a3G0h000000Tg9cEAC/NuMaker-IoT-M487)<br/>* [NuMaker-IoT-M487-Cellular 套件](https://devices.amazonaws.com/detail/a3G0h000007dhlHEAQ/NuMaker-IoT-M487-Cellular-Kit)<br/> |
| NXP Semiconductors | * LTS[LPC54018 IoT 解决方案](https://devices.amazonaws.com/detail/a3G0L00000AANtAUAX/LPC54018-IoT-Solution)<br/>* [FRDM-K64F 自由开发平台](https://devices.amazonaws.com/detail/a3G0h0000076fXUEAY/FRDM-K64F-Freedom-Development-Platform)<br/>* [MIMXRT1060-EVK](https://devices.amazonaws.com/detail/a3G0h0000076aV1EAI/MIMXRT1060-EVK)<br/>* [MIMX1050RT-EVKB](https://devices.amazonaws.com/detail/a3G0h0000076aUwEAI/MIMX1050RT-EVKB)<br/>* LTS[MW322 AWS IoT 入门套件](https://devices.amazonaws.com/detail/a3G0h000000OblKEAS/MW322-AWS-IoT-Starter-Kit)<br/>* LTS[MW320 AWS IoT 入门套件](https://devices.amazonaws.com/detail/a3G0h000000OaRnEAK/MW320-AWS-IoT-Starter-Kit)<br/> |
| R |
| Realtek | * [Realtek Ameba Z2](https://devices.amazonaws.com/detail/a3G0h000000OsmEEAS/Realtek-ameba-z2)<br/>* [Realtek Ameba D](https://devices.amazonaws.com/detail/a3G0h00000AjtR1EAJ/Realtek-Ameba-D)<br/> |
| Renesas Electronics（瑞萨电子） | * LTS[Renesas 入门套件+，适用于 RX65N-2MB](https://devices.amazonaws.com/detail/a3G0L00000AAOkeUAH/Renesas-Starter-Kit+-for-RX65N-2MB)<br/>* [RX65N 云套件](https://devices.amazonaws.com/detail/a3G0h000000P0lFEAS/RX65N-Cloud-Kit)<br/>* [RZ A2M 评估板套件](https://devices.amazonaws.com/detail/a3G0h0000076z53EAA/RZ-A2M-Evaluation-Board-Kit)<br/>* [RX72N Envision 套件](https://devices.amazonaws.com/detail/a3G0h000007dJazEAE/RX72N-Envision-Kit)<br/>* [RL78 G14 快速原型开发板](https://devices.amazonaws.com/detail/a3G0h00000EU3d2EAD/RL78-G14-Fast-Prototyping-Board)<br/>* [EK-RA6M3 评估套件](https://devices.amazonaws.com/detail/a3G0h000007dmC5EAI/EK-RA6M3-Evaluation-Kit)<br/> |
| S |
| 深圳市汇顶科技有限公司 | * [GR5515-SK 入门套件](https://devices.amazonaws.com/detail/a3G0h0000077UTNEA2/GR5515-SK-Starter-Kit)<br/> |
| SiFive | * [SiFive Learn Inventor](https://devices.amazonaws.com/detail/a3G0h0000077I8lEAE/SiFive-Learn-Inventor)<br/> |
| STMicroelectronics | * [SensorTile 无线工业节点开发套件](https://devices.amazonaws.com/detail/a3G0h0000077mTPEAY/SensorTile-Wireless-Industrial-Node-development-kit)<br/>* [STM32 NUCLEO-H743ZI 开发板](https://devices.amazonaws.com/detail/a3G0L00000AAOOBUA5/STM32-NUCLEO-H743ZI-Development-Board)<br/>* LTS[STM32L4 Discovery 套件 IoT 节点](https://devices.amazonaws.com/detail/a3G0L00000AANsWUAX/STM32L4-Discovery-Kit-IoT-Node)<br/>* [STM32L4+ Discovery 套件 IoT 节点](https://devices.amazonaws.com/detail/a3G0h0000087pwWEAQ/STM32L4+-Discovery-Kit-IoT-Node)<br/>* [STM32 NUCLEO-F767ZI 开发板](https://devices.amazonaws.com/detail/a3G0h0000087Y0MEAU/STM32-NUCLEO-F767ZI-Development-Board)<br/>* [STEVAL-STMODLTE](https://devices.amazonaws.com/detail/a3G0h000007dfiNEAQ/STEVAL-STMODLTE)<br/>* [STM32 Nucleo-STM32WB55RG](https://devices.amazonaws.com/detail/a3G0h000007dbjJEAQ/STM32-Nucleo-STM32WB55RG)<br/>* [X-NUCLEO-BNRG2A1](https://devices.amazonaws.com/detail/a3G0h00000AjrKdEAJ/X-NUCLEO-BNRG2A1)<br/> |
| T |
| Texas Instruments | * LTS[SimpleLink Wi-Fi® CC3220SF 无线微控制器 LaunchPad 开发套件](https://devices.amazonaws.com/detail/a3G0L00000AANtaUAH/SimpleLink-Wi-Fi%C2%AE-CC3220SF-Wireless-Microcontroller-LaunchPad-Development-Kit)<br/> |
| X |
| Xilinx | * LTS[MicroZed IIoT Bundle，配备 FreeRTOS](https://devices.amazonaws.com/detail/a3G0L00000AANtqUAH/MicroZed-IIoT-Bundle-with-Amazon-FreeRTOS)<br/> |
