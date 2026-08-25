---
title: TLS 简介
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

物联网 (IoT) 用例需要对 [MQTT](https://en.wikipedia.org/wiki/MQTT)
和 [HTTP](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) 等应用协议进行加密和身份验证。因此，
这些协议通常与传输层安全协议
 ([TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security)) 结合使用。有关“运行在 TLS 协议上的 MQTT 协议”，
请参阅 [MQTT 3.1 规范](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718098)一节，
有关“运行在 TLS 协议上的 HTTP 协议”，请参阅 [HTTPS 规范](https://tools.ietf.org/html/rfc2818#section-2)一节。

传输层安全协议 ([TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security))
是一种加密协议，旨在通过互联网实现客户端与服务器之间的安全通信。它
用于确保数据在客户端和服务器之间的安全传递，
但不考虑端点（客户端或服务器端）的安全性。客户端向服务器发出信号，表示它们希望建立 TLS 连接，
然后客户端和服务器使用[握手协议](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/03-TLS-terminology)
协商如何在彼此之间建立信任。握手协议完成后，
便可以使用握手期间协商的加密方法在双方之间发送数据。

通常只需要客户端认证服务器身份
（例如当 web 浏览器连接 HTTPS web 服务器时）。IoT 设备通常使用“双向认证”，
即还需要服务器验证 IoT 设备客户端的身份。


## 实现

所实现的 [TLS 协议](https://tools.ietf.org/html/rfc5246)为 TLS v1.2
