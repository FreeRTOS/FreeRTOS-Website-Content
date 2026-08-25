---
title: 延长维护计划
description: 关于 FreeRTOS 延长维护计划的介绍
---

## 引言

FreeRTOS 延长维护计划 (EMP) 能够让您从初始 LTS 周期到期后长达 10 年里 
在您所选 FreeRTOS Long Term Support (LTS) 版本上接收安全补丁和关键故障修复[^1] 
。FreeRTOS EMP 由 Amazon Web Services (AWS) 提供，可帮助客户 
在数年内保护其基于微控制器的设备，节省操作系统升级成本， 
同时降低与设备现场修补相关的风险。

[^1]: AWS 可以在您的订阅期限届满之前， 
根据适用于您 AWS 服务使用的协议终止任何版本 LTS 的延长维护计划，但需要 
提前至少 12 个小时通知。


## 优势

### 降低产品生命周期风险

使用的固件可以在产品的整个生命周期中从功能稳定的代码库上接收安全补丁 
。功能稳定的代码库可以让您收到同一 LTS 版本的安全补丁， 
无需升级到最新的 FreeRTOS 版本。

### 节省操作系统升级成本

在您的订阅期间，FreeRTOS 库会继续提供稳定的功能和 API， 
进而消除通常在系统版本升级时产生的额外开发、测试和质量保证成本 
。

### 提高设备的长期安全性

在您选择的 FreeRTOS LTS 库上接收安全补丁和关键故障修复，提高 
您的 IoT 设备整个生命周期的安全性。

### 降低延迟更新的风险

设备更新关键修复涉及项目规划、发布准备测试和 over-the-air 
(OTA) 更新调度。借助延长维护计划，您可以及时收到关于即将到来的补丁和故障修复的通知， 
使您能够提前组织和计划您的更新。 


## 操作方式

FreeRTOS EMP 将 FreeRTOS LTS 库最初两年的维护期额外延长了 10 年 
。一旦您选择了 LTS 版本， 
您将通过 
[FreeRTOS EMP 的 AWS IoT 控制台](https://us-east-1.console.aws.amazon.com/iot/home?region=us-east-1#/freertos-emp/home)获得任何补丁（如果需要）。 
与 FreeRTOS LTS 库一样，FreeRTOS EMP 库将继续在您的订阅期间，提供稳定的功能和 API 
。 


![](/media/2021/Product-Page-Diagram_FreeRTOS-Extended-Maintenance-Plan-1.png)   

了解更多有关 FreeRTOS EMP 的信息，请参阅  
FreeRTOS [功能](https://aws.amazon.com/freertos/features/#FreeRTOS_Extended_Maintenance_Plan)、[定价](https://aws.amazon.com/freertos/pricing/)  
和[常见问题](https://aws.amazon.com/freertos/faqs/)页面（位于 AWS）或者 [联系我们](mailto:aws-iot-devices-pm@amazon.com)。
