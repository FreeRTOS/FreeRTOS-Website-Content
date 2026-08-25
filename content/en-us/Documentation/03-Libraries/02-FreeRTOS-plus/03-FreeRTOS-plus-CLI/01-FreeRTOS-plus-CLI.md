---
title: FreeRTOS-Plus-CLI
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**An Extensible Command Line Interface Framework**


## Introduction

FreeRTOS-Plus-CLI (Command Line Interface) provides a simple, small, extensible and RAM efficient method
of enabling your FreeRTOS application to process command line input. The steps required to add a
command are shown in the clickable diagram below - **click each stage in the process individually** to
be taken to a worked example.

[![Provide a function that implements the FreeRTOS-Plus-CLI command behaviour](/media/2018/Creating-a-command-step-1.png)](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/02-Implementing-a-command)

![FreeRTOS command line interpreter sequence separator](/media/2018/Creating-a-command-sequence-arrow.png)

[![Provide a const struct that maps the command to the function that implements the command](/media/2018/Creating-a-command-step-2.png)](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/04-Registering-a-command)

![FreeRTOS command line interpreter sequence separator](/media/2018/Creating-a-command-sequence-arrow.png)

[![Register the const struct with the FreeRTOS command interpreter FreeRTOS-Plus-CLI](/media/2018/Creating-a-command-step-3.png)](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/04-Registering-a-command)

![FreeRTOS command line interpreter sequence separator](/media/2018/Creating-a-command-sequence-arrow.png)

[![Provide character input and output functions](/media/2018/Creating-a-command-step-4.png)](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/06-A-FreeRTOS-plus-CLI-task)
*Adding a command to FreeRTOS-Plus-CLI. **This diagram is clickable**.*


FreeRTOS-Plus-CLI is available in the following directory of the
 official [FreeRTOS zip file download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS): `FreeRTOS-Plus/Source/FreeRTOS-Plus-CLI`.
 Several [example projects](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/08-Demos)
 are also available on this website.

From FreeRTOS V10.0.0 FreeRTOS-Plus-CLI is provided under the [same MIT license as the FreeRTOS kernel.](/Documentation/03-Libraries/01-Library-overview/04-Licensing)
