---
title: X.509 证书
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

在通过互联网进行安全通信时，客户端（IoT 设备）和服务器必须提供 
其身份证明，方可建立双向验证的 [TLS](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/02-TLS-introduction) 
连接。[公钥基础设施 (PKI)](https://en.wikipedia.org/wiki/Public_key_infrastructure) 中会交换[数字（或身份）证书](https://en.wikipedia.org/wiki/Public_key_certificate)， 
以验证各实体的身份。[X.509 证书](https://en.wikipedia.org/wiki/X.509) 
是最常见的数字证书格式，广泛应用于互联网和 IoT 用例。 
X.509 证书 
会在 [TLS 握手过程](https://en.wikipedia.org/wiki/Transport_Layer_Security#Client-authenticated_TLS_handshake) 中进行交换， 
因此是建立 TLS 连接的关键部分。在 IoT 用例中，只有在建立 TLS 连接后，才能通过  
[HTTPS](https/index.md) 或 [MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 等通信协议 
传输数据。

在 PKI 中，签名的真实性通过密钥对（一个公钥和一个私钥）建立。 
公钥可能会广泛传播，而私钥仅为其所有者所知，这样做是为了 
维护整个系统的安全。使用私钥对数据进行签名或加密时，数据的所有接收者都可以 
使用匹配的公钥对数据进行验证和/或解密。使用公钥加密的数据 
只能由私钥持有者解密。

生成密钥对后，客户端 
将使用证书签名请求 (CSR) 向证书颁发机构申请 X.509 证书。X.509 证书可以 
由 CA（[证书颁发机构](https://en.wikipedia.org/wiki/Certificate_authority)）签名，也可以自签名。在大多数用例中， 
X.509 证书仅在 
为[根 CA 的证书](https://en.wikipedia.org/wiki/Root_certificate) 时才会自签名。在 IoT 用例中， 
更为常见的做法（也是更好的做法！）是由中间 CA（而不是根 CA）签署每个终端实体的 
证书，这样可防止暴露根证书的风险。使用中间证书可以形成 
[信任链](https://en.wikipedia.org/wiki/Chain_of_trust)，该信任链能够从根 CA 一直追溯到每个 
终端实体。 

如需了解更多详细信息，请点击此处：[X.509 RFC5280](https://tools.ietf.org/html/rfc5280)。

