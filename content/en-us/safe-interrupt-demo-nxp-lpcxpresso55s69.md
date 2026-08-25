---
title: Safer Interrupt Handling Demo for the  NXP LPCXpresso55S69 Development Board
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Introduction

[FreeRTOS ports with Memory Protection Unit (MPU) support](/Security/04-FreeRTOS-MPU-memory-protection-unit) enable
microcontroller applications to be more robust and more secure by running application tasks in unprivileged
mode. These unprivileged mode tasks have access only to their own stacks and some pre-configured memory regions.
On these MPU enabled microcontrollers, the only sections of application code that run in privileged mode are
Interrupt Service Routines (ISRs). In most applications, it is best practice to keep ISRs as short as possible
to maintain real-time responsiveness. On a microcontroller with an MPU, keeping ISRs short also makes the
application more secure as it minimizes time spent in privileged mode. This demo shows an approach to keeping
ISRs short by deferring most of the processing work to unprivileged tasks.


## Source Code Organization

The FreeRTOS zip file download contains the source code for all the FreeRTOS ports, and every demo
application. That means it contains many more files than are required to use the FreeRTOS ARMv8-M
Cortex-M33 port. See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page for information
on the zip file's directory structure.

The project file for this demo has the usual Eclipse project name .project and is located in the
`FreeRTOS/Demo/Safe_Interrupts_M33F_NXP_LPC55S69_MCUXpresso/MCUXpresso` directory. The
FreeRTOS ARMv8-M Cortex-M33 port files compiled in this project are in the
`FreeRTOS/Source/portable/GCC/ARM_CM33_NTZ/non_secure` directory.


## Concept

The application creates an interrupt queue (a standard FreeRTOS Queue) to which all ISRs post requests.
These requests are handled later by an unprivileged interrupt handler task. The interrupt handler task
runs at the highest priority to ensure that interrupt requests are not delayed because of other tasks.
The ISRs unblock the high priority interrupt handler task then return directly to the interrupt handler
task instead of the previously executing task.

[![](/media/2021/concept-interrupt-1.jpg)](/media/2021/concept-interrupt-1.jpg)

The design pattern can be easily extended to mimic interrupt nesting by having additional interrupt
queues and corresponding interrupt handler tasks at different priorities.

[![](/media/2021/concept-interrupt-2.jpg)](/media/2021/concept-interrupt-2.jpg)

In the above example image, the UART interrupt is handled by the low priority interrupt handler and,
therefore, can be interrupted by the GPIO interrupt which is handled by the high priority interrupt
handler.


## The Demo Application

The project includes two demos:

1. GPIO Demo
2. UART Demo


### GPIO Demo

The GPIO Demo consists of a task which periodically toggles the onboard RGB LED. When the user presses
the USER button on the LPC55S69-EVK, the GPIO interrupt is asserted and the corresponding interrupt handler
posts a request to the interrupt queue. The interrupt handler task handles this request and changes the
color of the LED.

```c
void userButtonPressedHandler( void )
{
    UserIrqRequest_t xIrqRequest;
    BaseType_t xHigherPriorityTaskWoken;

    /* We have not woken a task at the start of the ISR. */
    xHigherPriorityTaskWoken = pdFALSE;

    /* Post a request to the interrupt queue which will be later processed by
     * the unprivileged interrupt handler task. */
    xIrqRequest.xHandlerFunction = vButtonPressedIRQHandler;
    xIrqRequest.ulData = 0; /* Not used. */
    xQueueSendFromISR( xUserIrqQueueHandle, &( xIrqRequest ), &( xHigherPriorityTaskWoken ) );

    /* Posting the above request might have unblocked the interrupt handler task.
     * Make sure to always return to the interrupt handler task instead of the
     * previously executing task. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
**User Button Pressed ISR**


### UART Demo


The UART Demo consists of a task which prints a command menu on the serial console and waits for user
input. When the user provides input on the serial console, the UART Rx interrupt is asserted and the
corresponding interrupt handler posts a request to the interrupt queue. The interrupt handler task handles
this request and posts the results for the requested command to the serial console.

```c
void uartRxInterruptHandler( void )
{
    UserIrqRequest_t xIrqRequest;
    BaseType_t xHigherPriorityTaskWoken;

    /* We have not woken a task at the start of the ISR. */
    xHigherPriorityTaskWoken = pdFALSE;

    /* Post a request to the interrupt queue which will be later processed by
     * the unprivileged interrupt handler task. */
    xIrqRequest.xHandlerFunction = vUartDataReceivedIRQHandler;
    xIrqRequest.ulData = ( uint32_t ) USART_ReadByte( USART0 );
    xQueueSendFromISR( xUserIrqQueueHandle, &( xIrqRequest ), &( xHigherPriorityTaskWoken ) );

    /* Posting the above request might have unblocked the interrupt handler task.
     * Make sure to return to the interrupt handler task in case it was not already
     * running. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
**UART Rx ISR**


## Building and Running the RTOS Demo Application

1. Launch the MCUXpresso IDE. Note that you need the MCUXpresso IDE version 10.3.1 or higher to be able to
   build and run this demo.

2. Choose the workspace directory and click "**Launch**".

   [![](/media/2021/launch-workspace.jpg)](/media/2021/launch-workspace.jpg)

3. Open the Import Project dialog by clicking "**File -> Import...**".

   [![](/media/2021/import-project.jpg)](/media/2021/import-project.jpg)

4. Select "**General -> Existing Projects into Workspace**" and click "**Next**".

   [![](/media/2021/existing-project.jpg)](/media/2021/existing-project.jpg)

5. Click "**Browse...**" next to "**Select root directory**" and select the
   `FreeRTOS/Demo/Safe_Interrupts_M33F_NXP_LPC55S69_MCUXpresso` directory. A project named
   FreeRTOSDemo should be visible in the Projects pane as shown below. Click "**Finish**".

   [![](/media/2021/select-root-dir.jpg)](/media/2021/select-root-dir.jpg)

6. Build the project by right-clicking on FreeRTOSDemo and selecting "**Build Project**".

   [![](/media/2021/interrupt-build-project.jpg)](/media/2021/interrupt-build-project.jpg)

7. Power up the board using the "Debug Link (P6)" micro USB port.

8. Select the project by clicking "**FreeRTOSDemo**". Go to "**Debug your project**"
   in the Quickstart Panel and click on "**Program flash action using LinkServer**" in the dropdown
   as shown below.

   [![](/media/2021/program-flash-action.jpg)](/media/2021/program-flash-action.jpg)

9. LPC-LINK2 probe should be shown in the "Probes Discovered" window. Click "**OK**".

   [![](/media/2021/connect-to-target.jpg)](/media/2021/connect-to-target.jpg)

10. SWD Device 0 should be selected in the "**SWD Configuration**" window. Click "**OK**".

   [![](/media/2021/swd-configuration.jpg)](/media/2021/swd-configuration.jpg)

11. You should see "Finished writing Flash successfully" in the logs. Click "**OK**".

   [![](/media/2021/file-into-flash.jpg)](/media/2021/file-into-flash.jpg)

12. Go to "**Debug your project**" in the Quickstart Panel and click "**Debug using LinkServer probes**"
   in the dropdown as shown below to start the debug session.

   [![](/media/2021/debug-using.jpg)](/media/2021/debug-using.jpg)


## RTOS Configuration and Usage Details

Also see the page that  [describes running FreeRTOS on ARMv8-M cores](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers),
and the page that describes [setting ARM Cortex-M interrupt priorities for use with FreeRTOS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4).


* Configuration items specific to this demo are contained in
 `FreeRTOS/Demo/Safe_Interrupts_M33F_NXP_LPC55S69_MCUXpresso/Projects/MCUXpresso/Config/FreeRTOSConfig.h`.
 The constants defined in that file can be edited to suit your application. The following configuration options
 are specific to the ARM Cortex-M33 port:

	+ `configENABLE_MPU` - Enable/Disable Memory Protection Unit (MPU).
	+ `configENABLE_FPU` - Enable/Disable Floating Point Unit (FPU).
	+ `configENABLE_TRUSTZONE` - Enable/Disable TrustZone.

* This demo runs FreeRTOS on the secure side, and therefore, sets `configENABLE_TRUSTZONE`
  to 0 and `configRUN_FREERTOS_SECURE_ONLY` to 1 in the `FreeRTOSConfig.h` file. It uses
  the FreeRTOS port files in the `FreeRTOS/Source/portable/GCC/ARM_CM33_NTZ` directory.

* `Source/Portable/MemMang/heap_4.c` is included in the project to provide the memory
  allocation required by the RTOS kernel. Please refer to the "Memory Management" section of the API
  documentation for full information.

* `vPortEndScheduler()` has not been implemented.
