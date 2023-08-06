# pyWS2812

Control WS2812 LED by UART Serial Port Protocol + non-gate transistor

The hardware requires a USB serial port module (for example, CH34X, FT232RL) and a non-gate (preferably a Schmitt trigger) that supports a baud rate of more than 2.5 MHz

After the serial port TX pin output is connected to the data port of the WS2812 LED  through the inverter, the LED can be controlled by this module

通过UART串口协议+非门反相器来控制WS2812 LED🚨

硬件上需要一个支持2.5M波特率以上的USB转串口模块（例如<u>CH34x</u>, <u>FT232RL</u> 等）以及一个非门（最好是施密特触发器）

将串口TX引脚输出经过反相器后再连接到WS2812灯带的数据口后即可用本模块控制灯带了
