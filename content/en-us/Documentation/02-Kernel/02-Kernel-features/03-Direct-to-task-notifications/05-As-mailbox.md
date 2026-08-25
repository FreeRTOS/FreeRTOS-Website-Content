---
title: "RTOS task notifications"
created: 2018-09-20
categories:
  - kernel
description: FreeRTOS queues
relatedLinks:
  - title: API reference - Semaphores and Mutexes
    link: /Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores/
  - title: RTOS task notifications
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications/
  - title: As a binary semaphore
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore/
  - title: As a light weight counting semaphore
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore/
  - title: As a light weight event group
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group/
---

Used As Light Weight Mailbox

RTOS task notifications can be used to send data to a task, but in a much more
restricted way than can be achieved with an RTOS queue because:

1. Only 32-bit values can be sent
2. The value is saved as the receiving task's [notification value](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications), and there
   can only be one notification value at any one time

Hence the phrase 'lightweight mailbox' is used in preference to 'lightweight queue'.
The task's notification value is the mailbox value.

Data is sent to a task using the [xTaskNotify()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) (or xTaskNotifyIndexed())
and [xTaskNotifyFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/07-xTaskNotifyFromISR) (or xTaskNotifyIndexedFromISR()) API
functions with their eAction parameter set to either eSetValueWithOverwrite or
eSetValueWithoutOverwrite. If eAction is set to eSetValueWithOverwrite then the
receiving task's notification value is updated even if the receiving task already
had a notification pending. If eAction is set to eSetValueWithoutOverwrite then
the receiving task's notification value is only updated if the receiving task
did not already have a notification pending - as to update the notification value
would overwrite the previous value before the receiving task had processed it.

A task can read its own notification value using [xTaskNotifyWait()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait)
(or xTaskNotifyWaitIndexed()).

See the documentation for the relevant API functions for examples.
