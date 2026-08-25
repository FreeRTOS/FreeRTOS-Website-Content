---
title: "Debugging Hard Fault & Other Exceptions on ARM Cortex-M3 and ARM Cortex-M4 microcontrollers"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Introduction

The ARM Cortex-M core implements a set of fault exceptions. Each exception relates to an
error condition. If the error occurs, the ARM Cortex-M core stops executing the current
instruction, and branches to the exception's handler function. This mechanism is
just like that used for interrupts, where the ARM Cortex-M core branches to an interrupt
handler when it accepts an interrupt.

The CMSIS names for the fault handlers are as follows:

- UsageFault_Handler()
- BusFault_Handler()
- MemMang_Handler()
- HardFault_Handler()

The exact circumstances under which the ARM Cortex-M core calls each of these handlers
is out of scope of this document. See the ARM Cortex-M literature from ARM, and various
other sources, if you are interested in the details. For the purpose of this
document it is enough to say that, if your application ends up in one of these
handlers, then something has gone wrong. Hard faults are the most common fault
type, as other fault types that are not enabled individually will be escalated to
become a hard fault.

Despite the numerous RTOS support requests from people explaining that, when
using the RTOS kernel, their application ends up in the hard fault handler, when
the issue has been worked through, it is always shown that the cause of the
hardware fault is not the kernel, but one of the following:

- A misunderstanding of interrupt priorities on the ARM Cortex-M core (easy to do!),
  or a misunderstanding of how to use the FreeRTOS interrupt nesting model. The
  "[Running the RTOS on a ARM Cortex-M Core](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)"
  documentation page is provided specifically to assist with this.

- A general RTOS user error. The FAQ
  "[My Application Does Not Run - What Could Be Wrong](/Why-FreeRTOS/FAQs/Troubleshooting)" page
  is provided specifically to assist with this.

- A bug in the application code.

Hard fault debugging should start by ensuring the software application follows
the guidelines provided on the two pages linked to in the first two bullet points
above. If, after that, hard faults still persist, then it will be necessary to
determine the system state at the time the fault occurred. Debuggers do not always
make that easy, so the rest of this page describes a software technique than can
be used for the purpose.

## Determining Which Exception Handler is Executing

It is common for interrupt vector tables to install the same handler for every
interrupt/exception source. The default handlers are declared as
[weak symbols](https://en.wikipedia.org/wiki/Weak_symbol)
to allow the application writer to install their own handler simply by
implementing a function with the correct name. If an interrupt occurs for which
the application writer has not provided their own handler then the default handler
will execute.

Default interrupt handlers are typically implemented as an infinite loop. If an
application ends up in such a default handler it is first necessary to determine
which interrupt is actually executing.

The code snippet below demonstrates how to add a few instructions to a default
infinite loop handler to load the number of the executing interrupt into register
2 (r2) before the infinite loop is entered.

Interrupt numbers read from the NVIC in this way are
relative to the start of the vector table, in which entries for system exceptions
(such as the hard fault) appear before entries for peripheral interrupts.
If r2 contains the value 3 then, a hard fault exception is being handled.
If r2 contains a value equal to or greater than 16, then a peripheral interrupt
is being handled - and the interrupting peripheral can be determined by subtracting
16 from the interrupt number.

```c
Default_Handler:
  /* Load the address of the interrupt control register into r3. */
     ldr r3, NVIC_INT_CTRL_CONST
  /* Load the value of the interrupt control register into r2 from the
     address held in r3. */
  ldr r2, [r3, #0]
  /* The interrupt number is in the least significant byte - clear all
     other bits. */
  uxtb r2, r2
Infinite_Loop:
  /* Now sit in an infinite loop - the number of the executing interrupt
     is held in r2. */
  b  Infinite_Loop
  .size  Default_Handler, .-Default_Handler

.align 4
/* The address of the NVIC interrupt control register. */
NVIC_INT_CTRL_CONST: .word 0xe000ed04
```

## Debugging a ARM Cortex-M Hard Fault

The stack frame of the fault handler contains the state of the ARM Cortex-M registers
at the time that the fault occurred. The code below shows how to read the
register values from the stack into C variables. Once this is done, the values of
the variables can be inspected in a debugger just as an other variable.

First, a very short assembly function is defined to determine which stack was being
used when the fault occurred. Once this is done, the fault handler assembly code passes a pointer to the
stack into a C function called prvGetRegistersFromStack().

The fault handler is shown below using GCC syntax. Note that the function is declared
as being naked, so it does not contain any compiler generated code (for example,
there is no function entry prologue code).

```c
/* The prototype shows it is a naked function - in effect this is just an
   assembly function. */
static void HardFault_Handler( void ) __attribute__( ( naked ) );

/* The fault handler implementation calls a function called
   prvGetRegistersFromStack(). */
static void HardFault_Handler(void)
{
    __asm volatile
    (
        " tst lr, #4                                                \n"
        " ite eq                                                    \n"
        " mrseq r0, msp                                             \n"
        " mrsne r0, psp                                             \n"
        " ldr r1, [r0, #24]                                         \n"
        " ldr r2, handler2_address_const                            \n"
        " bx r2                                                     \n"
        " handler2_address_const: .word prvGetRegistersFromStack    \n"
    );
}
```

The implementation of prvGetRegistersFromStack() is shown below. prvGetRegistersFromStack()
copies the register values from the stack into the C variables, then sits in a
loop. The variables are named to indicate the register value that they hold.
Other registers will not have changed since the fault occurred, and can be viewed
directly in the debugger's CPU register window.

```c
void prvGetRegistersFromStack( uint32_t *pulFaultStackAddress )
{
/* These are volatile to try and prevent the compiler/linker optimising them
   away as the variables never actually get used. If the debugger won't show the
   values of the variables, make them global my moving their declaration outside
   of this function. */
volatile uint32_t r0;
volatile uint32_t r1;
volatile uint32_t r2;
volatile uint32_t r3;
volatile uint32_t r12;
volatile uint32_t lr; /* Link register. */
volatile uint32_t pc; /* Program counter. */
volatile uint32_t psr;/* Program status register. */

    r0 = pulFaultStackAddress[ 0 ];
    r1 = pulFaultStackAddress[ 1 ];
    r2 = pulFaultStackAddress[ 2 ];
    r3 = pulFaultStackAddress[ 3 ];

    r12 = pulFaultStackAddress[ 4 ];
    lr = pulFaultStackAddress[ 5 ];
    pc = pulFaultStackAddress[ 6 ];
    psr = pulFaultStackAddress[ 7 ];

    /* When the following line is hit, the variables contain the register values. */
    for( ;; );
}
```

## Using the Register Values

[See also "[Handling Imprecise Faults](#handling-imprecise-faults)" below]

The first register of interest is the program counter. In the code
above, the variable pc contains the program counter value. When the fault is a
precise fault, the pc holds the
address of the instruction that was executing when the hard fault (or other fault)
occurred. When the fault is an imprecise fault, then
[additional steps are
required](#handling-imprecise-faults) to find the address of the instruction that caused the fault.

To find the instruction at the address held in the pc variable, either...

1. Open an assembly code window in the debugger, and manually enter
   the address to view the assembly instructions at that address, or

2. Open the break point window in the debugger, and manually define an execution or access
   break point at that address. With the break point set, restart the application to
   see which line of code the instruction relates to.

Knowing the instruction that was being executed when the fault occurred allows
you to know which other register values are also of interest. For example, if
the instruction was using the value of R7 as an address, then the value of R7 needs to be know.
Further, examining the assembly code, and the C code that generated the assembly code, will show
what R7 actually holds (it might be the value of a variable, for example).

## Handling Imprecise Faults

ARM Cortex-M faults can be precise or imprecise. If the IMPRECISERR bit (bit 2)
is set in the BusFault Status Register (or BFSR, which is byte accessible at
address 0xE000ED29) is set then the fault is imprecise.

It is harder to determine the
cause of an imprecise fault because the fault will not necessarily occur concurrently
with the instruction that caused the fault. For example, if writes to memory
are cached then there might be a delay between an assembly
instruction initiating a write to memory and the write to memory actually occurring.
If such a delayed write operation is invalid (for example, a
write is being attempted to an invalid memory location) then an imprecise fault
will occur, and the program counter value obtained using the code above
will not be the address of the assembly instruction that initiated the write
operation.

In the above example, turning off write buffering by setting the DISDEFWBUF bit (bit 1) in the Auxiliary Control Register (or ACTLR) will result in the imprecise
fault becoming a precise fault, which makes the fault easier to debug, albeit at
the cost of slower program execution.
