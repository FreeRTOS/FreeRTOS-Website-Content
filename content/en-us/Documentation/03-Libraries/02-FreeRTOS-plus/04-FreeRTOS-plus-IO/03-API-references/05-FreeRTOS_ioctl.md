---
title: "FreeRTOS_ioctl()"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-IO API](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/01-FreeRTOS_IO_API_Functions)]

FreeRTOS_IO.h

```c
BaseType_t FreeRTOS_ioctl( Peripheral_Descriptor_t const xPeripheral,
                           uint32_t ulRequest,
                           void *pvValue );
```

Short for Input Output Control, ioctl() is the standard name for functions that are used for input output
device control, including device specific configuration. FreeRTOS\_ioctl() is the FreeRTOS-Plus-IO equivalent.
The action to be performed by a call to FreeRTOS\_ioctl() is identified by the request code passed into
FreeRTOS\_ioctl() as the second parameter.


**Parameters:**

- *pxPeripheral*

  The descriptor associated with the peripheral the FreeRTOS_ioctl() call will affect. The descriptor
  will have been returned from the [FreeRTOS\_open()](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/02-FreeRTOS_open) call used to open the peripheral.

- *ulRequest*

  The request code. Generic request codes [are listed below](#request-code-reference). Board support
  package specific request codes are provided with the [board support package](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/Board_Support_Packages)
  documentation.

- *pvValue*

  A parameter that is specific to the request code being used. For example, where the request code is
  used to set a timeout value, the parameter is used to define the timeout. Many request codes do not
  require a parameter. When this is the case, for future compatibility, it is advised to set pvValue
  to NULL. pvValue is a void pointer so it can be used to pass any data type - be it a simple integer
  value (cast to a void \*), or a pointer to a more complex data type.


**Returns:**

- pdPASS is returned if the request code was processed successfully.
- pdFAIL is returned in other cases.


**Example usage:**

All these code examples assume the pxPort descriptor has already been opened, and is valid.

The example 1 code snippet demonstrates how to configure a peripheral to use the zero copy transfer
mode. The pvValue parameter is not used with this request, so is set to NULL.

```c
FreeRTOS_ioctl( pxPort, ioctlUSE_ZERO_COPY_TX, NULL );
```
*Example 1: Configuring the peripheral associated with the pxPort descriptor to*

The example 2 code snippet demonstrates how to configure a peripheral's write timeout. In this case,
the pvValue parameter is used to pass the timeout value in ticks. The constant portTICK\_PERIOD\_MS
is used to convert 200 milliseconds into ticks.

```c
FreeRTOS_ioctl( pxPort, ioctlSET_TX_TIMEOUT, ( void * ) ( 200 / portTICK_PERIOD_MS ) );
```
*Example 1: Configuring the write timeout for the peripheral associated with the pxPort descriptor.*

The example 3 code snippet demonstrates how to set the slave address associated with an I2C port. In
this case, the pvValue parameter is used to pass the slave address to use, which is 0x20.

```c
FreeRTOS_ioctl( pxPort, ioctlSET_I2C_SLAVE_ADDRESS, ( void * ) 0x20 );
```
*Example 1: Using FreeRTOS_ioctl() to set the slave address associated with an I2C port.*


## Request Code Reference

### Request codes that set the transfer mode to use

The following request codes are used to set the [transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/06-Transfer-modes).
The [board support package](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/Board_Support_Packages) documentation details
which transfer modes are applicable to which peripherals.

#### ioctlUSE\_POLLED\_TX

  Configure the peripheral to use the [polled transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/07-Polled_Transfer_Mode) when writing bytes.

  All peripherals default to using the polled transfer mode when they are initially opened. Very few
  peripherals currently provide a means of returning to a polled transfer mode after an alternative
  mode has been manually selected.

  **Parameter:** Not used.

#### ioctlUSE\_POLLED\_RX

  Configure the peripheral to use the [polled transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/07-Polled_Transfer_Mode) when reading bytes.

  All peripherals default to using the polled transfer mode when they are initially opened. Very few
  peripherals currently provide a means of returning to a polled transfer mode after an alternative
  mode has been manually selected.

  **Parameter:** Not used.

#### ioctlUSE\_ZERO\_COPY\_TX

  Configure the peripheral to use the interrupt driven [zero copy transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode)
  when writing bytes.

  This request code will enable the peripheral's interrupts, and set the peripheral's interrupt priority
  to the lowest possible value. The ioctlSET\_INTERRUPT\_PRIORITY request code can be used to raise the
  interrupt priority if required.

  Peripheral interrupt service routines are provided within the FreeRTOS-Plus-IO code, so do not need
  to be implemented by the application code.

  **Parameter:** Not used.

#### ioctlUSE\_CHARACTER\_QUEUE\_TX

  Configure the peripheral to use the interrupt driven [character queue transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode)  
  when writing bytes.

  This request code will enable the peripheral's interrupts, and set the peripheral's interrupt priority
  to the lowest possible value. The ioctlSET\_INTERRUPT\_PRIORITY request code can be used to raise the
  interrupt priority if required.

  Peripheral interrupt service routines are provided within the FreeRTOS-Plus-IO code, so do not need
  to be implemented by the application.

  **Parameter:** The length, in bytes, of the queue used to hold bytes that are waiting to be written
  to the peripheral by the FreeRTOS-Plus-IO interrupt service routine. The queue is created by the
  FreeRTOS-Plus-IO code, and does not need to be created by the application code.

#### ioctlUSE\_CHARACTER\_QUEUE\_RX

  Configure the peripheral to use the interrupt driven [character queue transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode)  
  when reading bytes.

  This request code will enable the peripheral's interrupts, and set the peripheral's interrupt priority
  to the lowest possible value. The ioctlSET\_INTERRUPT\_PRIORITY request code can be used to raise the
  interrupt priority if required.

  Peripheral interrupt service routines are provided within the FreeRTOS-Plus-IO code, so do not need
  to be implemented by the application.

  **Parameter:** The length, in bytes, of the queue used to hold bytes that have been received, but not
  yet returned by a call to FreeRTOS\_read(). The queue is created by the FreeRTOS-Plus-IO code, and
  does not need to be created by the application code.

#### ioctlUSE\_CIRCULAR\_BUFFER\_RX

  Configure the peripheral to use the interrupt driven [circular buffer transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/09-Circular_Buffer_Transfer_Mode)
  when reading bytes.

  This request code will enable the peripheral's interrupts, and set the peripheral's interrupt priority
  to the lowest possible value. The ioctlSET\_INTERRUPT\_PRIORITY request code can be used to raise the
  interrupt priority if required.

  Peripheral interrupt service routines are provided within the FreeRTOS-Plus-IO code, so do not need to
  be implemented by the application.

  **Parameter:** The length, in bytes, of the circular buffer used to hold characters received by the
  FreeRTOS-Plus-IO interrupt service routine, but not yet returned by a call to FreeRTOS_read(). The
  circular buffer is created by the FreeRTOS-Plus-IO code, and does not need to be allocated by the
  application code.


### Request codes that affect the behaviour of a transfer mode

The following request codes are specific to one or more transfer modes:

#### ioctlOBTAIN\_WRITE\_MUTEX

  This request code is only applicable when the peripheral is using the interrupt
  driven [zero copy transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode).

  When using the zero copy transfer mode, the peripheral's write mutex must be obtained before calling
  FreeRTOS\_write(). ioctlOBTAIN\_WRITE\_MUTEX is a request to obtain the mutex.

  FreeRTOS\_ioctl() returns pdPASS if the mutex was successfully obtained, and pdFAIL in all other cases.

  The FreeRTOS-Plus-IO interrupt service routine automatically releases the mutex when all the bytes
  have been written. Therefore, successfully obtaining the write mutex is also an indication that no
  writes are currently in progress, and the buffer that was being written is free for re-use.

  The mutex must be manually released using the ioctlRELEASE\_WRITE\_MUTEX request code if it is obtained
  by a task, but the task does not then call FreeRTOS\_write(). See
  the [ioctlWAIT\_PREVIOUS\_WRITE\_COMPLETE](#ioctlwait_previous_write_complete) for an alternative.

  See the example code on the interrupt driven [zero copy write transfer mode documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode).

  **Parameter:** The maximum amount of time, in ticks, that the calling task will wait in
  the [Blocked](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/) 
  state for the mutex to become available.

  The portTICK\_PERIOD\_MS constant can be used to convert milliseconds into ticks. For example, to wait 50
  milliseconds, specify a value of ( 50UL / portTICK\_PERIOD\_MS ).

#### ioctlWAIT\_PREVIOUS\_WRITE\_COMPLETE

  This request code is only applicable when the peripheral is using either the interrupt
  driven [zero copy transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode), or the interrupt
  driven [character queue transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode).

  ioctlWAIT\_PREVIOUS\_WRITE\_COMPLETE results in the calling task being held in
  the [Blocked](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states/) 
  state until the current write operation completes.

  It should be noted that only one task is removed from the Blocked state at a time. Therefore, if two
  tasks use the ioctlWAIT\_PREVIOUS\_WRITE\_COMPLETE request code on the same peripheral simultaneously,
  then only the task with the highest priority will exit the Blocked state when the transmission is complete.

  See the example code on the interrupt driven [zero copy write transfer mode documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode).

  **Parameter:** The maximum amount of time, in ticks, that the calling task will wait in the Blocked
  state for the current write operation to complete.

  The portTICK\_PERIOD\_MS constant can be used to convert milliseconds into ticks. For example, to wait 50
  milliseconds, specify a value of ( 50UL / portTICK\_PERIOD\_MS ).

#### ioctlRELEASE\_WRITE\_MUTEX

  This request code is only applicable when the peripheral is using the interrupt
  driven [zero copy transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/08-Zero_Copy_Transfer_Mode).

  When using the zero copy transfer mode, the peripheral's write mutex must be obtained before calling
  FreeRTOS_write(). The mutex will then be automatically released by the FreeRTOS-Plus-IO interrupt
  service routine when the write is complete.

  The mutex must be manually released using the ioctlRELEASE\_WRITE\_MUTEX request code if it is obtained
  by a task, but the task does not then call FreeRTOS\_write(). See also
  the [ioctlWAIT\_PREVIOUS\_WRITE\_COMPLETE](#ioctlwait_previous_write_complete) and
  ioctlOBTAIN_WRITE_MUTEX request codes.

  **Parameter:** Not used.

#### ioctlSET\_TX\_TIMEOUT

  This request code is only applicable when the peripheral is using the interrupt
  driven [character queue transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode).

  When using the character queue transfer mode, FreeRTOS\_write() places the bytes to be written into
  a queue. If there is not enough space in the queue to hold all the bytes, then the calling task is
  placed into the Blocked state to wait for more space to become available. ioctlSET\_TX\_TIMEOUT sets
  the maximum amount of time the task should remain in the Blocked state. FreeRTOS\_write() returns the
  number of bytes successfully written to the queue, which will be less than the requested number of
  bytes if its write timeout expired.

  **Parameter:** The maximum amount of time, in ticks, that a task calling FreeRTOS\_write() will remain
  in the Blocked state to wait for there to be enough space in the write queue for it to complete its
  FreeRTOS\_write() operation.

  The portTICK\_PERIOD\_MS constant can be used to convert milliseconds into ticks. For example, to set
  a maximum block time of 50 milliseconds, use the value ( 50UL / portTICK\_PERIOD\_MS ).

#### ioctlSET\_RX\_TIMEOUT

  This request code is only applicable when the peripheral is using either the interrupt
  driven [character queue transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode), or the interrupt
  driven [circular buffer transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/09-Circular_Buffer_Transfer_Mode).

  When using one of these modes, FreeRTOS_read() returns bytes that have been buffered (in a queue
  or circular buffer) by the FreeRTOS-Plus-IO interrupt service routine. If the buffer does not already
  contain the requested number of bytes, then the task calling FreeRTOS\_read() is held in the Blocked
  state to wait for more bytes to become available. ioctlSET\_RX\_TIMEOUT is used to set the maximum
  time the task will remain in the Blocked state. FreeRTOS\_read() returns the number of bytes that
  were successfully read, which will be less than the requested number of bytes if its read timeout
  expired.

  **Parameter:** The maximum amount of time, specified in ticks, the task calling FreeRTOS\_read() will
  remain in the Blocked state while it is waiting to complete its FreeRTOS\_read() operation.

  The portTICK\_PERIOD\_MS constant can be used to convert milliseconds into ticks. For example, to set
  a maximum block time of 50 milliseconds, use the value ( 50UL / portTICK\_PERIOD\_MS ).

#### ioctlCLEAR\_RX\_BUFFER

  This request code is only applicable when the peripheral is using either the interrupt
  driven [character queue transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/10-Character_Queue_Transfer_Mode), or the interrupt
  driven [circular buffer transfer mode](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/03-API-references/09-Circular_Buffer_Transfer_Mode). When using one of these
  modes, FreeRTOS\_read() returns bytes that have been buffered (in a queue or circular buffer) by the
  FreeRTOS-Plus-IO interrupt service routine. The ioctlCLEAR\_RX\_BUFFER request code will remove (and
  loose) bytes that are already contained in the buffer, leaving the buffer empty.

  **Parameter:** Not used.


### Request codes that affect the behaviour of more than one type of peripheral

Request codes listed here are applicable to more than one peripheral type.
The [board support package](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_IO/Board_Support_Packages) documentation details which request codes are
applicable to which peripheral.

#### ioctlSET\_SPEED

  Configures the speed of a serial bus. For example, if the peripheral is a UART, this request code will
  set the UART baud rate. This request code is applicable to most, if not all, serial peripherals.

  **Parameter:** The absolute bus speed. For example, use 9600 to set the baud rate of a UART to 9600,
  use 200000 to set the SPI bus speed to 200000.

#### ioctlSET\_INTERRUPT\_PRIORITY

  Sets the priority of interrupts generated by the peripheral.

  Note that, for all FreeRTOS ports that implement
  the [configMAX\_SYSCALL\_INTERRUPT\_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#kernel_priority)
  setting, the priority assigned to an interrupt must be at or below the priority defined by
  configMAX\_SYSCALL\_INTERRUPT\_PRIORITY.

  **Parameter:** The absolute value of the interrupt priority.

  On Cortex-M devices, the interrupt priority must be specified using the format expected by the
  CMSIS NVIC\_SetPriority() function. Remember that Cortex-M devices use numerically low priority
  values to denote high interrupt priorities.


### SPI specific request codes

#### ioctlSET\_SPI\_DATA\_BITS

  Sets the number of data bits used in SPI transfers.

  **Parameter:** The number of data bits. For example, use 8 to specify that data uses 8 bits.

#### ioctlSET\_SPI\_CLOCK\_PHASE

  Sets the SPI clock phase (CPHA).

  **Parameter:** There are two valid values.

  - boardSPI\_SAMPLE\_ON\_LEADING\_EDGE\_CPHA\_0:

    Use boardSPI\_SAMPLE\_ON\_LEADING\_EDGE\_CPHA\_0 to capture data on the leading clock edge (regardless
    of its polarity).

    boardSPI\_SAMPLE\_ON\_LEADING\_EDGE\_CPHA\_0 is equivalent to a CPHA value of 0.

  - boardSPI\_SAMPLE\_ON\_TRAILING\_EDGE\_CPHA\_1:

    Use boardSPI\_SAMPLE\_ON\_TRAILING\_EDGE\_CPHA\_1 to capture data on the trailing clock edge (regardless
    of its polarity).

    boardSPI\_SAMPLE\_ON\_TRAILING\_EDGE\_CPHA\_1 is equivalent to a CPHA value of 1.

#### ioctlSET\_SPI\_CLOCK\_POLARITY

  Sets the polarity of the SPI clock (CPOL).

  **Parameter:** There are two valid values.

  - boardSPI\_CLOCK\_BASE\_VALUE\_CPOL\_1:

    Use boardSPI\_CLOCK\_BASE\_VALUE\_CPOL\_1 to set the base value of the clock between frames to high,
    and the active clock to low.

    boardSPI\_CLOCK\_BASE\_VALUE\_CPOL\_1 is equivalent to a CPOL value of 1.

  - boardSPI\_CLOCK\_BASE\_VALUE\_CPOL\_0:

    Use boardSPI\_CLOCK\_BASE\_VALUE\_CPOL\_0 to set the base value of the clock between frames to low,
    and the active clock to high.

    boardSPI\_CLOCK\_BASE\_VALUE\_CPOL\_0 is equivalent to a CPOL value of 0.

#### ioctlSET\_SPI\_MODE

  Sets the bus into master or slave mode.

  **Parameter:** There are two valid values.

  - boardSPI\_MASTER\_MODE:

    boardSPI\_MASTER\_MODE sets the SPI peripheral into master mode.

  - boardSPI\_SLAVE\_MODE:

    boardSPI\_SLAVE\_MODE sets the SPI peripheral into slave mode. Note that slave mode is not yet supported.


### I2C specific request codes

#### ioctlSET\_I2C\_SLAVE\_ADDRESS

  Sets the address written to when the I2C peripheral is in master mode. All I2C transfers will use
  this address until it is changed by another ioctlSET\_I2C\_SLAVE\_ADDRESS request.

  **Parameter:** The slave address to set. For example, use 0x20 to write to address 0x20.
