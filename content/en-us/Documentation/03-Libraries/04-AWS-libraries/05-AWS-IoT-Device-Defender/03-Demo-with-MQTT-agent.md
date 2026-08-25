---
title: Integrating the Device Defender Library with the MQTT Agent
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

* On this Page
  + [Introduction](#introduction)
  + [Instructions](#instructions)
    - [Getting Started](#getting-started)
    - [Creating Custom Metrics using AWS IoT Console](#creating-custom-metrics-using-the-aws-iot-console)
    - [Configuring a Security Profile](#configuring-a-security-profile)
    - [Configuring and running the demo](#configuring-and-running-the-demo)
    - [Viewing the metrics on the AWS IoT Console](#viewing-the-metrics-on-the-aws-iot-console)


## Introduction

This example uses the [MQTT agent](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo) to interact with 
the [AWS IoT Device Defender service](https://docs.aws.amazon.com/iot/latest/developerguide/device-defender.html) 
by submitting device defender reports, 
including [custom metrics](https://docs.aws.amazon.com/iot/latest/developerguide/dd-detect-custom-metrics.html), 
and verifying that the reports were accepted. The MQTT agent enables the Defender reporting functionality 
to run in the background and share the MQTT connection with other tasks.

The Device Defender demo code runs as a task in 
the [same demo project](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/tree/main/build/VisualStudio) 
as the [MQTT agent demo](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)  and the [OTA demo](/Documentation/03-Libraries/07-Modular-over-the-air-updates/02-Demos/02-mqtt-ota-agent-orchestrator). 
Follow the directions on the [MQTT agent demo documentation page](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo#obtaining-the-source-code) 
in order to obtain and configure the project. To use the Device Defender demo task, configure your project 
to connect to [AWS IoT Core](https://docs.aws.amazon.com/iot/index.html), and then perform the additional 
project and AWS account configurations specified on this page.

See the comments at the top of each C file in 
the [Source Directory](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/tree/main/source) for 
additional information. 


## Instructions

### Getting Started

Start by setting up the project as described on the [MQTT agent demo documentation page](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo). 
Be sure to follow all of the steps starting with:

1. [Learning about the MQTT Agent demo](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo#demo-project)
2. [Obtaining the source code](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo#obtaining-the-source-code)
3. [Configuring FreeRTOS-Plus-TCP](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)
4. [Configuring the MQTT broker](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)
5. [Configuring the MQTT Agent](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo)

Follow the instructions to [connect using the AWS IoT Core MQTT broker](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/02-coreMQTT-agent-demo#configuring-the-mqtt-broker-connection) 
and test the connection using one of the simple MQTT tasks. This will ensure connectivity to AWS IoT 
Core is working correctly before moving on to enabling the Device Defender task.

Once connectivity is working with a non-Defender demo, the following instructions show you how to: 

* Set up the custom metrics on your AWS account.
* Configure a security profile to retain submitted reports.
* Enable and run the demo task.
* View the submitted metrics.


### Creating custom metrics using the AWS IoT console

As the demo submits [custom metrics](https://docs.aws.amazon.com/iot/latest/developerguide/dd-detect-custom-metrics.html), 
the first step is to configure these metrics on the AWS account. The demo uses two custom metrics, 
named "stack\_high\_water\_mark" (of type number) and "task\_numbers" (of type number list). Start 
by going to the [AWS IoT console](https://console.aws.amazon.com/iot/home). 

In the navigation pane of the AWS IoT console, choose **Defend**, **Detect**, and then **Metrics**.

[![](/media/2021/Custom-Metrics-1.jpg)](/media/2021/Custom-Metrics-1.jpg)   
**Click to enlarge.**

Click "Create" in the custom metrics section. Under "Name", enter "stack\_high\_water\_mark". 
Under "Type", select "number". Then click "Create custom metric".

[![](/media/2021/Custom-Metrics-2.png)](/media/2021/Custom-Metrics-2.png)   
**Click to enlarge.**

Repeat the prior step, except use "task\_numbers" for the name and "number-list" for the type. You should 
see both metrics as shown below.

[![](/media/2021/Custom-Metrics-3.png)](/media/2021/Custom-Metrics-3.png)   
**Click to enlarge.**


### Configuring a Security Profile

In order for submitted reports to be retained, a security profile needs to be configured. Start by 
going to the [AWS IoT console](https://console.aws.amazon.com/iot/home). In the navigation pane of 
the AWS IoT console, choose **Defend**, **Detect**, and then **Security Profiles**.

[![](/media/2021/Custom-Metrics-4.png)](/media/2021/Custom-Metrics-4.png)   
**Click to enlarge.**

Under "Create Security Profile", select "Create Rule-based anomaly Detect profile". Enter a name 
under "Name". Under the dot menu, click "Delete" to remove the default behavior.

[![](/media/2021/Custom-Metrics-5.png)](/media/2021/Custom-Metrics-5.png)   
**Click to enlarge.**

Expand the "Additional Metrics to retain" section, and click the first checkbox in order to select all 
the metrics. Click next. Then on the Alert targets page, just click "Next".

[![](/media/2021/Custom-Metrics-6.png)](/media/2021/Custom-Metrics-6.png)   
**Click to enlarge.**

On the Attach page, select "All things", and then click "Next". Click "Save" on the Confirm page.

[![](/media/2021/Custom-Metrics-8.png)](/media/2021/Custom-Metrics-8.png)   
**Click to enlarge.**


### Configuring and Running the Demo

In order to run this demo, you'll need to set up your connection to AWS IoT Core. Follow 
the [configuration steps here](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection), and once 
you've completed those, perform the following steps:

**NOTE:** Make sure 
that [democonfigCLIENT\_IDENTIFIER](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/configuration-files/demo_config.h#L100) 
was set to the name of your Thing.

* Enable the defender demo task by updating [democonfigCREATE\_DEFENDER\_DEMO](https://github.com/FreeRTOS/coreMQTT-Agent-Demos/blob/main/source/configuration-files/demo_config.h#L84) to 1.
* Run the demo and let it submit some reports. By default, it sends a report every 30 seconds.
* When a report is successful, the following message will be printed to the console:

```c
**The defender report was accepted by the service.**  
```


### Viewing the metrics on the AWS IoT Console

Once the demo has submitted reports, you can view them to verify they are working as intended. Start 
by going to the [AWS IoT console](https://console.aws.amazon.com/iot/home). 

In the navigation pane of the AWS IoT console, choose **Manage**, and then **Things**. 

Select the Thing created for the demo, and select the "Defender metrics" tab. Here you can select reported 
metrics, including custom metrics, and view reported values. Reports may take some time to show up.

[![](/media/2021/Custom-Metrics-9.png)](/media/2021/Custom-Metrics-9.png)   
**Click to enlarge.**
