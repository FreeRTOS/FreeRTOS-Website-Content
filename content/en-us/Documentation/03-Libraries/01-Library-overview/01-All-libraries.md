---
title: FreeRTOS libraries
created: 2018-09-20
feature: standard
categories:
  - kernel
description: A brief introduction to FreeRTOS libraries.
related links: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Begginer's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
---

## Introduction

All the libraries listed below are [MIT (open source) licensed](https://opensource.org/licenses/MIT) 
and are designed for resource constrained devices such as microcontrollers and small microprocessors. 
FreeRTOS core and FreeRTOS for AWS libraries do not have any dependencies other than on the standard 
C library – they are not even dependent on an RTOS.

```jsx
<hr />
```

## FreeRTOS Plus

Libraries that implement additional functionality and, unlike the core libraries (see below), have a dependency 
on the FreeRTOS RTOS kernel.

```jsx
<LibrariesPlus />
<hr />
```

## FreeRTOS Core

FreeRTOS Core libraries implement open standards based connectivity, security, and related functionality. 
These libraries are suitable for building smart microcontroller-based devices that connect to the cloud. 
Unlike the FreeRTOS-Plus libraries (see above), FreeRTOS Core libraries have no dependencies other than 
on the standard C libraries, so FreeRTOS Core libraries are not dependent on the FreeRTOS RTOS kernel.

```jsx
<LibrariesCore />
<hr />
```

## FreeRTOS for AWS IoT

FreeRTOS for AWS libraries implement clients for AWS IoT specific value add cloud services, including 
over the air updates (OTA). These libraries are suitable for building smart microcontroller-based devices 
that connect to the AWS IoT cloud. Like the FreeRTOS core libraries, they have no dependencies on anything 
other than the standard C library, so are not dependent on the FreeRTOS RTOS kernel. See all library categories.

```jsx
<LibrariesIot />
<hr />
```

## FreeRTOS Lab libraries

FreeRTOS Labs projects are functional but either incomplete, experimental, or simply provided for open 
source community interest. The banner on the documentation page of each Labs library describes which 
criteria applies to that library.

```jsx
<LibrariesLab />
```
