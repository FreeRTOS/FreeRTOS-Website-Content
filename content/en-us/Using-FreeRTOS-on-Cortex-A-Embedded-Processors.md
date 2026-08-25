---
title: Using FreeRTOS on ARM Cortex-A9 Embedded Processors
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**That incorporate a Generic Interrupt Controller (GIC)**


## Introduction

The information on this page is relevant to both the 32-bit ARMv7-A and 64-bit ARMv8-A RTOS ports.

Some ARM Cortex-A processors incorporate ARM's own Generic Interrupt Controller (GIC), while others
incorporate proprietary interrupt controllers. Separate web pages are provided to give instructions
on using the RTOS in both scenarios. This page provides information on running the RTOS on an ARM
Cortex-A embedded processor that uses the ARM GIC. See also the web page that
describes [running the RTOS on an ARM Cortex-A embedded processor that uses a proprietary interrupt controller](Using-FreeRTOS-on-Cortex-A-proprietary-interrupt-controller).

## Features of the FreeRTOS ARM Cortex-A kernel port

The FreeRTOS ARM Cortex-A port:

* Extends the use of the familiar, small, simple, deterministic, de facto standard FreeRTOS kernel
  beyond the microcontroller market
* Implements a full interrupt nesting model
* Allows a subset of interrupts to remain enabled even inside RTOS critical sections[^1]
* Includes hardware floating point support
* Uses a flat/linear memory model (the MMU is not supported).

[^1]: The ARM Cortex-A hardware will itself globally disable interrupts when an interrupt is taken,
and dictates that interrupts are globally disabled when certain operations are performed. These
are the only times interrupts are globally disabled, and interrupts are always re-enabled as soon
as possible.


## Using the floating point unit (FPU) in interrupts

By default, the Cortex-A9 port does not support the use of the floating point unit in interrupts. If
it is necessary to use the floating point unit in interrupts then it will also be necessary to save
the entire floating point context to the stack on entry to each (potentially nested) interrupt. From
FreeRTOS V9.0.0 the FreeRTOS GCC Cortex-A port can do this automatically for you - see the description
of the vApplicationFPUSafeIRQHandler() callback function in the [Interrupt Handling](#interrupt-handling)
section below.


## Using the floating point unit (FPU) in tasks

To prevent processor register corruption a task must not use any floating point registers unless it
has a floating point context. Whether or not RTOS tasks are created with a floating point context by
default depends on the compiler in use, and the configUSE\_TASK\_FPU\_SUPPORT setting in FreeRTOSConfig.h.

A newly created task will not have a floating point context if:

* You are using a FreeRTOS version older than V9.0.0, **or**
* You are using a compiler other than GCC, **or**
* configUSE\_TASK\_FPU\_SUPPORT is set to 1 in FreeRTOSConfig.h, **or**
* configUSE\_TASK\_FPU\_SUPPORT is undefined.

A newly created task will already have a floating point context if:

* You are using FreeRTOS V9.0.0 **or** later, **and**
* The GCC compiler is used, **and**
* configUSE\_TASK\_FPU\_SUPPORT is set to 2 in FreeRTOSConfig.h.

A task that does not have a floating point context must create a floating point
context for itself by calling portTASK\_USES\_FLOATING\_POINT() before any floating point
calculations are executed. It is only necessary to
call portTASK\_USES\_FLOATING\_POINT() once per task. For example:

```c
void vATaskFunction( void *pvParameters )
{
double x, y;

    /* This task is going to use floating point operations. Therefore it calls
       portTASK_USES_FLOATING_POINT() once on task entry, before entering the loop
       that implements its functionality. From this point on the task has a floating
       point context. */
    portTASK_USES_FLOATING_POINT();

    /* Enter the loop that implements the task's function. */
    for( ;; )
    {
        /* portTASK_USES_FLOATING_POINT() has already been called, so it is safe
           to use the floating point x and y variables here... */
        x = [whatever];
        y = [whatever];
    }
}
```
*Calling portTASK_USES_FLOATING_POINT() before any floating point calculations are performed*


## Important note for GCC (and possibly other compiler) users:

Some GCC libraries optimise memory copy and memory set (and possibly other)
functions by making use of the wide floating point registers. Therefore, by default,
**any** task that uses functions such as memcpy(), memcmp() or memset(), or
uses a FreeRTOS API function such as xQueueSend() which itself uses memcpy(), will
inadvertently corrupt the floating point registers. Further, **any** interrupt
that calls a FreeRTOS queue or semaphore function will also corrupt the floating
point context as they too make use of memcpy().

To avoid this either:

* Use library functions that do not use the floating point registers, and if
  that is not possible provide your own implementation of memcpy(), memcmp()
  and memset() to ensure the versions provided by the library are not used.

* Make use of the portTASK\_USES\_FLOATING\_POINT() and vApplicationFPUSafeIRQHandler()
  functions described on this page.


## Essential information on interrupt priorities

The RTOS Cortex-A port implements a full interrupt nesting scheme, the behaviour
of which is dependent on the configMAX\_API\_CALL\_INTERRUPT\_PRIORITY setting.
configMAX\_API\_CALL\_INTERRUPT\_PRIORITY [must be defined in FreeRTOSConfig.h](#arm-cortex-a-specific-freertosconfigh-settings).

Interrupts assigned a priority at or below the priority set by configMAX\_API\_CALL\_INTERRUPT\_PRIORITY
can call interrupt safe FreeRTOS API functions, and will nest. Interrupt safe
FreeRTOS API functions are those that end in "FromISR" (FreeRTOS maintains a separate
interrupt API to ensure interrupt entry is as efficient and simple as possible).

Interrupts assigned a priority above the configMAX\_API\_CALL\_INTERRUPT\_PRIORITY setting
will not be affected by RTOS critical sections, and will nest, but **cannot call
any FreeRTOS API functions**.

**Special Note 1:** In ARM interrupt controllers, higher
numeric interrupt priority values denote lower logical interrupt priorities. Therefore an
interrupt priority of 5 is lower than an interrupt priority of 4. If
configMAX\_API\_CALL\_INTERRUPT\_PRIORITY is set to 5, then it is correct for an interrupt
handler that calls an interrupt safe API function to be assigned a priority of
5 or 6, but it is **not correct** for it to be assigned a priority of 4.

**Special Note 2:** The interrupt controller's internal
representation of priority bits can be ignored. If the interrupt controller
implements 32 unique priority levels, then the only valid values for
configMAX\_API\_CALL\_INTERRUPT\_PRIORITY are 1 to 30. Likewise, if the interrupt
controller implements 16 unique priority levels then valid values are 1 to 14.

**Special Note 3:** Interrupt controllers that can
sub-divide interrupt priority bits into preemption priorities and sub-priorities
should have all bits configured as preemption priority. In the ARM generic
interrupt controller (GIC) this means the interrupt controller's binary point
register must be set to 0.


## ARM Cortex-A specific FreeRTOSConfig.h settings

The following settings must be included in FreeRTOSConfig.h:

* configINTERRUPT\_CONTROLLER\_BASE\_ADDRESS

  Must be set to the base address of the ARM Generic Interrupt Controller (GIC)

* configINTERRUPT\_CONTROLLER\_CPU\_INTERFACE\_OFFSET

  The offset from configINTERRUPT\_CONTROLLER\_BASE\_ADDRESS at which the
  GIC's CPU interface starts. Typically this will be 0x1000.

* configUNIQUE\_INTERRUPT\_PRIORITIES

  The number of unique priorities that can be specified in the GIC.

* configMAX\_API\_CALL\_INTERRUPT\_PRIORITY

  See the [interrupt priorities](#essential-information-on-interrupt-priorities) section.

**Note:** If there is an official demo for the Cortex-A9 processor you are using then the
FreeRTOSConfig.h file provided with the demo will already contain the correct settings.


## Configuring and installing the RTOS tick interrupt

Every official FreeRTOS demo that targets an ARM Cortex-A based embedded processor
includes code to configure a timer to generate the RTOS tick interrupt, and install
the FreeRTOS tick interrupt handler. The following information is only required
if you need to change the provided implementation.

The macro configSETUP\_TICK\_INTERRUPT() is called by the RTOS kernel port layer.
configSETUP\_TICK\_INTERRUPT() must be #defined in FreeRTOSConfig.h to configure
a peripheral to generate a periodic interrupt at the frequency set by the
configTICK\_RATE\_HZ FreeRTOSConfig.h setting. FreeRTOS\_Tick\_Handler() must then
be installed as the interrupt's handler function. For example:


```c
/* Implement a function in a C file to generate a periodic interrupt at the
   required frequency. */
void vSetupTickInterrupt( void )
{
/* FreeRTOS_Tick_Handler() is itself defined in the RTOS port layer. An extern
   declaration is required to allow the following code to compile. */
extern void FreeRTOS_Tick_Handler( void );

    /* Assume TIMER1\_configure() configures a hypothetical timer peripheral called
    TIMER1 to generate a periodic interrupt with a frequency set by its parameter. */
    TIMER1_configure( configTICK_RATE_HZ );

    /* Next assume Install\_Interrupt() installs the function passed as its second
       parameter as the handler for the peripheral passed as its first parameter. */
    Install_Interrupt( TIMER1, FreeRTOS_Tick_Handler );
}
```
*Defining a function that configures a timer to generate a periodic tick*


```c
/* Given the function definition above, add the following line to FreeRTOSConfig.h. */
#define configSETUP_TICK_INTERRUPT() vSetupTickInterrupt()
#defining configSETUP_TICK_INTERRUPT() to the function that generates the periodic tick
```

## Interrupt handling

Every official FreeRTOS demo that targets an ARM Cortex-A based embedded processor
includes code that handles interrupts. The following information is only required
if you need to change the provided implementation.

Interrupt entry, nesting, and exit code is provided by the RTOS kernel port layer.
After an interrupt has been entered the RTOS port layer executes a callback function
that must be provided by the application writer. Individual interrupt service
routines can then be called by the callback function. An example is provided [below](#interrupt-handling).

The callback function can be called either vApplicationIRQHandler(), or if you
are using GCC and FreeRTOS V9.0.0 or later, vApplicationFPUSafeIRQHandler().

```c
/* The two callback function options. In both cases ulICCIAR is passed as the value
   of the interrupt controller's ICCIAR (interrupt acknowledge register). */
void vApplicationIRQHandler( uint32_t ulICCIAR );
void vApplicationFPUSafeIRQHandler( uint32_t ulICCIAR );
```

If the application writer provides a callback function called vApplicationIRQHandler() then
floating point registers will not be saved on entry to the interrupt, and the
interrupt must not use any floating point instructions or registers. If the
application writer instead provides a callback function called
vApplicationFPUSafeIRQHandler() then floating point registers will be saved on
entry to each (potentially nested) interrupt, which will use more stack space and
slow down interrupt entry, but allow interrupt handlers to use FPU registers. See the
"[Using the floating point unit (FPU) in interrupts](#using-the-floating-point-unit-fpu-in-interrupts)" section above.

The callback function (vApplicationIRQHandler() or vApplicationFPUSafeIRQHandler())
is called with interrupts disabled, but can (and in
most cases should) enable interrupts. Below is an example implementation:

```c
/* vApplicationIRQHandler() is just a normal C function. */
void vApplicationIRQHandler( uint32_t ulICCIAR )
{
uint32_t ulInterruptID;

    /* In the 64-bit Cortex-A RTOS port it is necessary to clear the source of
       the interrupt BEFORE interrupts are re-enabled. */
    ClearInterruptSource();

    /* Re-enable interrupts. */
    __asm volatile( "CPSIE I" );

    /* The ID of the interrupt can be obtained by bitwise ANDing the ICCIAR value
       with 0x3FF. */
    ulInterruptID = ulICCIAR & 0x3FFUL;

    /* On the assumption that handlers for each interrupt are stored in an array
       called InterruptHandlerFunctionTable, use the interrupt ID to index to and
       call the relevant handler function. */
    InterruptHandlerFunctionTable[ ulInterruptID ]();
}
```
*An example implementation of vApplicationIRQHandler()*


## Installing the FreeRTOS IRQ and SWI (SVC) interrupt handlers

FreeRTOS\_IRQ\_Handler() must be installed as the Cortex-A's IRQ handler.

FreeRTOS\_SWI\_Handler() must be installed as the Cortex-A's SWI (SVC) handler.

If it is not possible to edit the interrupt vector code then map the FreeRTOS
handlers to the required handler names using #defines in FreeRTOSConfig.h. For example,
if the installed handlers are called IRQ\_Handler() and SWI\_Handler() respectively, then
the FreeRTOS handlers can be mapped to these names by adding the following two lines
to FreeRTOSConfig.h.


```c
#define FreeRTOS_IRQ_Handler IRQ_Handler
#define FreeRTOS_SWI_Handler SWI_Handler
```
*Mapping the FreeRTOS interrupt handler names to alternative handler names*


## ARMv7A processor modes and stacks

The C start up code must, as a minimum, configure stacks for the IRQ and Supervisor modes
of the Cortex-A processor. **main() must be called from a privileged mode, preferably
Supervisor mode**.

It is not necessary to allocate a stack to User/System mode unless main() is
called from System mode (main() must not be called from User mode). If a stack
is allocated to User/System mode it will not be used after the RTOS kernel has
been started.

The RTOS stack overflow detection functionality only detects overflows in
task stacks, not IRQ or Supervisor stacks.


## ARMv8A exception levels

Currently:

* The RTOS executes at EL3 (Exception Level 3), and uses the EL3 stack.
* RTOS tasks execute at EL3 and use the EL1 stack.
