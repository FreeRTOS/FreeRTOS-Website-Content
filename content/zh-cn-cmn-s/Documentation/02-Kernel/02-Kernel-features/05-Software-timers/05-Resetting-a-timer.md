---
title: "FreeRTOS 软件定时器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 软件定时器
relatedLinks:
  - title: API 引用——软件定时器
    link: /Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/
---

[[关于软件定时器的更多信息……](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)]

### 重置软件定时器

可重置已开始运行的定时器。重置定时器会导致计时器重新计算到期时间，
到期时间将与
重置定时器的时间挂钩，
而非最初启动定时器的时间。下图演示了此行为，
其中 Timer 1 是一次性定时器，周期等于 5 秒。

在所描绘的示例中，假设应用程序在按下某个键时打开 LCD 背光，
并且保持开启状态，
如果没有按下任何键，可保持 5 秒。Timer 1 用于
在 5 秒后关闭 LCD 背光。

![一次性定时器和自动重载定时器的行为方式](/media/2018/resetting-a-FreeRTOS-software-timer.png)  
_定时器重置时的定时器行为_
