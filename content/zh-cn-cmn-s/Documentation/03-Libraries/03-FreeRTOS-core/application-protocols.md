---
title: 应用程序协议
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
description: FreeRTOS 应用程序协议库简介
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
- title: FreeRTOS 初学者指南
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
- title: 下载 FreeRTOS
  link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
- title: 常见问题
  link: /Why-FreeRTOS/FAQs
---

应用程序协议库为构建基于微控制器的 IoT 设备提供连接能力。“核心”
品牌的应用程序协议均为“独立”协议，除了 C 库之外不具有任何依赖项。
这些协议使用简单的传输接口定义，以确保它们不依赖于底层 TCP/IP 堆栈。

### coreMQTT

用于 IoT 用例的轻量级发布/订阅协议。
源代码现已可以在 [coreMQTT](https://github.com/FreeRTOS/coreMQTT/releases/latest) 存储库中获取。  
[了解更多](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)

### coreMQTT Agent

使用 coreMQTT 的线程安全 MQTT 库，用于 IoT 用例。
源代码现已可以在 [coreMQTT-Agent](https://github.com/FreeRTOS/coreMQTT-Agent/releases/latest) 存储库中获取。  
[了解更多](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent)

### coreHTTP

用于 IoT 用例的轻量级请求和响应消息传递协议。
源代码现已可以在 [coreHTTP](https://github.com/FreeRTOS/coreHTTP/releases/latest) 存储库中获取。  
[了解更多](http/index)

### coreSNTP

coreSNTP 库提供了一个简单网络时间协议 (SNTP) 的客户端，
允许设备将其系统时钟与时间服务器同步。此库实现了
[RFC 4330](https://tools.ietf.org/html/rfc4330) 中定义的 SNTPv4 规范。
源代码现已可以在 [coreSNTP](https://github.com/FreeRTOS/coreSNTP/releases/latest) 存储库中获取。  
[了解更多](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP)

### 传输接口

用于发送和接收数据的接口，此接口不依赖于底层 TCP/IP 堆栈。  
[了解更多](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)

### coreJSON

一种严格执行 ECMA-404 JSON 标准的解析器。
源代码现已可以在 [coreJSON](https://github.com/FreeRTOS/coreJSON/releases/latest) 存储库中获取。  
[了解更多](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)

### corePKCS #11

加密 API 层（OASIS 标准），用于抽象密钥存储、获取/设置加密
对象的属性和会话语义。
源代码目前可在 [corePKCS11](https://github.com/FreeRTOS/corePKCS11/releases/latest) github 存储库中获取。  
[了解更多](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)
