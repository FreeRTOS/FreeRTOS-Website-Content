---
title: Fleet Provisioning 术语
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

*Fleet Provisioning*   
创建资源的工作流，使您的设备可以和 AWS IoT 安全地通信。Fleet Provisioning 
可以创建 AWS IoT Things。有关详细信息，请参阅 
Device Provisioning 上的 [AWS IoT 文档](https://docs.aws.amazon.com/iot/latest/developerguide/iot-provision.html) 
。


*设备证书*   
设备证书是与特定设备关联的凭据。许多设备制造时 
已经配备设备证书。如果设备已经拥有证书，则可以向 
AWS IoT 注册。否则，可以从 AWS IoT 获得设备证书。有关设备证书的更多信息， 
请参阅 
Device Provisioning 上的 [AWS IoT 文档](https://docs.aws.amazon.com/iot/latest/developerguide/iot-provision.html) 
。


*预调配模板*   
预调配模板描述了 AWS IoT 预调配设备所需的资源。模板包含 
使您能够使用一个模板来设置多个设备的变量。预调配设备时， 
可使用字典或映射为特定于设备的变量指定值。若要预调配另一个设备， 
请在字典中指定新值。 


*通过申请预调配*   
使用申请证书和私钥向 AWS IoT 设置设备的方法。在制造设备时， 
可以在设备中嵌入专用凭据（预调配申请证书和私钥）。 
如果将这些证书注册到 AWS IoT，服务可以交换证书，作为设备可用于常规操作的唯一设备证书 
。有关通过申请预调配的更多信息，请参阅 
[AWS IoT 文档](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html)。


*使用可信用户的预调配*   
使用可信用户的访问权限向 AWS IoT 设置设备的方法。有关 
有关使用可信用户的预调配的更多信息，请参阅 
[AWS IoT 文档](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html)。
