---
title: FreeRTOS FAQ - ISR's
created: 2018-09-20
description: Troubleshooting ISR's
---


## Can a context switch occur within an ISR?

Yes. Each RTOS port provides a macro to request a context switch from within an ISR. The name of the 
macro is dependent on the port (for historic reasons). It will be either 
portYIELD\_FROM\_ISR() or portEND\_SWITCHING\_ISR. Refer to 
the [documentation page](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)
for the port being used.

Every official port comes with a demo application that demonstrates context switching from an ISR.


## How do I write an RTOS safe ISR?

That is very dependent on the microcontroller and tool chain port of FreeRTOS being used. Refer to 
the [documentation page](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices) and demo application 
for the RTOS port being used.


## Can interrupts be nested?

It depends on the port. See the description of 
the [configKERNEL\_INTERRUPT\_PRIORITY and configMAX\_SYSCALL\_INTERRUPT\_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#kernel_priority) 
configuration parameters for additional information.
