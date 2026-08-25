---
title: Porting FreeRTOS-Plus-TCP to a New Embedded C Compiler
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


### Summary Bullet Points

* The FreeRTOS-Plus-TCP source code has two compiler dependencies:

  1. How the compiler is told to pack C structures (that is,
     not leave any alignment bytes between the members of the
     C structure). Packing
     structures is very important to ensure data appears
     correctly in the TCP, UDP, IP and Ethernet frames.

  2. How the compiler and MCU RTOS port define an interrupt
     service routine (ISR).
     The embedded IP stack only uses interrupts to manage the
     Ethernet driver, and so this topic is not covered here.

* The syntax used to ensure C structures are packed correctly is
  placed in a compiler specific header file to ensure the non-portable
  code is not included in the core embedded IP stack source code.

* Two header files are required for each embedded C compiler.
 
  1. pack\_struct\_start.h contains the keywords required
     to appear before the definition of a C structure that
     must be packed.
  2. pack\_struct\_end.h contains the keywords required
     to appear after the definition of a C structure that
     must be packed.

* Compiler specific header files that ship with the embedded TCP/IP
  stack are located in the FreeRTOS-Plus/FreeRTOS-Plus-TCP/portable/Compiler
  directory tree.


### Detailed Explanation and Example

The FreeRTOS-Plus-TCP implementation uses C structures to map onto the TCP, IP,
ARP, DNS, DHCP, etc. protocol headers within the Ethernet frames. C
compilers normally lay out the memory used to hold a C structure such that
access to the C structure's members is optimised for the MCU architecture on
which the embedded software is running. This means empty padding bytes
are placed between C structure members to achieve a byte alignment that
is natural for the MCU.

For example, consider the following
structure defined on a 32-bit MCU:
 
```c
    struct a_struct  
    {  
        uint8_t Member1;  
        uint8_t Member2;  
        uint8_t Member3;  
        uint32_t Member4;  
    }  
```
*Example C structure definition*


The first three members are 8 bits each, and will most likely appear in three
consecutive bytes of the same 32-bit word. The forth member is 32-bits, and
can be accessed most efficiently (dependent on the MCU, but in most cases)
if it is placed on a 32-bit (four byte) boundary.
Therefore, without the structure being packets, the compiler will most
likely add a 'padding' byte between Member3 and Member4 to
move the start address of Member4 up one byte and so onto a 32-bit boundary.
The structure will then appear in memory as follows:
 
```c
    struct a_struct  
    {  
        uint8_t Member1;  At address 0 (first byte of first 32-bit word)  
        uint8_t Member2;  At address 1 (second byte of first 32-bit word)  
        uint8_t Member3;  At address 2 (third byte of first 32-bit word)  
        **Padding byte At address 4 (forth byte of the first 32-bit word)**  
        uint32_t Member4; Now at address 4, the first byte of the second 32-bit word  
    }  
```
*Example of how the C structure will appear in the MCU memory*

However, the TCP/IP protocol headers do not have padding bytes, so the compiler
must be instructed not to add them additional bytes into structures that
map onto the IP protocol headers that a written to or read from Ethernet
frames. Structures that do not contain padding bytes are said to be 'packed'. The
syntax required to ensure structures are packed depends on the embedded C
compiler. The FreeRTOS-Plus-TCP implementation cannot use any
C compiler specific syntax in the common (not MCU port specific) files,
and instead allows users to define their own packing directives in two
very simple header files that are then included from the C files.
 
Structures that require packing appear in the FreeRTOS-Plus-TCP code as follows:
 
```c
    #include "pack_struct_start.h"  
    struct a_struct  
    {  
        uint8_t Member1;  
        uint8_t Member2;  
        uint8_t Member3;  
        uint32_t Member4;  
    }  
    #include "pack_struct_end.h"  
```
*A structure wrapped in pack_struct_start.h and pack_struct_end header file inclusions*

A version of pack\_struct\_start.h and pack\_struct\_end.h that contains compiler
specific syntax can then be provided for each compiler.
 
For example, the directory FreeRTOS-Plus/FreeRTOS-Plus-UDP/portable/Compiler/GCC
contains definitions suitable for use with the GCC compiler. pack\_struct\_start.h is
empty because GCC does not require any special syntax at the start of the structure.
pack\_struct\_end.h contains the following single
line of code:

```c
    __attribute__( (packed) );
```

So, after pre-processing the C source code appears to the compiler
as shown below, which is valid GCC syntax:

```c
    struct a_struct  
    {  
        uint8_t Member1;  
        uint8_t Member2;  
        uint8_t Member3;  
        uint32_t Member4;  
    }  
    __attribute__( (packed) );  
```
*How GCC sees a packed structure after pack_struct_start.h and pack_struct_end.h have been included*

FreeRTOS-Plus/FreeRTOS-Plus-TCP/portable/Compiler/GCC is already included
in the FreeRTOS-Plus-TCP download and can be used as a refeference when porting to
other embedded C compilers.

**pack\_struct\_end.h must, as a minimum, contain at least a semicolon ( ; )
to mark the end of the structure definition.** It is sometimes valid
for pack\_struct\_start.h to be empty, but it is never valid for pack\_struct\_end.h to
be completely empty.
