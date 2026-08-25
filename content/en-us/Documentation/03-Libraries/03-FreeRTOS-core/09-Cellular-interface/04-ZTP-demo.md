---
title: Cellular Interface Demo (Zero Touch Provisioning)
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Introduction

1NCE is a global IoT Carrier that specializes in providing managed connectivity services for low 
bandwidth IoT applications. In this demo, the 1NCE service (a 1NCE sim card + AWS IoT device 
onboarding server) and a BG96 cellular module are used to demonstrate how to provision a device 
with zero-touch and to connect to AWS IoT core. Refer to 
the [1nce blueprint for FreeRTOS](https://github.com/1NCE-GmbH/blueprint-freertos).


## Download the source code

The source code can be downloaded from the FreeRTOS labs or by itself through Github.

To clone using HTTPS:

```c
git clone https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo.git --recurse-submodules
```

Using SSH:

```c
git clone git@github.com:FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo.git --recurse-submodules
```

If you have downloaded the repo without using the `--recurse-submodules` argument, you must run:

```c
git submodule update --init --recursive
```


## Source Code Organization

The demo project is called `1nce_bg96_zero_touch_provisioning_demo.sln` and can be found 
on [Github](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/tree/main/projects) in the 
following directory.

* [projects/1nce\_bg96\_zero\_touch\_provisioning\_demo](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/tree/master/projects/1nce_bg96_zero_touch_provisioning_demo)


```c
./Lab-Project-FreeRTOS-Cellular-Demo
├── lib
│   ├── backoff_algorithm ( submodule : backoffAlgorithm )
│   ├── cellular ( submodule : FreeRTOS-Cellular-Interface )
│   ├── coreMQTT ( submodule : coreMQTT )
│   ├── FreeRTOS ( submodule : FreeRTOS-Kernel )
│   └── ThirdParty
│       └── mbedtls ( submodule : mbedtls )
├── projects
│   ├──  sim70x0_mqtt_mutual_auth_demo ( demo project for SIMCOM sim7080/sim7090 )
│   └──  1nce_bg96_zero_touch_provisioning_demo ( demo project for 1nce zero touch provisioning with BG96 )
└── source
    ├── cellular
    │   └── ( code for adapting FreeRTOS Cellular Library with this demo )
    ├── coreMQTT
    │   └── ( code for adapting coreMQTT with this demo )
    ├── FreeRTOS
    │   └── ( code for adapting FreeRTOS with this demo )
    ├── mbedtls
    │   └── ( code for adapting mbedtls with this demo )
    ├── main.c
    ├── cellular_setup.c
    ├── MutualAuthMQTTExample.c
    ├── demo_config.h
    ├── logging_levels.h
    ├── logging_stack.h
    ├── 1nce_zero_touch_provisioning.h
    └── 1nce_zero_touch_provisioning.c
```


## Configure the Application Settings

### Configure the cellular network

The following parameters in the cellular 
configuration, [cellular\_config.h](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/cellular_config.h), 
must be modified for your network environment.

| Configuration | Description | Value |
| --- | --- | --- |
| CELLULAR\_COMM\_INTERFACE\_PORT | Cellular communication interface make use of COM port on computer to communicate with cellular module on windows simulator. | Your COM port connected to cellular module |
| CELLULAR\_APN | Default APN for network registration. | Specify the value according to your network operator. |
| CELLULAR\_PDN\_CONTEXT\_ID | PDN context id for cellular network. | Default value is CELLULAR\_PDN\_CONTEXT\_ID\_MIN. |
| CELLULAR\_PDN\_CONNECT\_TIMEOUT | PDN connect timeout for network registration. | Default value is 100000 milliseconds. |


### Configure the MQTT broker

The configuration for connecting to a MQTT broker can be found 
in ["source/demo\_config.h"](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/demo_config.h). 
Refer to the [documentation](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication#configuring-the-mqtt-broker-connection) for more information 
about the settings.


### Configure the COM port settings

Reference the cellular module documentation for COM port settings. Update 
the [comm\_if\_windows.c](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/source/cellular/comm_if_windows.c) 
if necessary.


### Configure the other sub-modules

["source/FreeRTOS/FreeRTOSConfig.h"](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/FreeRTOSConfig.h), 
 ["source/mbedtls/mbedtls\_config.h"](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/mbedtls_config.h) 
and ["source/coreMQTT/core\_mqtt\_config.h"](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/core_mqtt_config.h) 
are configurations for the corresponding sub-modules.


## Build and run the 1nce zero-touch-provisioning demo

1. In Visual Studio, open 
   the [1nce\_bg96\_zero\_touch\_provisioning\_demo.sln](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/tree/main/projects/1nce_bg96_zero_touch_provisioning_demo) 
   project. In this Visual Studio solution file, the macro `USE_1NCE_ZERO_TOUCH_PROVISIONING` is defined. 
   Please look for `#ifdef USE_1NCE_ZERO_TOUCH_PROVISIONING` in the source files to see the difference in 
   how a device using the 1nce service is provisioned. Otherwise, this demo performs the same mutually 
   authenticated MQTT operations as the other demos.

2. [Generate a self-signed certificate and its private key locally](https://docs.aws.amazon.com/iot/latest/developerguide/create-device-cert.html). 
   Update ["source/demo\_config.h"](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/demo_config.h) 
   with the certificate and private key. These are used to establish a TLS connection to the 1nce server. 
   Note that the keys are placed in a header file for demonstration purposes only; production devices should 
   use secure storage to store the keys.

3. Get the Access Point Name (APN) for your SIM card from 1NCE. Update `CELLULAR_APN` in the 
   file ["cellular\_config.h"](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-Cellular-Demo/blob/main/projects/1nce_bg96_zero_touch_provisioning_demo/cellular_config.h) 
   for BG96, and follow the steps in "Configure the Application Settings" above to finish the rest of 
   the configuration.

4. Compile and run.
