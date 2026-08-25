---
title: TCP 回显服务器示例
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例](TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


此示例使用 FreeRTOS-Plus-TCP 创建一个回显服务器，
该服务器在标准[回显协议](https://en.wikipedia.org/wiki/Echo_Protocol)
端口 7 上侦听回显请求。
可能需要将
mainCREATE_SIMPLE_TCP_ECHO_SERVER 设置为 1
（具体位置为项目的 main.c 源文件顶部），以将示例包含在
构建中。此示例未包含在所有 FreeRTOS-Plus-TCP 演示中。

当在 [FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT Windows 演示](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/examples_FreeRTOS_simulator)中执行示例时，
回显请求会从 Windows 线程发送到回显服务器，
并使用 Windows TCP/IP 堆栈，因此无需进一步操作。

当使用任何 FreeRTOS-Plus-TCP 演示而非 Windows 演示执行示例时，
则需要手动向服务器发送回显请求
。这可通过使用第三方 [EchoTool](https://github.com/PavelBansky/EchoTool)
实用工具实现（链接中提供了预建可执行文件
）。

下面的 `TCPEcho.bat` 命令使用 `echotool` 将回显请求发送到 FreeRTOS-Plus-TCP 回显
服务器：

```c
REM Echo 10 times then disconnect and start over.  Assumes the target's LLMNR
REM name is "RTOSDemo".
:start
echotool RTOSDemo /t 5 /p tcp /r 7 /n 10 /d 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299

goto start

```

![使用 echotool 向 FreeRTOS-Plus-TCP 回显服务器发送回显请求](/media/2018/freertos_echo_server.jpg)
*TCPEcho.bat 使用 EchoTool 重复连接使用 FreeRTOS-Plus-TCP* 实现的回显服务器，向其发送十个回显请求，接收回显回复，然后
 断开连接。
