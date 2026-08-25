---
title: vEventGroupDelete()
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[Event Group API](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)]

event\_groups.h

```c
 void vEventGroupDelete( EventGroupHandle_t xEventGroup );
```

Delete an [event group](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups) that was previously
created using a call to [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate).

Tasks that are blocked on the event group being deleted will be unblocked, and
report an event group value of 0.

The RTOS source file FreeRTOS/source/event\_groups.c must be
included in the build for the vEventGroupDelete() function to be available.

This function cannot be called from an interrupt.


**Parameters:**

- *xEventGroup*

  The event group being deleted.


**Returns:**

*None.*
