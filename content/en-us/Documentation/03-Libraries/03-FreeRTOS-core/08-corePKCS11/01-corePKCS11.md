---
title: "corePKCS11"
created: 2018-09-20
categories:
  - kernel
description: An introduction to the corePKCS11 library
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/

external Links:
  - title: corePKCS11 API reference
    link: https://freertos.github.io/corePKCS11/v3.5.0/
---


## Introduction

corePKCS11 is a software based mock implementation of a subset of the PKCS #11 application programming 
interface (API). It is provided to enable hardware independent rapid prototyping and development before 
switching to a security hardware specific implementation in production devices.

[PKCS #11](https://en.wikipedia.org/wiki/PKCS_11) is a standardised and widely used API for manipulating 
common cryptographic objects. It is important because the functions it specifies allow application software 
to use, create, modify, and delete cryptographic objects without ever exposing those objects to the 
application's memory. For example, FreeRTOS AWS reference integrations use **a small subset of** the 
PKCS #11 API to, among other things, access the secret (private) key necessary to create a network connection 
that is authenticated and secured by the [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) 
(TLS) protocol - without the application ever 'seeing' the key. PKCS #11 is maintained by 
the [OASIS PKCS#11 Technical Committee](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=pkcs11).

Generally vendors for secure cryptoprocessors such as Trusted Platform Module (TPM), Hardware Security 
Module (HSM), Secure Element, or any other type of secure hardware enclave, distribute a PKCS #11 implementation 
with the hardware. The purpose of the corePKCS11 software only mock is therefore to provide a hardware 
independent PKCS #11 implementation for development use before switching to a security hardware specific 
implementation in production devices.

Since the PKCS #11 interface is defined as part of 
the [PKCS #11 specification](https://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html) 
replacing this library with another implementation should require little porting effort, as the interface 
will not change. The system tests distributed with corePKCS #11 can be leveraged to verify your hardware 
specific PKCS #11 implementation behaves the same as corePKCS11.


**Code Size of corePKCS11 (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| --- | --- | --- |
| core\_pkcs11.c | 0.8K | 0.8K |
| core\_pki\_utils.c | 0.5K | 0.3K |
| core\_pkcs11\_mbedtls.c | 8.9K | 7.5K |
| Total estimates | 10.2K | 8.6K |
