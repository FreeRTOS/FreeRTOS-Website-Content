---
title: AWS IoT Device Shadow Operations Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### Introduction

This demo shows how to use the AWS IoT Device Shadow library to connect to the AWS Device Shadow Service.
It uses the [coreMQTT library](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) to establish an MQTT connection with TLS (Mutual Authentication)
to the AWS IoT MQTT Broker and the [coreJSON parser](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) to parse shadow documents it receives
from the AWS Shadow service. The demo showcases some basic shadow operations, such as how to update a shadow
document and how to delete a shadow document. The demo also shows how to register a callback function with
the MQTT library to handle messages like the shadow `/update`
and `/update/delta` messages that are sent from the AWS Device Shadow service.

This demo is intended only as a learning exercise because the request to update the shadow document (state)
and the update response are done by the same application. In a realistic production scenario, an external
application (e.g. an application running on a user's phone) would request an update of the state of the device
remotely, even if the device is not currently connected. The device will acknowledge the update request
when it is connected.

This demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so you can build and evaluate it with
the [free Community version of Visual Studio](https://visualstudio.microsoft.com/vs/community/) on
Windows without the need for any MCU hardware.


### Source Code Organization

The demo project is called `shadow_device_operations_demo.sln` and can be found in
the [FreeRTOS](https://github.com/FreeRTOS/FreeRTOS) repository on GitHub in the following directory:

```c
FreeRTOS-Plus\Demo\AWS\Device_Shadow_Windows_Simulator\Device_Shadow_Demo
```


### Configure the Demo Project

The demo uses the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), so
follow the instructions provided for
the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator) to:

1. [Install the pre-requisite components](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)
   (such as WinPCap).

2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)
   on your host machine.

5. **(Important!)** [Test your network connection](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#connectivity-test)
   before you attempt to run the Shadow demo.

All of these settings should be set in the Shadow demo project.


### Configure the AWS IoT MQTT Broker Connection

In this demo you use an MQTT connection to the AWS IoT MQTT broker. This connection is configured in
the same way as the [MQTT mutual authentication demo](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication).


### Build the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).
To build the demo:

1. Open the Visual Studio solution
   file `FreeRTOS-Plus\Demo\AWS\Device_Shadow_Windows_Simulator\Device_Shadow_Demo\shadow_main_demo.sln`
   from within the Visual Studio IDE.

2. Select '**build solution**' from the IDE's '**build**' menu.


### Functionality

The demo creates a single application task that loops through a set of examples that demonstrate
shadow `/update` and `/update/delta` callbacks to simulate toggling a remote IoT device's state. It sends
a shadow update with the new `desired` state and waits for the IoT device to change its `reported` state
in response to the new `desired` state. In addition, a shadow `/update` callback is used to print the
changing shadow states. This demo also uses a secure MQTT connection to the AWS IoT MQTT Broker, and
assumes there is a `powerOn` state in the device shadow. By default, the demo uses the classic unnamed
shadow. Optionally `democonfigSHADOW_NAME` can be defined to select a named shadow.

The demo performs the following operations:

1. Establish a MQTT connection by using the helper functions in `shadow_demo_helpers.c`.

2. Assemble MQTT topic strings for IoT device shadow operations, using macros defined by the Device
   Shadow library.

3. Publish to the MQTT topic used for deleting a device shadow to delete any existing device shadow.

4. Subscribe to the MQTT topics for `/update/delta`, `/update/accepted` and `/update/rejected` using
   helper functions in `shadow_demo_helpers.c`.

5. Publish a desired state of `powerOn` using helper functions in `shadow_demo_helpers.c`. This will cause
   an `/update/delta` message to be sent to the device.

6. Handle incoming MQTT messages in `prvEventCallback`, and determine whether the message is related
   to the device shadow by using a function defined by the Device Shadow library (`Shadow_MatchTopicString`).
   If the message is a device shadow `/update/delta` message, then the main demo function will publish a
   second message to update the reported state to `powerOn` . If an `/update/accepted` message is received,
   verify that it has the same clientToken as previously published in the update message. That will mark the
   end of the demo.

The structure of the demo can be found
in [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L811-L1128)
on GitHub.

This screenshot shows the expected output when the demo executes correctly:

[![](/media/2020/Shadow-Demo-Sucess.png)](/media/2020/Shadow-Demo-Sucess.png)
*Click to enlarge*


#### *Connect to the AWS IoT MQTT Broker*

To connect to the AWS IoT MQTT broker, we use the same method as `MQTTConnect()` in
the [MQTT mutual authentication demo](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication).


#### *Delete the Shadow Document*

To delete the shadow document, call `xPublishToTopic` with an empty message, using macros defined by
the Device Shadow library. This uses `MQTT_Publish` to publish to the `/delete` topic. An example showing
how this is done in the `prvShadowDemoTask` can be found
in [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L871-L877)
on GitHub.


#### *Subscribe to Shadow Topics*

Subscribe to the Device Shadow topics to receive notifications from the AWS IoT broker about shadow
changes. The Device Shadow topics are assembled by macros defined in the Device Shadow library. An
example showing how this is done in the `prvShadowDemoTask` function can be found
in [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L918-L937)
on GitHub.


#### *Send Shadow Updates*

To send a shadow update, the demo calls `xPublishToTopic` with a message in JSON format, using macros
defined by the Device Shadow library. This uses `MQTT_Publish` to publish to the `/delete` topic. An
example showing how this is done in the `prvShadowDemoTask` function can be found
in [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L1019-L1029)
on GitHub.


#### *Handle Shadow Delta Messages and Shadow Update Messages*

The user callback function, that was registered to the [coreMQTT Client library](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)
using the function [`MQTT_Init()`](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#mqttinit), will notify
us about an incoming packet event. The code for an example callback function can be found
in [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L687-L768)
on GitHub.

The callback function confirms the incoming packet is of type `MQTT_PACKET_TYPE_PUBLISH`, and uses
the Device Shadow Library API `Shadow_MatchTopic` to confirm that the incoming message is a shadow message.

If the incoming message is a shadow message with type `ShadowMessageTypeUpdateDelta`, then we
call `prvUpdateDeltaHandler` to handle this message. The handler `prvUpdateDeltaHandler` uses
the [coreJSON library](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) to parse the message to get the delta value for the `powerOn`
state and compares this against the current device state maintained locally. If these are different,
the local device state is updated to reflect the new value of the `powerOn` state from the shadow
document. The code for `prvUpdateDeltaHandler` can be found
in [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L475-L591)
on GitHub.

If the incoming message is a shadow message with type `ShadowMessageTypeUpdateAccepted`, then we
call `prvUpdateAcceptedHandler` to handle this message. The handler `prvUpdateAcceptedHandler`
parses the message using the [coreJSON library](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) to get the `clientToken` from the
message. This handler function checks that the client token from the JSON message matches the client
token used by the application. If it doesn't match, the function logs a warning message. The code
for `prvUpdateAcceptedHandler` can be found
in [ShadowDemoMainExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/AWS/Device_Shadow_Windows_Simulator/Device_Shadow_Demo/DemoTasks/ShadowDemoMainExample.c#L595-L678)
on GitHub.
