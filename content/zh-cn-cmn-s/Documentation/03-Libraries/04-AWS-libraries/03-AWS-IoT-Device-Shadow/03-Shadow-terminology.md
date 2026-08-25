---
title: Shadow 术语
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

*Device Shadow 服务文档*   
Device Shadow 服务文档是由 Amazon 
Web Services (AWS) 云中的 Shadow 服务维护的 JSON 文档。用于存储和检索设备的当前状态信息。

示例文档：

```c
{  
    "state" : {
        "desired" : {
            "color" : "RED"
        },
        "reported" : {
            "color" : "GREEN"
        }
    },
    "metadata" : {
        "desired" : {
            "color" : {
                "timestamp" : 12345
            }
        },
        "reported" : {
            "color" : {
                "timestamp" : 12345
            }
        }
    },
    "version" : 10,
    "clientToken" : "UniqueClientToken",
    "timestamp": 123456789
}
```

*Device Shadow 服务文档属性*   
设备的 Shadow 服务文档包含以下属性： 

+ `state`

+ `desired`

  设备（事物）的所需状态。应用程序可以写入文档的这一部分 
  来更新事物的状态，而无需直接连接到事物。如上图所示的一个状态示例 
  是“颜色”：“红色"。 

+ `reported`

  事物的报告状态是当前状态。事物写入文档的此部分 
  以报告新状态。 

+ `metadata`

  有关 `state` 部分中存储的数据的信息， 
  例如 `state` 部分中每个属性的时间戳（以纪元时间为单位）。这使您能够确定这些部分何时更新。

+ `timestamp`

  表示消息由 AWS IoT 传输的时间。通过使用消息中的时间戳和 
  `desired` 或 `reported` 部分中各个属性的时间戳， 
  即使没有实现内部时钟，事物也能确定更新项目的时间。

+ `clientToken`

  该字符串是设备唯一的字符串， 
  使您能够将响应与 MQTT 环境中的请求相关联。

+ `version`

  文档版本每次更新都会递增。它用于确保 
  正在更新的文档版本为最新。


*Shadow Update*   
Shadow Update 操作可创建设备的影子（如果不存在）， 
或更新设备的 Shadow 服务文档的内容。任何内容更改都存储有一个时间戳， 
以显示上次更新的时间。消息将发送给所有订阅者，其中包括 `desired` 与 
`reported` 状态之间的差异（Delta）。接收到这些信息的事物或应用程序 
可以根据 `desired` 和 `reported` 状态之间的差异执行操作。例如，设备可以将其状态更新到所需状态， 
或者应用程序可以更新其 UI 以显示设备状态的变化。


*Shadow Get*   
Shadow Get 操作可检索存储在设备影子中的最新状态。例如，在启动时， 
设备连接到 AWS IoT Core，以检索配置数据和最后一个操作状态。此 
方法返回完整的 JSON 文档，包括元数据。


*Shadow Delete*   
Shadow Delete 操作将删除设备的影子，包括其所有内容。这 
将从数据库中删除 JSON 文档。Device Shadow 一旦删除，就无法恢复， 
但可以创建新的 Device Shadow（名称相同）。


*Shadow Delta 回调*   
Shadow Delta 回调返回 Shadow Delta 状态，这是一个虚拟状态， 
包含 `desired` 和 `reported` 状态之间的差异。`desired` 部分中 
与 `reported` 部分不匹配的字段将包含在 Delta 中。位于 `reported` 部分但不位于 
`desired` 部分中的字段不包含在 Delta 中。当更新设备影子时， 
如果影子文档中的 `desired` 和 `reported` 状态不同， 
则会向 $aws/things/*`thing-name`*/shadow/update/delta 主题发布一条消息。

此消息仅包含设备 Shadow 文档中 `desired` 和 `reported` 部分之间的差异 
。收到此消息后，设备应决定是否进行请求的更改 
。在 Shadow 库中，可以通过注册 Shadow Delta Callback 回调来检索增量状态。


*Shadow Updated Callback*   
每当成功更新影子时，Shadow Updated 回调就会从  AWS IoT 
向此主题返回一个状态文档：


$aws/things/*`thingName`*/shadow/update/documents

JSON 文档将包含两个主节点：`previous` 和 `current`。`previous` 节点将 
包含更新前的完整影子文档内容，而 `current` 节点将 
包含成功应用更新后的完整影子文档内容。首次更新（创建）影子时， 
`previous` 节点将包含 `null`。在 Shadow 库中， 
可以通过注册 Shadow Updated 回调来检索更新后的状态文档。
