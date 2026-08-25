---
title: 将 Device Defender 库与 MQTT Agent 集成
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

* 本页内容：
  + [简介](#引言)
  + [说明](#说明)
    - [入门指南](#入门指南)
    - 通过 AWS IoT 控制台创建自定义指标
    - [配置安全配置文件](#配置安全配置文件)
    - [配置和运行演示](#配置和运行演示)
    - 查看 AWS IoT 控制台上的指标


## 引言

此示例使用 [MQTT agent](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo) 与 
[AWS IoT Device Defender 服务](https://docs.aws.amazon.com/iot/latest/developerguide/device-defender.html)交互。 
交互的方式是提交 device defender 报告， 
其中包括[自定义指标](https://docs.aws.amazon.com/iot/latest/developerguide/dd-detect-custom-metrics.html)， 
并验证报告是否被接受。MQTT Agent 启用 Defender 报告功能， 
使其在后台运行，并与其他任务共享 MQTT 连接。

Device Defender 演示代码作为任务运行在 
与下列各项[相同的演示项目](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/tree/main/build/VisualStudio)中： 
[MQTT agent 演示](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)  和 [OTA 演示](/Documentation/03-Libraries/07-Modular-over-the-air-updates/02-Demos/02-mqtt-ota-agent-orchestrator)。 
按照 [MQTT agent 演示文档页面](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo#obtaining-the-source-code)中的指示操作， 
以获取和配置项目。要使用 Device Defender 演示任务，请配置您的项目 
以连接到 [AWS IoT Core](https://docs.aws.amazon.com/iot/index.html)，然后执行 
此页面上指定的其他项目和 AWS 帐户配置。

有关更多信息，请参阅 
[源目录](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/tree/main/source)中各 C 文件顶部的注释 
。 


## 说明

### 入门指南

首先按照 [MQTT agent 演示文档页面](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)所述设置项目。 
请务必执行以下所有步骤，首先是：

1. [了解 MQTT Agent 演示](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo#demo-project)
2. [获取源代码](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo#obtaining-the-source-code)
3. [配置 FreeRTOS-Plus-TCP](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)
4. [配置 MQTT 代理](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)
5. [配置 MQTT Agent](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)

按照说明[使用 AWS IoT Core MQTT 代理连接](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo#configuring-the-mqtt-broker-connection) 
并使用一个简单的 MQTT 任务来测试连接。这将保证与 AWS IoT Core 的连接正常运作， 
然后再继续激活 Device Defender 任务。

与非 Defender 演示的连接可正常使用后，以下说明将为您展示如何： 

* 在您的 AWS 帐户上设置自定义指标。
* 配置安全配置文件以保留提交的报告。
* 启用并运行演示任务。
* 查看提交的指标。


### 通过 AWS IoT 控制台创建自定义指标

此演示提交[自定义指标](https://docs.aws.amazon.com/iot/latest/developerguide/dd-detect-custom-metrics.html)时， 
第一步是在 AWS 账户上配置这些指标。演示使用了两个自定义指标， 
分别名为 "stack_high_water_mark"（类型编号）和 "task_numbers"（类型编号列表）。首先 
前往 [AWS IoT 控制台](https://console.aws.amazon.com/iot/home)。 

在 AWS IoT 控制台的导航窗格中，依次选择 **Defend**、**Detect** 和 **Metrics**。

[\![](/media/2021/Custom-Metrics-1.jpg)](/media/2021/Custom-Metrics-1.jpg)   
**点击放大。**

点击自定义指标部分中的 “Create”。在 “Name” 下，输入 “stack_high_water_mark”。 
在 “Type” 下，选择 “number”。然后，点击 “Create custom metric”。

[\![](/media/2021/Custom-Metrics-2.png)](/media/2021/Custom-Metrics-2.png)   
**点击放大。**

重复上一步，但名称选择 “task_numbers”，然后类型选择 “number-list”。此时应该能够 
看到下文所示的两个指标。

[\![](/media/2021/Custom-Metrics-3.png)](/media/2021/Custom-Metrics-3.png)   
**点击放大。**


### 配置安全配置文件

为保留已提交的报告，需要配置安全配置文件。首先， 
前往 [AWS IoT 控制台](https://console.aws.amazon.com/iot/home). 在 
AWS IoT 控制台的导航窗格中，依次选择 **Defend**、**Detect** 和 **Security Profiles**。

[\![](/media/2021/Custom-Metrics-4.png)](/media/2021/Custom-Metrics-4.png)   
**点击放大。**

在 “Create Security Profile” 下，选择 “Create Rule-based anomaly Detect profile”。在 “Name” 下 
输入名称。在点菜单下，点击 “Delete” 以删除默认行为。

[\![](/media/2021/Custom-Metrics-5.png)](/media/2021/Custom-Metrics-5.png)   
**点击放大。**

展开 “Additional Metrics to retain” 部分，然后单击第一个复选框以选择所有指标 
。点击下一步。然后在“预警目标”页面上，单击 "Next"。

[\![](/media/2021/Custom-Metrics-6.png)](/media/2021/Custom-Metrics-6.png)   
**点击放大。**

在“附加”页面上，选择 “All things”，然后单击 “Next”。点击“确认”页面上的 “Save” 按钮。

[\![](/media/2021/Custom-Metrics-8.png)](/media/2021/Custom-Metrics-8.png)   
**点击放大。**


### 配置和运行演示

要运行此演示，您需要设置与 AWS IoT Core 的连接。请按照 
[此处配置步骤](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection)操作， 
完成之后执行以下步骤：

**注意：**确保 
 [democonfigCLIENT_IDENTIFIER](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/configuration-files/demo_config.h#L100) 
已设置为 Thing 的名称。

* 将 [democonfigCREATE_DEFENDER_DEMO](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/configuration-files/demo_config.h#L84) 更新为 1 来启用 defender 演示任务。
* 运行演示并让其提交一些报告。默认情况下，演示每 30 秒发送一次报告。
* 报告发送成功时，以下消息将打印到控制台：

```c
**The defender report was accepted by the service.**  
```


### 查看 AWS IoT 控制台上的指标

演示提交报告后，您便可以查看报告以验证其是否正常运作。首先， 
前往 [AWS IoT 控制台](https://console.aws.amazon.com/iot/home)。 

在 AWS IoT 控制台的导航窗格中，选择 **Manage**，然后选择 **Things**。 

选择为演示创建的 Thing，然后选择 “Defender metrics” 选项卡。这里您可以选择已报告的指标， 
包括自定义指标，然后查看已报告的数值。报告可能需要等一会才能显示出来。

[\![](/media/2021/Custom-Metrics-9.png)](/media/2021/Custom-Metrics-9.png)   
**点击放大。**
