---
title: FreeRTOS 库
created: 2018-09-20 00:00:00.0 UTC
feature: standard
categories:
- 内核
description: FreeRTOS 库简介。
related links:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
- title: FreeRTOS 简介
  link: /Why-FreeRTOS/What-is-FreeRTOS/
- title: FreeRTOS 初学者指南
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
- title: 下载 FreeRTOS
  link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
- title: 常见问题
  link: /Why-FreeRTOS/FAQs
---

## 引言

下列所有库均基于 [MIT（开源）许可](https://opensource.org/licenses/MIT)， 
专为资源受限的设备（如微控制器和小型微处理器）而设计。 
FreeRTOS Core 和适用于 AWS 的 FreeRTOS 库除了标准 C 库之外没有其他依赖项， 
甚至不依赖 RTOS。

```jsx
<hr />
```

## FreeRTOS Plus

与 Core 库（见下文）不同，实现附加功能的库依赖 
FreeRTOS RTOS 内核。

```jsx
<LibrariesPlus />
<hr />
```

## FreeRTOS Core

FreeRTOS Core 库可实现基于开放标准的连接、安全性和相关功能。 
这些库适用于构建连接到云端的基于微控制器的智能设备。 
与 FreeRTOS-Plus 库（见上文）不同，FreeRTOS Core 库除了标准 C 库之外没有其他依赖项， 
因此 FreeRTOS Core 库不依赖 FreeRTOS RTOS 内核。

```jsx
<LibrariesCore />
<hr />
```

## 适用于 AWS IoT 的 FreeRTOS

适用于 AWS 的 FreeRTOS 库可实现针对 AWS IoT 特定增值云服务 
（包括 over the air (OTA) 更新）的客户端。这些库适用于构建连接到 
AWS IoT 云的基于微控制器的智能设备。与 FreeRTOS Core 库一样，它们除了标准 C 库之外没有其他依赖项， 
因此不依赖 FreeRTOS RTOS 内核。查看所有库类别。

```jsx
<LibrariesIot />
<hr />
```

## FreeRTOS Lab 库

FreeRTOS Labs 项目具有实用性，但同时欠完整，或处于实验阶段， 
或仅为开源社区提供。每个 Labs 库文档页面上的横幅会描述 
适用于该库的标准。

```jsx
<LibrariesLab />
```

