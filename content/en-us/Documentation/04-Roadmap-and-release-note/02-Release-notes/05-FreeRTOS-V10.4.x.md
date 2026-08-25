---
title: "Upgrading From FreeRTOS V10.3.0 to V10.4.x"
created: 2018-09-20
categories:
  - roadmap and release notes
description: Information on Upgrading From FreeRTOS V10.3.0 to V10.4.x
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
---


### Note on future versioning:

Until now the FreeRTOS zip file releases have carried the version number of the kernel release they contain.
For example, FreeRTOSv10.4.0.zip contains version 10.4.0 of the FreeRTOS kernel. However, the kernel is not
the only individually versioned library contained in the zip file, and the number of libraries in the zip
file will increase in future releases. Therefore, to better reflect that the zip file actually contains a
collection of libraries integrated together, future releases will use a date stamp version instead of the
kernel’s version


### Backward Compatibility

FreeRTOS V10.4.0 is a drop in replacement for FreeRTOS V10.3.x for all ports other than those supporting
memory protection units (MPUs). The page that documents the FreeRTOS MPU
port [provides upgrade information](/Security/04-FreeRTOS-MPU-memory-protection-unit#upgrading-to-FreeRTOS-10.4.0).

A note for Tracealyzer users: The task notification feature in FreeRTOS V10.4.0 is backward compatible
with that in FreeRTOS V10.3.x with the exception of trace recorder macros. Tracealyzer users will need to
update their trace recorder code to that provided in the FreeRTOS V10.4.0 release, and set
TRC\_CFG\_FREERTOS\_VERSION to TRC\_FREERTOS\_VERSION\_10\_4\_0 in their trcConfig.h files.

See the [change history](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history) for more
details of new ports and other enhancements.


### Feature enhancements

#### Direct to Task Notification Enhancements

Prior to FreeRTOS V10.4.0 each task only had a
single [direct to task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications).
From FreeRTOS V10.4.0 each task has a [user definable array of task notifications](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtask_notification_array_entries).

### Other Changes

#### Contributed Linux Port change

The old Linux FreeRTOS port provided by William Davy has been replaced with an enhanced port provided by
David Vrabel. The new version fixes a long standing scheduler bug where two tasks could execute at the same
time during a context switch. Read  [the Linux simulator documentation](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux) for
more information.


#### Formatting Changes

Code formatting is now automated to facilitate the increase in
collaborative development in Git. The auto-formatted code is not identical
to the original formatting conventions. Most notably spaces are now used
in place of tabs.
