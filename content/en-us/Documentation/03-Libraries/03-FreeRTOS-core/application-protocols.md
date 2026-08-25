---
title: "Application Protocols"
created: 2018-09-20
categories:
  - kernel
description: A brief introduction to FreeRTOS application protocol libraries
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
---

Application Protocol libraries provide connectivity for building microcontroller-based IoT devices. The 'core'
branded application protocols are 'standalone' in that they do not have any dependencies outside of the C library.
They use a simple transport interface definition to ensure they are not dependent on the underlying TCP/IP stack.

### coreMQTT

A lightweight pub/sub protocol for IoT use cases.
Source code is now available in [coreMQTT](https://github.com/FreeRTOS/coreMQTT/releases/latest) github repository.
[Learn More](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)

### coreMQTT Agent

A thread safe MQTT library using coreMQTT for IoT use cases.
Source code is now available in [coreMQTT-Agent](https://github.com/FreeRTOS/coreMQTT-Agent/releases/latest) github repository.
[Learn More](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent)

### coreHTTP

A lightweight request and response messaging protocol for IoT use cases.
Source code is now available in [coreHTTP](https://github.com/FreeRTOS/coreHTTP/releases/latest) github repository.
[Learn More](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP)

### coreSNTP

The coreSNTP library provides a client for the Simple Network Time Protocol (SNTP) to allow devices
to synchronize their system clocks with time servers. This library implements the SNTPv4 specification defined in
[RFC 4330](https://tools.ietf.org/html/rfc4330).
Source code is now available in [coreSNTP](https://github.com/FreeRTOS/coreSNTP/releases/latest) github repository.
[Learn More](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP)

### Transport Interface

Interface for sending and receiving data that is not dependent on the underlying TCP/IP stack.
[Learn More](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)

### coreJSON

A parser that strictly enforces the ECMA-404 JSON standard.
Source code is now available in [coreJSON](https://github.com/FreeRTOS/coreJSON/releases/latest) github repository.
[Learn More](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)

### corePKCS #11

A cryptographic API layer (OASIS standard) that abstracts key storage, get/set properties for cryptographic
objects, and session semantics.
Source code is now available in [corePKCS11](https://github.com/FreeRTOS/corePKCS11/releases/latest) github repository.
[Learn More](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)
