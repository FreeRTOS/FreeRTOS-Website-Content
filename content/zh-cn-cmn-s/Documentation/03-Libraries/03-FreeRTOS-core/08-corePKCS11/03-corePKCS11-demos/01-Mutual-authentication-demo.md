---
title: corePKCS11 双向验证演示 (MQTT)
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


**注意：建议您在所有物联网 (IoT) 应用程序中始终使用严格双向验证。
本示例使用推荐的双向验证，适用于生产环境中的 IoT。**

* 本页内容：
    + [源代码组织](#源代码组织)
    + [配置演示项目](#配置演示项目)
    + [构建演示项目](#构建演示项目)
    + [功能](#功能)


## 简介

本演示基于 MQTT 双向验证演示，并假定您已经熟悉 
MQTT 演示系列。如果不熟悉，请参阅 [MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 部分。

PKCS #11 演示项目使用 
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)， 
因此可以在 Windows 上使用 
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估， 
无需任何特定 MCU 硬件。

演示中与 AWS (Amazon Web Services) IoT 建立连接的方式与 MQTT 双向验证类似， 
但该方式使用 PKCS #11 来管理 
与 AWS IoT 建立连接所需的凭据。出于演示目的，此 PKCS #11 实现使用 Windows 文件系统 
进行凭据管理。

PKCS #11 的工作原理是为每个加密对象分配一个人类可读标签。在本演示中，我们 
将 "Device Priv TLS Key" 标签映射到私钥，将 "Device Cert" 标签映射到证书。这些标签 
可在 `core_pkcs11_config.h` 中进行管理。在 `core_pkcs11_pal.c` 中，我们已将这些标签分别映射到 `FreeRTOS_P11_Key.dat` 
和 `FreeRTOS_P11_Certificate.dat`。 


### 源代码组织

基于 PKCS #11 的双向验证的 Visual Studio 解决方案演示名为 `pkcs11\_mqtt\_mutual\_auth\_demo.sln.sln`， 
位于 `\FreeRTOS-Plus\Demo\corePKCS11\_MQTT\_Mutual\_Auth\_Windows\_Simulator\pkcs11\_mqtt\_mutual\_auth\_demo.sln` 
目录（详见 FreeRTOS 主下载内容）。

[\![](../fr-content-src/uploads/2020/10/PKCS11-Source-Code-Organization.png)](../fr-content-src/uploads/2020/10/PKCS11-Source-Code-Organization.png)   
*点击放大*


## 配置演示项目

请按照 
[MQTT 双向验证](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication) 中的说明配置演示项目，您可以忽略 
涉及将证书和私钥迁移到 `democonfig.h` 文件的步骤，但请确保 
 `democonfig.h` 中包含 Thing 名称和 AWS IoT 端点。之所以可以忽略这些步骤， 
是因为您将通过 PKCS #11 接口（而非本演示项目）导入凭据。 

完成后，请按照以下步骤操作：

1. 在 `democonfig.h` 中

   1. 将 `democonfigCLIENT_CERTIFICATE_PEM` 设置为空字符串。

      `#define democonfigprofileCLIENT_CERTIFICATE_PEM ""`

   2. 将 `democonfigprofileCLIENT_PRIVATE_KEY_PEM` 设置为空字符串。

      `#define democonfigprofileCLIENT_PRIVATE_KEY_PEM ""`

   3. 这是为了防止 `\FreeRTOS-Plus\Demo\corePKCS11_MQTT_Mutual_Auth_Windows_Simulator\demo_config.h;` 
      生成编译器错误，并进一步证明演示中从未使用 
      此头文件中的凭据。

2. 将使用 AWS IoT Core 进行验证的密钥和证书 PEM 文件转换为 DER 格式。

   1. 想必您已在 MQTT 演示中获取了 PEM 格式的凭据。如果没有，请重新查看 
      MQTT 双向验证演示系列，以获取有关检索这些凭据的指导。

   2. 方案 1：使用提供的 python 脚本：

      1. 导航到 `\FreeRTOS-Plus\Demo\corePKCS11_MQTT_Mutual_Auth_Windows_Simulator`，然后 
         将密钥和证书 PEM 文件的绝对路径传递至 `pkcs11_demo_setup.py`。

         `python3 pkcs11_demo_setup.py -c thing_cert_pem_file.pem -k thing_private_key_pem_file.pem`

      2. 这将在脚本运行的同一位置输出等效的 .dat 文件。

   3. 方案 2：手动转换 PEM 文件。

      1. 如果您选择不使用上述脚本，请手动将 PEM 文件转换为 PKCS #11 兼容的 DER 格式。

      2. 使用 [OpenSSL](https://www.openssl.org/) 进行转换的示例：

         `openssl x509 -outform der -in "CERTIFICATE_PEM_FILE" -out FreeRTOS_P11_Certificate.dat`

         `openssl pkcs8 -topk8 -inform PEM -outfrom -DER -in "KEY_PEM_FILE" -out FreeRTOS_P11_Key.dat`

3. 将新创建的 .dat 文件移动到与项目解决方案相同的文件夹，本例中 
   为 `FreeRTOS-Plus\Demo\corePKCS11_MQTT_Mutual_Auth_Windows_Simulator\pkcs11_mqtt_mutual_auth_demo.sln;`。


## 构建演示项目

演示项目 
使用  [社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)[。](../mqtt/basic-mqtt-example.md#source_code)

1. 在 Visual Studio IDE 中，打开 `\FreeRTOS-Plus\Demo\corePKCS11_MQTT_Mutual_Auth_Windows_Simulator\pkcs11_mqtt_tls_mutual_auth\pkcs11_mqtt_tls_mutual_auth_demo.sln` 
   Visual Studio 解决方案文件。

2. 在 IDE 的 'build'（构建）菜单中选择 'build solution' （构建解决方案）。


## 功能

本演示与双向验证 MQTT 演示提供的功能相同，增加了 
使用 PKCS #11 管理凭据相关内容。有关 MQTT 功能的详细信息，请查看 
[MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication) 演示系列。 

本演示与 MQTT 演示系列之间的主要区别在于 
`FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/src/tls_freertos_pkcs11.c` 
修改为使用 PKCS #11。 
请参阅 `FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/src/tls_freertos_pkcs11.c` 
和 `FreeRTOS-Plus/Source/Application-Protocols/platform/freertos/transport/include/tls_freertos_pkcs11.h`， 
了解如何使用 PKCS#11 建立 TLS 连接。

应用程序层也存在代码更改，强调使用 PKCS #11 进行凭据 
管理。例如，在 `FreeRTOS-Plus/Demo/corePKCS11_MQTT_Mutual_Auth_Windows_Simulator/DemoTasks/MutualAuthMQTTExample.c` 中， 
`xNetworkSecurityCredentials` 结构体中不包含客户端证书和密钥， 
这与 `FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/DemoTasks/MutualAuthMQTTExample.c` 不同。 

您还可以采取额外步骤，在演示过程中尝试将 .dat 文件移动到其他目录中。这会导致 
无法与 AWS IoT Core 建立新连接，因此后续无法对演示进行 
迭代。有关成功演示的输出示例，请参阅 MQTT 演示系列。

