---
title: TLS 术语
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

- *基本 TLS 握手*

  [基本 TLS 握手](https://en.wikipedia.org/wiki/Transport_Layer_Security#Basic_TLS_handshake) 是 
  指客户端和服务器之间进行协商，以便对服务器进行身份验证 
  并协商通信细节。在握手过程中，由客户端和服务器决定 TLS 版本（二者都支持的最高版本） 
  和密码套件。基本 TLS 握手中只对服务器进行身份验证。


- *TLS 握手*

  [整个 TLS 握手](https://en.wikipedia.org/wiki/Transport_Layer_Security#Client-authenticated_TLS_handshake) 
  过程需要客户端和服务器之间进行相互身份验证。在此过程中，客户端还必须 
  在建立连接之前向服务器证明其身份的真实性。


- *密码套件*

  [密码套件](https://en.wikipedia.org/wiki/Cipher_suite) 是指一组算法， 
  用于在客户端和服务器进行安全通信期间对数据进行加密和身份验证。客户端和服务器 
  必须先就密码套件达成一致，然后才能进行超越握手的通信。


- *PKI（公钥基础设施）*

  PKI（[公钥基础设施](https://en.wikipedia.org/wiki/Public_key_infrastructure)） 
  为管理数字证书定义了一组角色和程序。该系统 
  负责确保服务器和客户端签发的每个证书的真实性。在 PKI 中， 
  CA（证书颁发机构）负责签发数字证书。这些证书用于验证 
  持证者（服务器/客户端）的真实性。


- *公钥和私钥*

  [公钥密码系统](https://en.wikipedia.org/wiki/Public-key_cryptography) 
  是一种使用数学相关密钥对为数据进行加密和签名的系统。公钥密码系统中的每对密钥 
  都包含一个广为人知的公钥和 
  一个只有一方知道的私钥匙。使用私钥给数据签名或加密，任何接收方都可以使用匹配的公钥 
  对数据进行身份验证和/或解密。使用公钥加密的数据 
  只能由私钥持有人解密。TLS 在 TLS 握手期间使用公钥密码系统。


- *CA 根证书*

  [CA 根证书](https://en.wikipedia.org/wiki/Root_certificate) 证实了 
  证书颁发机构的真实性。该根证书是最顶层的证书， 
  用于对证书颁发机构颁发的证书进行签名。例如，在采用了 TLS 的 MQTT 演示中， 
  CA 根证书可配置为使用公共 MQTT 代理（例如 [test.mosquitto.org](http://test.mosquitto.org/)）， 
  或使用 AWS IoT Core 时，CA 根证书是 
  [推荐使用的 IoT Core CA 证书](https://docs.aws.amazon.com/iot/latest/developerguide/server-authentication.html)之一。


- *mbed TLS*

  [mbed TLS](https://en.wikipedia.org/wiki/Mbed_TLS) 是 TLS 的一种实现， 
  专为内存受限的嵌入式 IoT 设备而设计。它使用 TLS 堆栈的最小子集。
