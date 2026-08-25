---
title: 什么是 FreeRTOS？
created: 2023-05-16 00:00:00.0 UTC
categories:
  - 开始使用
description: FreeRTOS 的历史和当前功能简介。
featuredImage: /media/2023/what_is_freertos.png
feature: blog
relatedLinks:
  - title: 为什么使用 FreeRTOS？
    link: /Why-FreeRTOS/Why-FreeRTOS
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
next:
  title: RTOS 基础知识
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/01-RTOS-fundamentals
---

<blockquote>
  <span class="content">
    “提供超越商业替代品用户所要求的质量和服务的免费产品”
  </span>
</blockquote>

15 多年来，FreeRTOS 专职开发人员一直与全球 
顶尖的芯片公司紧密合作， 
为客户提供[市场领先](https://www.embedded.com/electronics-blogs/embedded-market-surveys/4458724/2017-Embedded-Market-Survey)以及 
完全免费的商用级、[高品质](/Documentation/02-Kernel/06-Coding-guidelines/02-FreeRTOS-Coding-Standard-and-Style-Guide) **RTOS**和工具……但 
什么是 RTOS？

此页面首先介绍了操作系统的定义，接着具体定义了 
[实时操作系统](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel)，然后 
更进一步定义了实时定时器内核（或实时执行器）。

另请参阅常见问题项目“[为什么用 RTOS](/Why-FreeRTOS/FAQs/What-is-this-all-about#why-use-an-rtos)” ，了解有关在什么情况使用和为什么
在嵌入式系统软件设计中使用 RTOS 会有帮助。


## 什么是通用操作系统？

操作系统是支持计算机基本功能的计算机程序， 
为在计算机上运行的程序（或*应用程序*）提供服务。应用程序提供计算机用户 
想要或需要的功能。操作系统提供的服务使得应用程序写入更快、更简单、 
并且更易于维护。如果您正在阅读此网页，说明您正在使用网络浏览器（提供您感兴趣的功能的应用程序 
），该浏览器本身会在操作系统提供的环境中运行 
。


## 什么是 RTOS？

大多数操作系统似乎能同时执行多个程序。这称为多任务处理。实际上， 
每个处理器内核在任何给定时间点都只能运行一个执行线程。操作系统中 
一个名为调度器的部分负责决定何时运行哪个程序， 
并通过在每个程序之间快速切换以造成同时执行的假象。

操作系统的类型取决于调度器如何决定何时运行哪个程序。例如， 
多用户操作系统（如 Unix）中使用的调度器将确保每个用户都能获得合理的处理时间 
。再比如，桌面操作系统（如 Windows）中的调度器会努力确保计算机对用户作出响应。 
（**注意：FreeRTOS 并非大型操作系统，也不是为在台式
计算机级处理器上运行而设计的，我使用这些例子纯粹是因为它们是读者熟悉的系统。**）

实时操作系统中的调度器旨在提供
可预测的（通常描述为 
*确定性*）执行模式。这对嵌入式系统而言意义重大，因为嵌入式系统 
经常有实时要求。实时要求是指定嵌入式系统 
必须在严格定义的时间内（*截止时间*）响应某个事件。只有当操作系统调度器的行为 
可以预测（因此具有确定性）时， 
才能保证满足实时要求。

传统的小型实时调度器（如 [FreeRTOS](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/04-Task-scheduling) 中使用的调度器）
通过允许用户为每个执行线程分配优先级来实现确定性。然后，调度器根据优先级来判断 
下一个要运行的执行线程。在 FreeRTOS 中，执行线程称为 *任务*。


## 什么是 FreeRTOS？

(另请参阅“[有关 FreeRTOS](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel) 的更多信息”)

FreeRTOS 是 RTOS 的一个类别，设计得足够小，可以在微控制器上运行， 
但其用途并不局限于微控制器应用程序。

微控制器是一种小型且资源有限的处理器， 
在单个芯片上集成了处理器本身、  用于保存待执行程序的只读存储器（ROM 或闪存）  以及执行程序所需的随机存取存储器（RAM） 
。通常情况下，程序是  直接从只读存储器中执行的。

微控制器通常用于深度嵌入式应用中（在这些应用中， 
实际上看不到处理器本身，也看不到它们运行的软件）， 
它们通常有非常具体和专门的工作要做。由于大小限制和专用终端应用的性质，很少有理由使用完整的 RTOS 实现， 
或者说，使用完整的 RTOS 实现是不可能的。因此，FreeRTOS 只提供核心的实时调度功能、 
任务间通信、定时和同步原语。这意味着 
将它描述为实时内核或实时执行器更准确。其他功能，如命令控制台 
接口或网络堆栈，可通过附加组件实现。
