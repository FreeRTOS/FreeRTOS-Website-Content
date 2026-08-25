---
title: 蜂窝接口演示（零接触配置）
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 简介

1NCE 是一家全球 IoT 运营商，专门为低 
带宽 IoT 应用程序提供托管连接服务。在本演示中， 1NCE 的服务（1NCE SIM 卡 + AWS IoT 设备启动服务器） 
与一个 BG96 蜂窝模块将用于演示如何通过 
零接触方式配置设备并连接 AWS IoT 内核。请参阅 
FreeRTOS[(https://github.com/1NCE-GmbH/blueprint-freertos) 的 ]1nce 蓝图。


## 下载源代码

源代码可以从 FreeRTOS 实验室下载，也可以通过 Github 自行下载。

使用 HTTPS 进行克隆：

```c
git clone https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo.git --recurse-submodules
```

使用 SSH：

```c
git clone git@github.com:FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo.git --recurse-submodules
```

如果下载存储库时未使用 `--recurse-submodules` 实参，则必须运行：

```c
git submodule update --init --recursive
```


## 源代码组织

演示项目名为 `1nce_bg96_zero_touch_provisioning_demo.sln`， 
可在 [Github](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/tree/main/projects) 上的 
以下目录中找到。

* [projects/1nce_bg96_zero_touch_provisioning_demo](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/tree/master/projects/1nce_bg96_zero_touch_provisioning_demo)


```c
./Lab-Project-FreeRTOS-Cellular-Demo
├── lib
│   ├── backoff_algorithm ( submodule : backoffAlgorithm )
│   ├── cellular ( submodule : FreeRTOS-Cellular-Interface )
│   ├── coreMQTT ( submodule : coreMQTT )
│   ├── FreeRTOS ( submodule : FreeRTOS-Kernel )
│   └── ThirdParty
│       └── mbedtls ( submodule : mbedtls )
├── projects
│   ├──  sim70x0_mqtt_mutual_auth_demo ( demo project for SIMCOM sim7080/sim7090 )
│   └──  1nce_bg96_zero_touch_provisioning_demo ( demo project for 1nce zero touch provisioning with BG96 )
└── source
    ├── cellular
    │   └── ( code for adapting FreeRTOS Cellular Library with this demo )
    ├── coreMQTT
    │   └── ( code for adapting coreMQTT with this demo )
    ├── FreeRTOS
    │   └── ( code for adapting FreeRTOS with this demo )
    ├── mbedtls
    │   └── ( code for adapting mbedtls with this demo )
    ├── main.c
    ├── cellular_setup.c
    ├── MutualAuthMQTTExample.c
    ├── demo_config.h
    ├── logging_levels.h
    ├── logging_stack.h
    ├── 1nce_zero_touch_provisioning.h
    └── 1nce_zero_touch_provisioning.c

```


## 配置应用程序设置

### 配置蜂窝网络

蜂窝配置中的以下参数 
[cellular_config.h](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/cellular_config.h)， 
必须根据您的网络环境进行修改。

| 配置 | 描述 | 值 |
| --- | --- | --- |
| CELLULAR_COMM_INTERFACE_PORT | 蜂窝通信接口利用计算机上的 COM 端口，与 Windows 模拟器上的蜂窝模块进行通信。 | 连接到蜂窝模块的 COM 端口 |
| CELLULAR_APN | 网络注册的默认 APN。 | 根据您的网络运营商指定此值。 |
| CELLULAR_PDN_CONTEXT_ID | 蜂窝网络的 PDN 上下文 ID。 | 默认值为 CELLULAR_PDN_CONTENT_ID_MIN。 |
| CELLULAR_PDN_CONNECT_TIMEOUT | 网络注册的 PDN 连接超时。 | 默认值为 100000 毫秒。 |


### 配置 MQTT 代理

连接至 MQTT 代理的配置可以在 
["source/demo_config.h"](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/demo_config.h) 中找到。 
请参阅[文档](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection) 
了解有关设置的详细信息。


### 配置 COM 端口设置

有关 COM 端口设置，请参阅蜂窝模块文档。更新 
[comm_if_windows.c](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/source/cellular/comm_if_windows.c) 
（如有必要）。


### 配置其他子模块

["source/FreeRTOS/FreeRTOSConfig.h"](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/FreeRTOSConfig.h)、 
 ["source/mbedtls/mbedtls_config.h"](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/mbedtls_config.h) 
和 ["source/coreMQTT/core_mqtt_config.h"](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/core_mqtt_config.h) 
是相应子模块的配置。


## 构建并运行 1NCE 零接触配置演示

1. 在 Visual Studio 中，打开 
   [1nce_bg96_zero_touch_provisioning_demo.sln](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/tree/main/projects/1nce_bg96_zero_touch_provisioning_demo) 
   项目。在此 Visual Studio 解决方案文件中，定义了宏 `USE_1NCE_ZERO_TOUCH_PROVISIONING`。 
   请查看源文件中的 `#ifdef USE_1NCE_ZERO_TOUCH_PROVISIONING`， 
   了解使用 1nce 服务的设备在配置方式上的差异。否则，该演示将执行 
   与其他演示相同的相互验证 MQTT 操作。

2. [在本地生成自签名证书及其私钥](https://docs.aws.amazon.com/iot/latest/developerguide/create-device-cert.html)。 
   用证书和私钥更新 [“source/demo_config.h”](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/demo_config.h) 
   。其被用于建立 TSL 与 1NCE 服务器间的连接。 
   需注意私钥均放置于头文件中，仅可用于演示用途；生产设备应使用安全的 
   存储器来存放密钥。

3. 从 1NCE 获取 SIM 卡的接入点名称 (APN)。为 BG96 更新 `CELLULAR_APN` 
   （在文件 ["cellular_config.h"](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/cellular_config.h) 中） 
   然后按照上文“配置应用程序设置”中的步骤完成其余 
   配置。

4. 编译并运行。
