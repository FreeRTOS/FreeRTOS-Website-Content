---
title: coreSNTP Library Terminology
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**Polling Interval**   
An SNTP client can periodically synchronize the system time with a time server to ensure that the system 
clock does not drift beyond the threshold tolerated by the application. The time interval between consecutive 
synchronization attempts with the time server is called the polling interval.


**Clock Offset**   
When the coreSNTP library receives a server response, the library calculates how much the system time has drifted 
from the server time. This calculated value is called the clock offset, and it can be a positive value (when the 
system has drifted behind the server time) OR a negative value (when the system has drifted ahead of the server
time). The clock-offset value is calculated by the coreSNTP library when it receives a server response from the 
network. This value is used to correct for the time delay that occurred in sending and receiving SNTP packets 
on the network. 

The library uses the following mathematical formula for calculating the clock offset:

```c
                T2      T3
     ---------------------------------   <-----   *SNTP/NTP server*
              /\         \
              /           \
    Request* /             \ *Response*
            /              \/
     ---------------------------------   <-----   *SNTP client*
          T1                T4
```
 
The four most recent timestamps, T1 through T4, are used to compute
the clock offset of the SNTP client relative to the server where:

``` 
    T1 = Client Request Transmit Time
    T2 = Server Receive Time (of client request)
    T3 = Server Response Transmit Time
    T4 = Client Receive Time (of server response)
 
 Clock Offset = T(NTP/SNTP server) - T(SNTP client)
              = [( T2 - T1 ) + ( T3 - T4 )]
                ---------------------------
                             2
```


**Kiss-o'-Death Packet**   
When an SNTP/NTP server rejects a time request from an SNTP/NTP client, the rejection response it sends 
is called a "Kiss-o'-Death" packet. The server MAY send a 4 letter "kiss-code" in the response packet 
that gives the reason for the rejection. The **serializer/de-serializer** API of the coreSNTP library 
provides the application with the "kiss-code" it has parsed from an SNTP server rejection response packet. 
The **client** API layer generally handles these server rejection responses by avoiding re-use of that 
server and rotating to the next server you have configured in the library's list of servers. Therefore, 
we recommend that you configure more than one time server in your application for resiliency; a back-up 
server will be used in case the primary server experiences unexpected service downtimes. 


**NTP Era and NTP Era Epoch**   
An NTP era comprises the number of seconds that can be represented with an unsigned 32 bit integer (~136 years). 
The limit of 32 bits for an NTP era is due to the 32 bit width of the "seconds" portion of an NTP timestamp. 
The NTP era epoch is the starting or base time for the era. For example, the NTP era 0 represents times from 
the 1st of January 1900 0h:0m:0s to the 7th of February 2036 6h:14m:27s. The 1st of January 1900 0h:0m:0s is 
the epoch time for NTP era 0. 

The following table of NTP eras is taken from the NTPv4 specification. The coreSNTP library provides support for 
timestamps within the eras of NTP 0 and NTP 1.

```c
   +-------------+------------+-----+---------------+------------------+
   | Date        | MJD        | NTP | NTP Timestamp | Epoch            |
   |             |            | Era | Era Offset    |                  |
   +-------------+------------+-----+---------------+------------------+
   | 1 Jan -4712 | -2,400,001 | -49 | 1,795,583,104 | 1st day Julian   |
   | 1 Jan -1    | -679,306   | -14 | 139,775,744   | 2 BCE            |
   | 1 Jan 0     | -678,491   | -14 | 171,311,744   | 1 BCE            |
   | 1 Jan 1     | -678,575   | -14 | 202,939,144   | 1 CE             |
   | 4 Oct 1582  | -100,851   | -3  | 2,873,647,488 | Last day Julian  |
   | 15 Oct 1582 | -100,840   | -3  | 2,874,597,888 | First day        |
   |             |            |     |               | Gregorian        |
   | 31 Dec 1899 | 15019      | -1  | 4,294,880,896 | Last day NTP Era |
   |             |            |     |               | -1               |
   | 1 Jan 1900  | 15020      | 0   | 0             | First day NTP    |
   |             |            |     |               | Era 0            |
   | 1 Jan 1970  | 40,587     | 0   | 2,208,988,800 | First day UNIX   |
   | 1 Jan 1972  | 41,317     | 0   | 2,272,060,800 | First day UTC    |
   | 31 Dec 1999 | 51,543     | 0   | 3,155,587,200 | Last day 20th    |
   |             |            |     |               | Century          |
   | 8 Feb 2036  | 64,731     | 1   | 63,104        | First day NTP    |
   |             |            |     |               | Era 1            |
   +-------------+------------+-----+---------------+------------------+

                 Figure 4: Interesting Historic NTP Dates 
```
