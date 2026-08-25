---
title: xEventGroupCreateStatic
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[Event Group API](00-Event-groups)]

[**TIP: 'Task Notifications' can provide a light weight alternative to event groups in many situations**](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group)

event\_groups.h

```c
EventGroupHandle_t xEventGroupCreateStatic(
                             StaticEventGroup_t *pxEventGroupBuffer );
```

Creates a new RTOS [event group](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups), and returns a handle by which the newly created
event group can be referenced. [configSUPPORT\_STATIC\_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation)
must be set to 1 in FreeRTOSConfig.h and the RTOS source file FreeRTOS/source/event\_groups.c must be
included in the build for the `xEventGroupCreateStatic()` function to be available.

Each event group requires a (very) small amount of RAM that is used to hold the
event group's state. If an event group is created using [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate)
then the required RAM is automatically allocated from the [FreeRTOS heap](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).
If an event group is created using `xEventGroupCreateStatic()`
then the RAM is provided by the application writer, which requires an additional
parameter, but allows the RAM to be statically allocated at compile
time. See the [Static Vs Dynamic allocation](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation) page for more information.

Event groups are stored in variables of type `EventBits_t`. The number of
bits (or flags) implemented within an event group is 8 if [configUSE\_16\_BIT\_TICKS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_16_bit_ticks) is set to
1, or 24 if `configUSE_16_BIT_TICKS` is set to 0. The dependency on `configUSE_16_BIT_TICKS` results from
the data type used for thread local storage in the internal implementation of RTOS tasks.


**Parameters:**

- *pxEventGroupBuffer*

  Must point to a variable of type `StaticEventGroup_t`, in which the event group data structure will be stored.


**Returns:**

- If the event group was created successfully then a handle to the event
  group is returned.

- If `pxEventGroupBuffer` was NULL then NULL is returned.


**Example usage:**

```c
    /* Declare a variable to hold the handle of the created event group. */
    EventGroupHandle_t xEventGroupHandle;

    /* Declare a variable to hold the data associated with the created
       event group. */
    StaticEventGroup_t xCreatedEventGroup;

    /* Attempt to create the event group. */
    xEventGroupHandle = xEventGroupCreateStatic( &xCreatedEventGroup );

    /* pxEventGroupBuffer was not null so expect the event group to have
       been created? */
    configASSERT( xEventGroupHandle );
```
