---
title: Using format methods to validate OTA protocol
created: 2020-12-14
feature: blog
categories:
  - Long term support
authors: 
  - talupur
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Murali Talupur](../author/talupur) on 14 Dec 2020

AWS FreeRTOS is a real-time operating system designed to run on IoT devices to enable them to interact 
easily and reliably with AWS services. The **Over the Air (OTA)** update functionality makes it possible 
to update a device with security fixes quickly and reliably. The [OTA Library](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates), a part 
of the overall OTA functionality that runs on the IoT devices, enables customers to learn of available 
updates, download the updates, check their cryptographic signatures, and apply them.


## OTA system architecture

The figure below shows a slightly simplified end-to-end architecture of the OTA system. On the AWS side 
we have a Job server that tracks the states of IoT devices in the field. That is, it tracks whether a 
device is active, what version of vendor software it is running, whether it needs an update, and so 
on. We also have File servers, which are AWS S3 buckets, that hold updates to send to devices. On the 
IoT device side we have the OTA Library that tracks the device state, handles incoming requests from 
the Job server, manages transfer of data from the File servers to the devices, applies the update and 
reports back to the Job server. The OTA App is the developer’s application code and the OTA PAL is the 
interface between the OTA Library and device-specific hardware. Communication among the devices and 
servers happens over MQTT and/or HTTP networks. 

![](/media/2020/Figure-1-4.png)  

The OTA system is a complex piece of software that performs firmware updates reliably and securely -- 
keeping all devices in a consistent state -- in the presence of arbitrary failures of devices and 
communication. The heart of the OTA system is an intricate distributed protocol, the OTA protocol, that 
co-ordinates the execution of the different agents involved. 


## OTA protocol validation

Apart from unit tests for individual agents like *Job server* or *OTA Library*, we have written extensive 
end to end tests for the whole system. Unlike a sequential system where we more or less know the flow 
of control through the code, a distributed system has multiple asynchronously executing agents -- like 
hardware device, network, AWS services, and so on for the OTA system -- leading to scenarios which are 
unanticipated. In fact, there are so many possible interleavings of individual agents’ executions that 
it is almost impossible to think through all of them.

This is a well-known problem in validating distributed systems and at AWS we have been using formal 
methods, in particular model checking, to raise the quality bar on distributed systems. As early as 
2011, several distributed protocols at AWS were subjected to model checking [1].

Given the centrality of OTA protocol to FreeRTOS, to achieve higher code quality than is possible with 
standard testing, we decided to use formal methods to validate the OTA protocol. In particular, we used 
model checking to thoroughly explore a model of the OTA protocol and uncover tricky corner-case scenarios.


## Model checking

Formal methods make use of mathematical logic and search techniques to reason about program correctness. 
Model checking is a notable technique in this area that, starting from a program description and a correctness 
property, exhaustively explores all the possible behaviors of the program, checking along the way if 
each such behavior satisfies the property. Any violation is reported back to the user along with a trace 
leading to the failure, thus giving the user precise and actionable feedback. As systems that have been 
model checked tend to be of higher quality and have significantly fewer bugs, it is used in both hardware 
industry and software industry for verifying critical designs [2][3]. 

Typically, distributed systems tend to be too large to verify directly using model checking. The standard 
practice is to create a model of the system that captures the core behavior of system and analyze that 
for protocol level errors. This approach has been successfully used both in hardware and software industry 
in designing intricate distributed systems [1][5]. Several model checkers --- including TLA+, SPIN, 
P --- have proven suitable for this task. We used P [4].


## OTA protocol modeling

The first step was to extract from the implementation a model of the protocol that is small enough to 
be amenable to formal analysis and rich enough to exhibit behaviors that mirror real scenarios. Our goal 
was to capture the core protocol in detail and analyze precisely those aspects of the OTA system that 
are hardest to test.

To this end we retained the protocol-specific details, such as the types of the messages the agents 
send and the protocol state machines of the various agents, and abstracted away all details not relevant 
to the core protocol. The level of detail in a distributed system can be gauged by the amount detail 
that messages carry. As an indication of the difference in detail, the actual job documents that are 
sent by the Job server to OTA Library is an UTF-8 encoded JSON containing about 20 fields. In our model, 
we simplified the job information to contain only 4 simplified fields, namely job id, job status, update 
version, and flag indicating http use, as shown below:

```c
enum JobStatus {  
  EMPTY = 0,  
  PENDING = 1,  
  INPROGRESS = 2,  
  SELFTEST = 3  
}  
```

```c
type job = (  
  id: int,   
  status: JobStatus,   
  version: int,   
  http: bool  
);  
```

## OTA protocol model checking

Once this was done, we used a model checker to generate thousands of scenarios to explore the OTA protocol 
model. The model checker generated these scenarios by scheduling system events in combinatorially interesting 
ways to stress the system. During this process we found 3 bugs in the model that pointed to potential 
issues in the actual implementation itself. 

To give an idea of the thoroughness with which the model checker explores, one of the bugs it found 
was as follows. In the normal course of operation OTA PAL tests the update received from Job Server 
and if it passes integrity check conveys that to the OTA Library, which in turns sends a notification 
across the network to Job server. Our model checker found a tricky corner case scenario where OTA Library 
gets disconnected before it can send the message back to Job server. Once the OTA Library comes back 
online, Job server instructs it to test the update again, not knowing that the test was already done. 
OTA Library conveys this to OTA PAL which by this time has moved onto a different state where it is 
not expecting a message to start the test. This leads the OTA PAL to hang, taking the whole OTA system down.

Thanks to our modeling effort, we discovered this subtle bug before ever running the code on real hardware, 
where root causing such bugs takes far more time and effort. Not only could we fix it before release, 
but because model checking produced a scenario eliciting this bug, we could add an integration test to 
the regression to make sure this scenario is always tracked. In this way, using findings produced by 
model checking, we hardened the code by fixing issues found, adding tests to integration suites, and 
adding assumptions to the code.


## Conclusion

By extracting from the OTA implementation a model of the OTA protocol, and by using a model checker 
to explore the OTA protocol model more extensively than is possible with the implementation itself, 
we have demonstrated the architectural integrity of the OTA implementation. This, together with extensive 
system-level testing of the OTA implementation using methods standard in the industry, delivers to the 
customer a high level of confidence in the quality of the protocol and the implementation being released. 


## References

1. How Amazon Web Services Uses Formal Methods. By Chris Newcombe et al in Communications of the ACM, 
   Vol 58, No.4, April 2015
2. Formal verification in a commercial setting. By Robert Kurshan. In Proceedings of the 34th annual 
   Design Automation Conference (DAC) 1997
3. Model Checking Boot Code from AWS Data Centers. By Byron Cook et al in Proceedings of 30th International 
   Conference on Computer Aided Verification (CAV) 2018
4. P: Safe Asynchronous Event-Driven Programming. By Ankush Desai et al in Proceedings of ACM SIGPLAN 
   Conference on Programming Language Design and Implementation (PLDI), 2013
5. Protocol verification using Flows: An industrial experience report. By John O’Leary et al. in Proceedings 
   of Conference of Formal Methods in Computer Aided Design (FMCAD) 2009


## Contributing Authors:

* Muralidhar Talupur (Principal Scientist, Applied, Automated Reasoning Group)
* Huaixi Lu (AWS, Applied Scientist Intern, Automated Reasoning Group)
* Mark R Tuttle (Principal, Applied Scientist, Automated Reasoning Group)


## About the author

![](https://secure.gravatar.com/avatar/a02800d22dad3240a5ff2c23ac24fa4a?s=200&d=mm&r=g)   
Murali Talupur is a Principal Applied Scientist with the Automated Reasoning Group at Amazon Web 
Services (AWS). His work focuses on formal verification of distributed systems and critical software libraries.   
[View articles by this author](../author/talupur) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
