---
title: MCUBoot
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**NOTE**:
The FreeRTOS MCUBoot demo is a [FreeRTOS Lab Project](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) provided for community
interest and to serve as a reference. It is fully functional, but may not comply with our production code
standards. It is available from the [Lab-Project-FreeRTOS-MCUBoot](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-MCUBoot)
repository on GitHub.


## Introduction

MCUBoot is a configurable secure bootloader maintained by several industry leaders. It can operate as
the first or second stage bootloader, with support for cryptographic verification of software images with
support for these schemes:

* ECDSA-P256
* RSA-2048
* RSA-3072

By default, it supports image reversion whereby downloaded firmware image updates are tentatively booted once.
Upon the initial upgrade boot, if the upgrade image marks itself as confirmed, it is retained as the
primary image. If the upgrade image is not confirmed, the subsequent boot will rollback to the prior
confirmed image. If no valid image is available in any slot, the device bricks itself as a safety
precaution. The developers of MCUBoot have more detailed documentation in
their [docs](https://github.com/mcu-tools/mcuboot/tree/main/docs) repository on GitHub.

MCUBoot also provides subset support for [MCUMGR](https://github.com/apache/mynewt-mcumgr-cli) when a
device enters serial boot recovery mode.
If enabled, serial mode can be triggered during bootup via user input, such as a button hold. The MCUMGR
interface enables users to retrieve image diagnostics from the board, query resets, upload/modify images,
and more.
