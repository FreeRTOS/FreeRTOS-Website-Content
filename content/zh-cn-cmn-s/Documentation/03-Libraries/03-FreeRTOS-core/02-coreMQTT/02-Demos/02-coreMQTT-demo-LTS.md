---
title: coreMQTT 演示（带 TLS 服务器身份验证）
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

coreMQTT是一个 MIT 授权的开源 MQTT 客户端 C 库，适用于基于微控制器和小型微处理器的 IoT 设备。
  
**注意：我们建议在构建任何物联网 (IoT) 应用程序时使用相互身份验证（IoT MQTT 客户端和服务器相互
验证）。此页面上的演示展示了未经客户端身份验证的加密通信，仅用于
教育目的。它
不适用于生产用途。** 


## 单线程 VS 多线程

coreMQTT 有两种使用模式，*单线程*和*多线程*（多任务）。在多线程应用程序中， 
仅在一个线程上使用 MQTT 库（如本页记录的演示那样） 
等同于单线程用例。单线程 
用例要求应用程序写入器对 MQTT 库进行重复的显式调用。与此不同的是， 
多线程用例可以从一个[ agent（或守护进程任务）任务中在后台执行 MQTT 协议](mqtt-agent-demo.md)。 
在 agent 任务中执行 MQTT 协议使应用程序写入器无需 
显式托管任何 MQTT 状态或调用 `MQTT_ProcessLoop()` API 函数。使用 agent 任务还可以 
让多个应用程序任务共享单个 MQTT 连接，无需互斥锁之类的同步基元 
。
  

## 演示简介

共有三个示例项目介绍 
[“TLS 简介”](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction)页面上描述的概念，此示例项目是其中之一。 
[第一个示例](basic-mqtt-example.md)演示了未加密的 MQTT 通信。第二个 
示例（即本页面上的示例）在第一个示例的基础上引入服务器身份验证（ IoT 
客户端对其所连接的 MQTT 服务器进行身份验证）。[第三个示例](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication) 
在第二个示例的基础上引入强力相互身份验证（MQTT 服务器也会对其所连接的  
客户端进行身份验证）。

此演示不使用相互身份验证，因此**仅**用于练习。  

此 MQTT 演示使用基于 mbedTLS 的[网络传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)实现， 
先与 MQTT 代理建立经过服务器身份验证过的 TLS 连接，然后演示 
MQTT 在 [QoS 2](mqtt_terminology.md) 等级的订阅-发布工作流程。此演示通过订阅单个主题过滤器， 
然后再发布到同一主题上，让代理回显消息。每次发布后， 
它都会等待接收 [QoS 2](mqtt_terminology.md) 等级上的服务器返回的消息。 
这种向代理发布消息，然后又从代理那里接收同一消息的循环 
会无限重复。此演示中的消息在 QoS 2 上发送，确保消息*仅*传送一次。

此基础 MQTT 演示项目使用 
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)， 
因此可以在 Windows 上使用 
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估， 
无需任何特定 MCU 硬件。 


## 源代码组织

演示项目名为 mqtt_basic_tls_demo.sln， 
可在 FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Basic_TLS 
目录中找到，位于[主 FreeRTOS 下载中](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)，（也可在下载页面链接的 Github 中找到）。


## 配置演示项目

此演示使用 [FreeRTOS-Plus-TCP TCP/IP 堆栈](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/index.md)。 
请按照 
[TCP/IP 入门项目的说明操作，](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md) 
以确保您：

1. [安装了必备组件](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#prerequisites)（例如 WinPCap）。

2. [设置了静态或动态 IP 地址、网关地址和网络掩码](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#static-dynamic)（可选）。

3. [设置了 MAC 地址](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#mac-addr)（可选）。

4. 在您的主机上[选择以太网接口](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#network-interface) 
   。

5. ......以及**最重要的是**，在尝试运行 MQTT 演示之前，[请先测试网络连接](../FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator.md#connectivity-test) 
   。

所有这些设置都应在 MQTT 演示项目中执行，而非在同一页面中引用的 TCP/IP 入门项目中执行 
！传递时，TCP/IP 堆栈被配置为使用动态 IP 地址。


## 配置 MQTT 代理连接

### 备选方案 1：使用公开托管的 Mosquitto MQTT 代理（ web 托管）：

想要与 Mosquitto 公开托管的 MQTT 代理进行通信，请按照下列步骤进行操作：

1. 打开 `FreeRTOS/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Basic_TLS/demo_config.h` 的本地副本
2. 设置下列两个常量：
	* `#define democonfigMQTT_BROKER_ENDPOINT "test.mosquitto.org"`
	* `#define democonfigMQTT_BROKER_PORT (8883)`
3. 将常量 `#democonfigROOT_CA_PEM`（服务器的 CA 根证书）设置为 
   与 [https://test.mosquitto.org](https://test.mosquitto.org/) 主页链接的 PEM 证书 。该证书 
   要以字符串的形式进行粘贴，因此它将如下所示：

   ```c
   #define democonfigROOT_CA_PEM  &bsol;
      "-----BEGIN CERTIFICATE-----&bsol;n"&bsol;
      "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&bsol;n"&bsol;
      "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb&bsol;n"&bsol;
      "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc&bsol;n"&bsol;
      "... etc. .......................................................&bsol;n"&bsol;
      "-----END CERTIFICATE-----"
   ```


如果演示连接到具有 DHCP 服务和互联网接入的网络，则此设置应有效。 
请注意，FreeRTOS Windows 移植仅适用于有线以太网适配器 
（可以是虚拟以太网适配器）。 

应使用单独的 MQTT 客户端（如 [MQTT.fx](https://mqttfx.jensd.de/)）测试 
从您的主机到公共 MQTT 代理的 MQTT 连接。 

**注意**：Mosquitto 是一个开源 MQTT 消息代理，支持 MQTT 5.0、3.1.1 和 3.1 版本。 
它是 Eclipse 基金会的一部分，是一个 Eclipse IoT 项目。`test.mosquitto.org` MQTT 代理 
不隶属于 FreeRTOS 也不由其维护，并且可能随时不可用。此外， 
该代理所使用的服务器身份验证是基于 1024 位 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)）， 
所以不推荐用于生产目的。**请勿**从您的设备 
向此 MQTT 代理发送任何机密信息。  

  
### 备选方案 2：使用本地托管的 Mosquitto MQTT 消息代理（主机）

Mosquitto 代理也可以在本地运行，无论是在您的主机上（用于构建演示应用程序的机器），还是在 
您本地网络的另一台计算机上。请按以下步骤操作：

1. 请按照 https://mosquitto.org/download/上的说明在本地下载和安装 Mosquitto。
2. 打开 Mosquitto 安装目录中的 “mosquitto.conf”，并设置下列配置：
   * **per_listener_settings:** true
   * **port:** 8883
   * **allow_anonymous:** false
   * **cafile:** ./mosquitto/config/ca.crt
   * **certfile:** ./mosquitto/config/server.crt
   * **keyfile:** ./mosquitto/config/server.key
   * **tls_version:** tlsv1.2

注：上述配置中的 “cafile”、“certfile”、“keyfile” 分别指本地生成的 
 CA 证书、服务器证书和服务器密钥。它们都可以使用 OpenSSL 生成。 
如需了解更多信息，请登录 [mosquitto.org](https://mosquitto.org/man/mosquitto-tls-7.html)。

- 打开 `FreeRTOS/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Basic_TLS/demo_config.h` 的本地副本
- 添加下列行以设置 democonfigMQTT_BROKER_ENDPOINT 和 democonfigMQTT_BROKER_PORT：
  * `#define democonfigMQTT_BROKER_ENDPOINT "w.x.y.z"`
  * `#define democonfigMQTT_BROKER_PORT ( 8883 )`

**注意：**端口号 8883 是加密 MQTT 的默认端口号。如果您无法使用那个 
端口（例如，如果它被您的 IT 安全策略阻止），请把 Mosquitto 使用的端口更改为更高的端口号 
（例如，50000 到 55000 范围内的端口号），并相应地设置 `mqttexampleMQTT_BROKER_PORT` 
。Mosquitto 使用的端口号是由位于 Mosquitto 安装目录下的 "mosquitto.conf" 中的 "port" 参数 
设置的。 


### 备选方案 3：您选择的 MQTT 代理：

任何支持加密 TCP/IP 通信的 MQTT 代理都可与此演示一起使用。请按以下步骤操作：

1. 打开 `/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Basic_TLS/demo_config.h` 的本地副本
2. 添加下列行，并设置您所选择的代理：
   * #define democonfigMQTT_BROKER_ENDPOINT "your-desired-endpoint"
   * #define democonfigMQTT_BROKER_PORT ( 8883 )
3. 在 `demo_config.h` 中设置服务器的 CA 根证书 (`#democonfigROOT_CA_PEM`) （可选）


### 构建演示项目

演示项目的构建方式与 [基础 MQTT 演示（无 TLS）相同。](basic-mqtt-example.md#source_code)

* 在 Visual Studio IDE 中，打开 `FreeRTOS/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Basic_TLS/mqtt_basic_tls_demo.sln` 
  Visual Studio 解决方案文件。
* 在 IDE 的 “Build” 菜单中选择 “Build Solution”。

**注意：**如果您使用的是 Microsoft Visual Studio 2017 或更早版本，则必须选择与您的版本兼容的 “Platform 
Toolset”："Project -> RTOSDemos Properties -> Platform Toolset"。 


## 功能

此演示提供的功能和结构体与 
[基础 MQTT 演示](basic-mqtt-example.md#functionality)（无 TLS）相同， 
但使用包含 TLS 的[传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)来代替明文传输 
接口。


### 连接至 MQTT 代理（使用 TLS）

函数 `prvConnectToServerWithBackoffRetries()` 试图将 TLS 连接到 MQTT 
代理。如果连接失败，则在超时后重试。超时值将呈指数增长， 
并包括抖动，直到达到最大的尝试次数或达到最大的超时值 
。函数 `RetryUtils_BackoffAndSleep()` 提供呈指数增长的超时值， 
并在达到最大尝试次数时返回 `RetryUtilsRetriesExhausted`。重试之间的时间差 
用于确保碰巧同时断开连接的 IoT 设备群 
不会在完全相同的时间内尝试重新连接。 

```c
static TlsTransportStatus_t prvConnectToServerWithBackoffRetries(  
                                NetworkCredentials_t * pxNetworkCredentials,  
                                NetworkContext_t * pxNetworkContext )  
{  
    TlsTransportStatus_t xNetworkStatus;  
    RetryUtilsStatus_t xRetryUtilsStatus = RetryUtilsSuccess;  
    RetryUtilsParams_t xReconnectParams;  
  
    /* Set the credentials for establishing a TLS connection. */  
    pxNetworkCredentials->pRootCa = ( const unsigned char * ) democonfigROOT_CA_PEM;  
    pxNetworkCredentials->rootCaSize = sizeof( democonfigROOT_CA_PEM );  
    pxNetworkCredentials->disableSni = democonfigDISABLE_SNI;  
  
    /* Initialize reconnect attempts and interval. */  
    RetryUtils_ParamsReset( &xReconnectParams );  
    xReconnectParams.maxRetryAttempts = MAX_RETRY_ATTEMPTS;  
  
    /* Attempt to connect to the MQTT broker. If connection fails, retry after  
     * a timeout. Timeout value will exponentially increase until maximum  
     * attempts are reached. */   
    do  
    {  
        /* Establish a TLS session with the MQTT broker. This example connects  
         * to the MQTT broker as specified in democonfigMQTT_BROKER_ENDPOINT  
         * and democonfigMQTT_BROKER_PORT at the top of this file. */  
        xNetworkStatus = TLS_FreeRTOS_Connect( pxNetworkContext,  
                                democonfigMQTT_BROKER_ENDPOINT,  
                                democonfigMQTT_BROKER_PORT,  
                                pxNetworkCredentials,  
                                mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS,  
                                mqttexampleTRANSPORT_SEND_RECV_TIMEOUT_MS );  
  
        if( xNetworkStatus != TLS_TRANSPORT_SUCCESS )  
        {  
            /* Connection failed. */  
            xRetryUtilsStatus = RetryUtils_BackoffAndSleep( &xReconnectParams );  
        }  
  
        if( xRetryUtilsStatus == RetryUtilsRetriesExhausted )  
        {  
            /* Maximum number of connection attempts reached. */  
            xNetworkStatus = TLS_TRANSPORT_CONNECT_FAILURE;  
        }  
    } while( ( xNetworkStatus != TLS_TRANSPORT_SUCCESS ) &&  
             ( xRetryUtilsStatus == RetryUtilsSuccess ) );  
  
    return xNetworkStatus;  
}  

```

