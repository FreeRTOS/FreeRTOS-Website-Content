---
title: OTA 术语
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

*AWS Jobs*
AWS IoT Jobs 是一项服务，用于通知一个或多个已连接设备有待处理的“作业”（Job）。作业可
用于管理设备群、更新设备上的固件和安全证书，或执行重启设备、运行诊断等管理任务。有关
更多信息，请参阅 [Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs)。


*AWS Management Console*
[AWS Management Console](https://aws.amazon.com/console/) 是一个用于访问各种 AWS 服务的网站。


*AWS IoT Console*
[AWS IoT Console](https://aws.amazon.com/iot/) 是一个用于与 IoT 相关 AWS 服务交互的网站，
其中包括用于管理、监控和更新设备的服务。


*OTA Update Manager Service*
Over-the-air (OTA) Update Manager 服务提供以下功能：

1. 创建 OTA 更新及其使用的资源，包括 AWS IoT 作业、AWS IoT 流和代码签名。
2. 获取有关 OTA 更新的信息。
3. 列出与您的 AWS 账户关联的所有 OTA 更新。
4. 删除 OTA 更新。

[了解更多](https://docs.aws.amazon.com/freertos/latest/userguide/ota-manager.html)


*AWS Command Line Interface (AWS CLI)*
在 Windows、macOS 和 Linux 上运行 AWS IoT 命令。这些命令可让您创建和管理事物、证书、规则
和策略。要开始使用，请参阅 [AWS Command Line Interface 用户指南](https://docs.aws.amazon.com/cli/latest/userguide/)。
有关 AWS IoT 命令的更多信息，请参阅 *AWS CLI 命令参考* 中的
[iot](https://docs.aws.amazon.com/cli/latest/reference/iot/index.html)。


*S3 Bucket*
Amazon Simple Storage Service (S3) 是一项 AWS 服务，使您能够在云中存储文件，并可由您或其他
服务访问。OTA 更新文件存储在 Amazon S3 存储桶中。
[了解更多](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/what-is-s3.html)


*Registry*
在 AWS 云中组织与每台设备关联的资源。您可以注册设备，并为每台设备关联最多三个自定义属性。
您还可以为每台设备关联证书和 MQTT 客户端 ID，以提升管理和排查设备问题的能力。有关更多信息，
请参阅 [使用 AWS IoT 管理设备](https://docs.aws.amazon.com/iot/latest/developerguide/iot-thing-management.html)。


*AWS IoT 中的“事物”（Things）*
事物是 AWS IoT 中设备或逻辑实体的表示形式。它可以是物理设备或传感器（例如灯泡或墙上的开关），
也可以是逻辑实体，例如某个应用程序的实例，或者本身不连接 AWS IoT 但与连接设备相关的物理实体
（例如装有发动机传感器或控制面板的汽车）。AWS IoT 提供事物注册表，帮助您管理事物。

事物通过名称进行标识。事物还可以拥有属性，即名称-值对，可用于存储有关事物的信息，例如序列号
或制造商。将事物添加到事物注册表后，您可以更轻松地管理和搜索它们。

**您知道吗？** 事物不一定需要连接到设备。您可以将事物连接到计算机、模拟器等。


*AWS IoT Policy*
[AWS IoT 策略](https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html)授予您的设备
访问 AWS IoT 资源的权限。它存储在 AWS 云中。


*IAM Role*
Identity Access Management [(IAM)](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
帮助您安全地控制对 AWS 资源的访问。您可以使用 IAM 控制谁通过身份验证（已登录）以及谁获得授权
（拥有权限）来使用资源。[IAM 角色](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
是您 AWS 账户中的一个实体，拥有特定权限，您可以将其分配给其他用户。


*MQTT*
[MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)（Message Queue Telemetry
Transport，消息队列遥测传输）库提供了一种轻量级的发布/订阅
（即 [PubSub](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)）消息协议，运行在
TCP/IP 之上，常用于机器对机器（M2M）和物联网（IoT）场景。
[了解更多](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)


*MQTT Broker Endpoint*
客户端连接到其 AWS 账户的设备端点。每个账户都有若干个设备端点，这些端点对该账户唯一，
并支持特定的 IoT 功能。
[了解更多](https://docs.aws.amazon.com/iot/latest/developerguide/iot-connect-devices.html#iot-connect-device-endpoints)


*Patch*
补丁（patch）是两个固件版本之间的一组更改。用户可以使用任意二进制差分机制生成补丁，
其中较为常用的有 bsdiff、xdelta、jojodiff 和 courgette。
