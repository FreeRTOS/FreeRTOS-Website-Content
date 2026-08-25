---
title: AWS IoT Jobs Library Demo
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Introduction

The AWS IoT Jobs Library Demo shows you how to connect to
the [AWS IoT Jobs service](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) through
an MQTT connection, retrieve a [job](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/02-Jobs-terminology) from AWS IoT, and process it on a device. The
AWS IoT Jobs Demo project uses
the [FreeRTOS Windows port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW),
so it can be built and evaluated with
the [free Community version of Visual Studio](https://visualstudio.microsoft.com/vs/community/) on Windows.
No microcontroller hardware is needed. The demo establishes a secure connection to the AWS IoT MQTT broker
using TLS in the same manner as the [MQTT mutual authentication demo](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication).


## Source Code Organization

The demo project is called `jobs_demo.sln` and can be found in
the [FreeRTOS-Plus Jobs\_Demo](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/AWS/Jobs_Windows_Simulator/Jobs_Demo)
repository on GitHub in the following directory:

```c
FreeRTOS-Plus\Demo\AWS\Jobs_Windows_Simulator\Jobs_Demo
```

## Configure the Demo Project

The demo uses the [FreeRTOS-Plus-TCP TCP/IP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), so follow
the instructions provided for the [TCP/IP starter project](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)
to:

1. [Install the pre-requisite components](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#prerequisites)
   (such as WinPCap).

2. Optionally [set a static or dynamic IP address, gateway address and netmask](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#static-dynamic).

3. Optionally [set a MAC address](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#mac-addr).

4. [Select an Ethernet network interface](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator#network-interface)
   on your host machine.

The above settings should be changed in the Jobs demo project.


### Configure the AWS IoT MQTT Broker Connection

In this demo you use an MQTT connection to the AWS IoT MQTT broker. This connection is configured in the same
way as in the [MQTT mutual authentication demo](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection).


## Build the Demo Project

The demo project uses the [free community edition of Visual Studio](https://visualstudio.microsoft.com/vs/community/).
To build the demo:

1. Open the Visual Studio solution file `FreeRTOS-Plus/Demo/AWS/Jobs_Windows_Simulator/Jobs_Demo/jobs_demo.sln`
   from within the Visual Studio IDE.

2. Select **build solution** from the IDE's **build** menu.


## Functionality

The demo shows the workflow used to receive jobs from AWS IoT and process them on a device. The demo
is interactive and requires you to create jobs using either the AWS IoT console or the AWS CLI.
See [create-job](https://docs.aws.amazon.com/cli/latest/reference/iot/create-job.html) in the *AWS CLI
Command Reference* for more information about creating a job. The demo requires the job document to
have an "action" key set to "print" to print a message to the console. The format for this job document
is as follows:

```c
{
    "action": "print",
    "message": "INSERT_MESSAGE_HERE"
}
```

Using the AWS CLI, a job can be created as follows (command prompt):

```c
aws iot create-job \
    --job-id t12 \
    --targets arn:aws:iot:us-east-1:1234567890:thing/device1 \
    --document '{"action":"print","message":"hello world!"}'
```

The arguments used above are examples only.

The demo also uses a job document that has the "action" key set to "publish"
to republish the message to a topic. The format for the job document is as follows:

```c
{
    "action": "publish",
    "message": "INSERT_MESSAGE_HERE",
    "topic": "topic/name/here"
}
```
The demo loops until it receives a job document with the "action" key set to "exit" to exit the demo.
The format for the job document is as follows:

```c
{
    "action: "exit"
}
```


### Entry point of the Jobs Demo

The source code for the Jobs demo entry point function can be found
in [JobsDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/AWS/Jobs_Windows_Simulator/Jobs_Demo/DemoTasks/JobsDemoExample.c#L741-L935)
on GitHub. This function performs the following operations:

1. Establish an MQTT connection using the helper functions in `mqtt_demo_helpers.c`.

2. Subscribe to the MQTT topic for the `NextJobExecutionChanged` API, using helper functions in `mqtt_demo_helpers.c`.
   (The topic string is assembled earlier, using macros defined by the Jobs library.)

3. Publish to the MQTT topic for the `StartNextPendingJobExecution` API, using helper functions in `mqtt_demo_helpers.c`.
   (The topic string is assembled earlier, using macros defined by the Jobs library.)

4. Repeatedly call `MQTT_ProcessLoop` to receive incoming messages which are handed to `prvEventCallback`
   for processing.

5. After the demo receives the exit action, unsubscribe from the MQTT topic and disconnect, using the helper
   functions in `mqtt_demo_helpers.c`.


### Callback for Received MQTT messages

This function calls `Jobs_MatchTopic` from the Jobs library to classify the incoming MQTT message.
If the message type corresponds to a new job, `prvNextJobHandler` is called.

The function `prvNextJobHandler`, and the functions it calls, parse the job document from the
JSON-formatted message, and execute the action specified by the job. Of particular interest is the
function `prvSendUpdateForJob`.

The source code for this callback function for incoming messages can be found
in [JobsDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/AWS/Jobs_Windows_Simulator/Jobs_Demo/DemoTasks/JobsDemoExample.c#L622-L718)
on GitHub.


### Send an Update for a Running Job

The function `prvSendUpdateForJob` calls `Jobs_Update` from the Jobs library to populate the topic string
used in the MQTT publish operation that immediately follows.

The source code for the `prvSendUpdateForJob` function can be found
in [JobsDemoExample.c](https://github.com/FreeRTOS/FreeRTOS/blob/202012.00/FreeRTOS-Plus/Demo/AWS/Jobs_Windows_Simulator/Jobs_Demo/DemoTasks/JobsDemoExample.c#L400-L445)
on GitHub.
