---
title: TLS Introduction
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Internet of Things (IoT) use cases require application protocols like [MQTT](https://en.wikipedia.org/wiki/MQTT)
and [HTTP](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) to be encrypted and authenticated. So
it is common to use these protocols in combination with Transport Layer
Security ([TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) ). MQTT over TLS is described in
the [MQTT 3.1 specification](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718098),
and HTTP over TLS is described in the [HTTPS specification](https://tools.ietf.org/html/rfc2818#section-2).

Transport Layer Security ([TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) ) is a cryptographic
protocol that is designed to provide secure communications over the internet between a client and server. It
is meant to ensure the safe delivery of data between a client and server, but it does NOT account for security
at the endpoints (the client or server side). Clients signal to the server that they wish to establish a TLS
connection, then the client and server use a [handshake protocol](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/03-TLS-terminology) to negotiate how they
will establish trust between one another. Once the handshake protocol has been completed, data can be sent
between the two parties using the encryption method negotiated during the handshake.

It is common for only the client to authenticate the server, for example when a web browser connects to
an HTTPS web server. IoT devices often use “mutual authentication”, where the server also authenticates the
identity of the IoT device client.


## Implementation

The [TLS Protocol](https://tools.ietf.org/html/rfc5246) implemented is v1.2
