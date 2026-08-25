---
title: "FreeRTOS software timers"
created: 2018-09-20
categories:
  - kernel
description: FreeRTOS software timers
relatedLinks:
  - title: API reference - software timers
    link: /Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/
---

[[More about software timers...](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)]

### Resetting a software timer

It is possible to re-set a timer that has already started to run. Resetting a
timer results in the timer recalculating its expiry time so the expiry time
becomes relative to when the timer was reset, and not when the timer was
originally started. This behaviour is demonstrated in the next diagram, where
Timer 1 is a one-shot timer that has a period equal to 5 seconds.

In the depicted example, it is assumed that the application switches on an LCD
back-light when a key is pressed, and that the back-light remains on until 5
seconds pass without any keys being pressed. Timer 1 is used to switch off the
LCD back-light when this 5 seconds has elapsed.

![The behaviour of one-shot timers and auto-reload timers](/media/2018/resetting-a-FreeRTOS-software-timer.png)  
_Timer behaviour when a timer is reset_
