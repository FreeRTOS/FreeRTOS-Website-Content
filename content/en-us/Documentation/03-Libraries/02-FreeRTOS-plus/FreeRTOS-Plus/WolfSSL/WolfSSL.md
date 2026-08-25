---
title: WolfSSL
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


State of the art networking security for embedded systems

**-  [Evaluate Now in the FreeRTOS Windows Simulator](FreeRTOS_WolfSSL_Example) -**

**Technology Highlights**

* Up to 20x smaller than OpenSSL
* Only requires 20-100KB Flash
* Only requires 1-36kB RAM
* Supports TLS 1, 1.1 and 1.2 (client and server)
* Supports DTLS 1 and 1.2 (client and server)
* Hashing functions: MD2, MD4, MD5, SHA-1, SHA-2, SHA-256, SHA-384, SHA-512, BLAKE2b, and RIPEMD-160
* Block, Stream, and AEAD ciphers: AES (CBC, CTR, GCM, CCM), Camellia, DES, 3DES, ARC4, RABBIT, HC-128 ciphers
* Public key options: RSA, DSS, DH, EDH, NTRU
* Private key encryption: PKCS #8, #5, #12
* Supports PEM and DER certificates
* Key generation and ECC support
* Certificate generation
* FreeRTOS port layer
* OpenSSL compatibility layer


## Introduction

WolfSSL is a lightweight TLS/SSL library. It is used to add **security**, **authentication**, **integrity**
and **confidentiality** to network communications.

WolfSSL is about 10 times smaller than yaSSL, and can be up to 20 times
smaller than OpenSSL (depending on the build configuration). User feedback
also reports dramatically better performance when compared to OpenSSL in
standard SSL operations.

WolfSSL's small size, speed and feature set make it ideal for
use with FreeRTOS, but WolfSSL does not compromise on functionality. It
supports the latest industry standards, such as
the [Transport Security Layer](http://en.wikipedia.org/wiki/Transport_Layer_Security)
(TLS) protocol version 1.2, as well as progressive streaming, block, and AEAD ciphers
such as [AES-GCM](http://en.wikipedia.org/wiki/Galois/Counter_Mode), [RABBIT](http://www.ecrypt.eu.org/stream/rabbitpf.html),
and [NTRU](http://en.wikipedia.org/wiki/NTRU).


## FreeRTOS Integration Example

WolfSSL is already ported to FreeRTOS, and an example project [is provided](FreeRTOS_WolfSSL_Example).
The example runs in the FreeRTOS Windows simulator, allowing WolfSSL to be
evaluated in a FreeRTOS environment from the convenience of a standard Windows
computer, without the need for external target hardware.


## Application Integration

WolfSSL is delivered as a set of ANSI standard
C source files that can be added to any C project, and built with any
ANSI compatible C compiler. Instructions for building WolfSSL with
a cross compiler are contained in the user manual.

WolfSSL has a simple API, and can be added into existing applications
just as easily as it can be used in new applications.
The [Simple WolfSSL Client Side Usage Example](Using-SSL-TLS-in-a-client-site-application)
and [Simple WolfSSL Server Side Usage Example](Using-SSL-TLS-in-a-server-site-application)
pages on this website demonstrate the steps necessary for a basic integration, and
the [provided FreeRTOS simulator example project](FreeRTOS_WolfSSL_Example)
can be used as a reference.
The user manual contains a complete configuration and API reference.
