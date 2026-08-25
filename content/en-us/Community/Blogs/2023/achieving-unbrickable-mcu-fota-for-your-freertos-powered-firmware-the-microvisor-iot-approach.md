---
title: "Achieving Unbrickable MCU FOTA for your FreeRTOS-powered Firmware: The Microvisor IoT Approach"
date: 18 May 2023
feature: blog
authors:
  - tony_smithtwilio-com
---
FreeRTOS brings a stack of functionality to embedded applications, enabling them to become much more flexible, and their developers to be more creative.
But there's a key requirement of Internet of Things (IoT) applications in particular that takes a lot of extra development work to put in place, to make it
truly secure, and to eliminate the risk of application crashes that cause devices to stop functioning: over-the-air (OTA) updates that can't brick devices.


Zapping a unit might not be a problem if the hardware is sitting on your desk in front of you, but it's a really big deal if your fleet is remote.
Happily there's a solution, and it's one that plays incredibly well with FreeRTOS:
[Twilio Microvisor](https://www.twilio.com/iot/microvisor-iot-platform).


The Microvisor-based approach to IoT connectivity
-------------------------------------------------


What is Microvisor? Think of it as a hypervisor for embedded systems, or a 'microvisor', with some additional functionality devised with IoT use-cases
in mind. Microvisor doesn't operate on top of FreeRTOS, but sits right alongside it, so there's no interference with how the OS or the hosted application
function. Equally, Microvisor doesn't depend upon FreeRTOS to function.


[![](/media/2023/microvisor-zone.png)](/media/2023/microvisor-zone.png)

Microvisor relies on [Arm's TrustZone technology](https://www.arm.com/technologies/trustzone-for-cortex-a)
to partition the host microcontroller — STMicroelectronics's STM32U585 MCU is the first microcontroller we support — into a 'secure', privileged kernel space and
a 'non-secure' user space. Microvisor runs in the former; your application in the latter. Non-secure sounds pejorative, but it just means that the application
cannot access resources in the TrustZone's secure world. This ensures Microvisor is free to manage critical system functionality and watch key attack surfaces:
the primary Internet connection, system clocks, interrupt management, and so on.


When activated, TrustZone only boots code in the secure world. In Microvisor's case, that's a pre-boot stub that verifies the installed Microvisor code's
X.509 credentials before starting it. Microvisor itself checks for locally staged application updates, verifying their signatures before installing them. Once
any updates have been installed, Microvisor configures the non-secure world and fires up the application.


By 'application' we mean FreeRTOS and a hosted app, of course. Both run together within the non-secure zone as if they were running on bare metal. Under
Microvisor, FreeRTOS requires no special configuration beyond what you might do for any given application and MCU combination. Write your ISRs and make use
of FreeRTOS tasks, semaphores, queues and notifications without change.


Microvisor maintains a primary connection to the Twilio Cloud via WiFi, cellular or Ethernet, or whichever of these connectivity types your product is fitted
with. You upload new versions of your application to the Twilio Cloud and then deploy it to one or more devices remotely. You can do this via the
[Twilio web console](https://console.twilio.com/), or our
[CLI tooling](https://www.twilio.com/docs/iot/microvisor/how-to-install-the-microvisor-sdk).


Let's say you've done just that and staged an update to your application. The Cloud signals the installed Microvisor on each target device. A given Microvisor
instance retrieves the update's manifest and uses it to download code and associated data in chunks called 'layers'. This way interruptions to communications,
if they occur, don't force Microvisor to reacquire the whole update on every error. Instead it assembles the update layer by layer. With the complete update
verified and then written to a staging area in Flash, Microvisor tears down the non-secure world, installs the new application and starts it.


Microvisor's TrustZone-secured environment ensures that application crashes don't bring it down too. In fact, it actually monitors application state so that
crashes can be tracked, a stack trace saved for future reporting, and the application restarted. This makes firmware OTA updates essentially 'unbrickable'. The
application may continue to die every time it's restarted — until you deploy the fix, of course — but Microvisor remains operational, connected and accessible.


This functionality comes 'for free' — there's nothing the application need do to activate it. Microvisor is always protecting your device.


Developing and debugging your application with Microvisor
---------------------------------------------------------


So how do you develop your application for use in a Microvisor-managed environment? The simple answer is that you don't need to do very much at all. Your
application can run without having to be coded in any special way. An existing application ported to Microvisor will need a little tweaking, primarily around
clock configuration, as Microvisor does this for you. However, new applications can focus entirely on the business logic.


Every application running alongside Microvisor has complete access to all of the host device's hardware resources with the exception of the device's primary
cloud-facing network interfaces and a handful of microcontroller peripherals which Microvisor requires for system-level functionality. If you wish to use other
interfaces, such as other wireless technologies, you can, but your application needs to incorporate drivers and security provisions. If all you need to do is
reach your own servers, you just use the Microvisor-maintained link as a tunnel to host your own HTTP and/or MQTT requests, for which Microvisor provides an API,
as we'll see.


Access to the MCU's GPIO and peripherals is shared by both Microvisor and the application, but a small number of GPIO registers are reserved by Microvisor.
Any attempts by the application to access these resources will result in an exception so you can discover conflicts during development and remedy them. You can
view a list of the STM32U585 peripherals and pins reserved by Microvisor in the
[Microvisor hardware design guide](https://www.twilio.com/docs/iot/microvisor/design-iot-devices-with-microvisor#stm32u585-reserved-peripherals).


The application may use any other peripheral, and on the STM32U585 there are plenty. It can access these resources at the memory locations detailed in the
[STM32U585 datasheet](https://www.st.com/resource/en/datasheet/stm32u585ai.pdf), or by calling convenience
functions provided by a hardware abstraction layer (HAL) library.


MCU storage and memory are partitioned too. The STM32U585 contains 2MB of internal flash. Microvisor takes the upper 1MB and assigns the remaining 1MB to
the application, mapped it to the non-secure world address range 0x08000000-080FFFFF, so the application has access to the same flash addresses, minus the
top 1MB, that it would expect if it were running on an ordinary STM32U5.


Microvisor owns the MCU's BKPSRAM (2KB) and the top half (256KB) of SRAM3. The lower 256KB of SRAM3, and all of the remaining SRAM banks SRAM1 (272KB in total),
is available to the application, 528KB in all.


What this means is that the application has plenty of memory, storage, interrupts, and a wide array of peripherals to use. Depending on the nature of your
application, you may be content to work with these resources and ignore Microvisor: you can allow it to focus on application updates and remote debugging in the
background. Yes, Microvisor enables a channel for GDB debug sessions — with full code stepping; variable inspection and setting; backtracing; breakpoints; and
register peeking. Our CLI tooling includes a custom local GDB server to relay messaging to the device via the Twilio Cloud.


Interacting with Microvisor through System Calls
------------------------------------------------


More likely, however, you will want to interact with Microvisor. You do so by working with its [System Calls](https://www.twilio.com/docs/iot/microvisor/syscalls) and [notification mechanism](https://www.twilio.com/docs/iot/microvisor/microvisor-notifications). System calls allow your application to ask Microvisor to perform certain operations on your behalf:


* [Network management](https://www.twilio.com/docs/iot/microvisor/syscalls/network).
* [HTTP](https://www.twilio.com/docs/iot/microvisor/syscalls/http) and
 [MQTT](https://www.twilio.com/docs/iot/microvisor/syscalls/mqtt) communications.
* [Notification setup](https://www.twilio.com/docs/iot/microvisor/syscalls/notifications).
* [Low-latency interrupt configuration](https://www.twilio.com/docs/iot/microvisor/syscalls/interrupts).
* [Time checking](https://www.twilio.com/docs/iot/microvisor/syscalls/time).
* [Device management](https://www.twilio.com/docs/iot/microvisor/syscalls/device).
* [Application logging](https://www.twilio.com/docs/iot/microvisor/syscalls/application-logging).


[![](/media/2023/microvisor-notifications.png)](/media/2023/microvisor-notifications.png)

Click to enlarge


All system calls return a status code indicating whether the request was accepted or rejected (and why). Data is returned to the application by writing
it to a memory location or a buffer provided by the application. In the case of highly asynchronous operations, such as HTTP requests, which are relayed via
the Twilio Cloud, your application is notified when returned data is available.


The notification system binds operations to notification buffers sized and provided by the application. Notifications are of a fixed size (16 bytes)
and are appended to the buffer at the write pointer; the buffer is circular. Then an interrupt is raised. The application's notifications ISR can parse
the latest message and act accordingly.


For example, to issue an HTTP request you must call:


```c
enum MvStatus status = mvSendHttpRequest(http_channel_handle, &request_config);
```

`http_channel_handle` is a 32-bit unsigned integer that identifies a previously established HTTP data transfer channel; the application will
also have set up a network 'connection' (think of it as permission to leverage Microvisor's primary Internet link) to host the channel. `request_config`
is a [Microvisor-defined structure](https://www.twilio.com/docs/iot/microvisor/syscalls/http#mvsendhttprequest)
that specifies the HTTP request you wish to make.


The value of status will be zero (`MV_STATUS_OKAY`) if Microvisor accepts the request. Any other value indicates an error: for instance, pointers
included in the request configuration are invalid, or the supplied handle references an MQTT channel, or the channel has already been closed.


Even success at this stage doesn't mean the request was issued and a response received. An incorrect request URL can't be identified until the request is
relayed to the Twilio Cloud and the request issued. Such failures are reported to Microvisor which informs the application through a notification center already
set up and bound to the HTTP data channel being used. The receipt of responses from the target server are signaled the same way.


Incidentally, the device-cloud connection is fully managed and secured with TLS 1.2. It's regularly pentested. This channel, maintained by Microvisor, is
used for OTA updates, HTTP and MQTT communications, application logging and remote debugging.


When your application creates notification centers, it assigns them an interrupt; this is triggered when Microvisor has written a new notification. The
ISR determines if the current notification's type is `MV_EVENTTYPE_CHANNELDATAREADABLE` and sets a flag, `received_request`:


```c
void TIM8_BRK_IRQHandler(void) {
    // Check for a suitable event -- readable data in the channel – by
    // reading in the latest notification
    bool got_notification = false;

    volatile struct MvNotification notification = http_notification_center[current_notification_index];

    if (notification.event_type == MV_EVENTTYPE_CHANNELDATAREADABLE) {
        // Flag we need to access received data and to close the HTTP channel

        // when we're back in the main loop. This lets us exit the ISR quickly.

        // We should not make Microvisor System Calls in the ISR.
        received_request = true;
        got_notification = true;
    }

    if (notification.event_type == MV_EVENTTYPE_CHANNELNOTCONNECTED) {

        // The HTTP channel signaled its unexpected closure
        channel_was_closed = true;
        got_notification = true;
    }

    if (got_notification) {
        // Point to the next record to be written

        current_notification_index = (current_notification_index + 1) % HTTP_NT_BUFFER_SIZE_R;
        // Clear the current notifications event
        // See https://www.twilio.com/docs/iot/microvisor/microvisor-notifications#buffer-overruns
        notification.event_type = 0;
    }

}
```

The FreeRTOS work task checks the flag and, if it's set, requests the response data from Microvisor using another system call. The application provides
a buffer into which the response will be written and the channel ID:


```c
status = mvReadHttpResponseData(http_channel_handle, &response_buffer);
```

The call will fail if `&response_buffer` is invalid, the handle is bad (`NULL` or the wrong type), or the response is too large for
the buffer. If the response is written, it's in the form of a defined structure from which your application can access response metadata: the HTTP status code,
the number of headers included, and so on. Separate Microvisor system calls allow you to get the response body itself and header values.


The Microvisor SDK provides the system call bindings, a Microvisor-specific version of ST's STM32U585 HAL, and a custom linker script to handle the setting
of the text, initialized data, and uninitialized data sector addresses.


How to start working with Twilio Microvisor and FreeRTOS
--------------------------------------------------------


**To learn more about Twilio Microvisor and get access to our dev boards, visit [www.microvisor.com](https://www.twilio.com/iot/microvisor-iot-platform).**


To understand how Microvisor and a FreeRTOS-based application work together, [we've put together a demo](https://github.com/twilio/twilio-microvisor-freertos). It's a classic 'Hello, World' application that establishes a couple of FreeRTOS
tasks: one to periodically flash a connected LED, the other to perform some basic logging work.


The demo pulls in FreeRTOS as a git submodule and includes a ready rolled `FreeRTOSConfig.h` file. The Microvisor SDK and HAL are pulled in
the same way. The key file to observe is `main.c` which sets up the FreeRTOS tasks and starts the scheduler. State messages are emitted via
Microvisor's application logging system calls. It's ready to be used as the basis for your own Microvisor-hosted application.


Further [Microvisor sample applications](https://www.twilio.com/docs/iot/microvisor/sample-code)
demonstrate working with HTTP and MQTT requests, and interacting with connected devices, including displays and sensors.
