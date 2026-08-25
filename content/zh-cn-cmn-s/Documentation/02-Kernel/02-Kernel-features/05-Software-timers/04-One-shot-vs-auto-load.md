---
title: "FreeRTOS 软件定时器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 软件定时器
relatedLinks:
  - title: API 引用 — 软件定时器
    link: /Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/
---

[[关于软件定时器的更多信息……](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)]

### 一次性定时器与自动重载定时器

定时器有两种类型，一次性定时器和自动重载定时器。一
次性定时器启动后只会执行一次回调函数。它可以
手动重新启动，但不会自动重新启动。与一次性定时器相反，
自动重载定时器一旦启动，将在每次执行调用回调函数后，自动重新启动，
从而周期性地执行回调。

下图中的时间线展示了一次性定时器和自动重载定时器之间活动行为的差异
。在此图中，定时器 1 是
定时为 100 的一次性定时器，定时器 2 是自动重载
定时器，定时为 200。

![一次性定时器和自动重载定时器的行为方式](/media/2018/one-shot-timer-behaviour-vs-auto-reload-timer-behaviour.png)

一次性定时器和自动重载定时器的行为方式
