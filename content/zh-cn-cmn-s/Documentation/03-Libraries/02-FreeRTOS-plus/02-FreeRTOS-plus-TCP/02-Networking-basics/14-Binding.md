---
title: 绑定
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


每个[套接字](socket.md)
都需要一个唯一的地址。如前所述，地址是
[IP 地址](IP_address.md)
和[端口号](port_number.md)的组合。

套接字创建时，会假定
创建套接字的网络节点的 IP 地址。
如果套接字有 IP 地址但没有端口号，则称为
“未绑定”。未绑定的套接字无法接收数据，因为
没有完整的地址。

如果套接字同时具有 IP 地址和端口号，则称为
“绑定到端口”或“绑定到地址”。绑定的套接字
可以接收数据，因为具有完整的地址。

将端口号分配给套接字的过程
称为“绑定”。

API 函数 [FreeRTOS_bind()](API/bind.md)
将 FreeRTOS-Plus-TCP 套接字绑定到端口号。

如果 [ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND](TCP_IP_Configuration.md#ipconfigallow_socket_send_without_bind)
在 [FreeRTOSIPConfig.h](TCP_IP_Configuration.md) 中设置为 0，
则必须使用 FreeRTOS_bind() 将套接字绑定到端口号，
然后套接字才可用于发送或接收数据。如果
在 FreeRTOSIPConfig. h 中将 ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND 设置为 1，
则未绑定的套接字在首次
尝试发送数据（对于 UDP 套接字）或连接（对于 TCP 套接字）时将自动绑定到端口号，
但仍只能在绑定后
接收数据。

