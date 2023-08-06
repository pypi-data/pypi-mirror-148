import serial
import threading
import time
import math
from collections import deque
from abc import ABC, abstractclassmethod


class LEDColorConst:
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    GRAY = "#808080"
    RED = "#FF0000"
    ORANGE = "#FFA500"
    YELLOW = "#FFFF00"
    GREEN = "#00FF00"
    CYAN = "#00FFFF"
    BLUE = "#0000FF"
    PURPLE = "#800080"
    VIOLET = "#EE82EE"


class WS2812Controller:

    def __init__(self, port, baudrate=3000000, n_led=1) -> None:
        """

        Args:
            port (_type_): on Windows, it is like as "COMx"; in Linux, it would be like as "/dev/ttyUSBx"
            baudrate (int, optional): UART protocol baudrate. Defaults to 3000000.
            n_led (int, optional): _description_. Defaults to 1.
        """
        self.n_led = n_led
        #串口通信，每次传输8bit且无奇偶校验位
        self.ser = serial.Serial(port=port,
                                 baudrate=baudrate,
                                 bytesize=8,
                                 parity=serial.PARITY_NONE,
                                 stopbits=1,
                                 timeout=5)
        self.__color_status = [LEDColorConst.BLACK] * self.n_led

    def __del__(self):
        self.close()

    @property
    def color_status(self):
        return self.__color_status

    @color_status.setter
    def color_status(self, color_arr):
        colors = color_arr[:self.n_led] + self.__color_status[len(color_arr):]
        colors = self.colors_formatting(colors)
        self.__color_status = colors[:]

    def close(self):
        """Close and release resource
        """
        self.turn_off_all()
        if not self.ser.closed:
            self.ser.close()

    def refresh(self):
        """refresh LED colors by color_status
        """
        uartmsg = self.colors_to_uartmsg(self.__color_status)
        if not self.ser.closed:
            self.ser.write(uartmsg)

    def color_to_uartbytes(self, color_data):
        dic = {'1': '110', '0': '100'}
        bytes_data = []
        if isinstance(color_data, str):
            #颜色采用#xxxxxx形式
            color = color_data[-6:]
            #WS2812采用GRB颜色，需要将RGB转为GRB
            grbcolor = color[2:4] + color[:2] + color[4:]
            cb = bin(int(grbcolor, 16))[2:].zfill(24)
        else:
            #颜色采用(r, g, b)形式
            cb = bin(color_data[1] % 256)[2:].zfill(8) + bin(color_data[0] % 256)[2:].zfill(8) + bin(
                color_data[2] % 256)[2:].zfill(8)
        i = 0
        while i < 24:
            #颜色数据每3位进行切割，用一个字节来表示3位数据，由于UART用小端序传输，还需要reverse一下
            sx = (dic[cb[i]] + dic[cb[i + 1]] + dic[cb[i + 2]])[1:][::-1]
            #UART空闲是高电平，因此TX端口需要接一个非门，这里就需要按位取反
            rsx = ''.join(['0' if b == '1' else '1' for b in sx])
            x = int(rsx, 2)
            bytes_data.append(x)
            i += 3
        return bytes(bytes_data)

    def colors_to_uartmsg(self, color_arr):
        led_data = b''
        for color in color_arr:
            led_data += self.color_to_uartbytes(color)
        return led_data

    def set_colors(self, color_arr):
        """Set the color of all LED in order

        Args:
            color_arr (_type_): Color array data, 
        """
        # colors = color_arr[:self.n_led] + self.__color_status[len(color_arr):]
        # colors = self.colors_formatting(colors)
        # self.__color_status = colors[:]
        self.color_status = color_arr
        self.refresh()

    def set_pixel_color(self, id, color):
        """Set single pixel color

        Args:
            id (_type_): the ID of the led what you want to set. the range of value must between 0~n_led, otherwise the request would be ingored.
            color (_type_): the color what you want to set. format must be like (r,g,b) or #aabbcc
        """
        if id < 0 or id >= self.n_led:
            return
        self.__color_status[id] = color
        self.refresh()

    def turn_on_all(self, brightness=50):
        """Turn on all LED lights

        Args:
            brightness (int, optional): Range of value is 0~100 . Defaults to 50.
        """
        brightness = min(100, abs(brightness))
        if brightness == 100:
            self.set_colors([LEDColorConst.WHITE] * self.n_led)
        else:
            c = int(255 * brightness / 100)
            self.set_colors([(c, c, c)] * self.n_led)

    def turn_off_all(self):
        """Turn off all LED lights
        """
        self.set_colors([LEDColorConst.BLACK] * self.n_led)

    def colors_formatting(self, colors_arr, mode="hex"):
        """Formatting colors data
        e.g. (255,0,255) -> #ff00ff

        Args:
            colors_arr (_type_): colors data

        Returns:
            _type_: formatted colors data
        """
        decimal2hex = lambda num: hex(min(abs(num), 255))[2:].zfill(2)
        formated_colors = []
        if mode == "hex":
            for c in colors_arr:
                if isinstance(c, str):
                    fc = "#" + c[-6:].upper()
                elif isinstance(c, (tuple, list)):
                    fc = "#" + (decimal2hex(c[0]) + decimal2hex(c[1]) + decimal2hex(c[2])).upper()
                else:
                    fc = LEDColorConst.BLACK
                formated_colors.append(fc)
        elif mode == "tuple":
            for c in colors_arr:
                if isinstance(c, str):
                    fcr = int("0x" + c[-6:-4], 16)
                    fcg = int("0x" + c[-4:-2], 16)
                    fcb = int("0x" + c[-2:], 16)
                    fc = (fcr, fcg, fcb)
                elif isinstance(c, (tuple, list)):
                    fc = tuple(c)
                else:
                    fc = (0, 0, 0)
                formated_colors.append(fc)
        return formated_colors


class AbstractWS2812Thread(ABC):

    def __init__(self, controller: WS2812Controller) -> None:
        self.controller = controller
        self.controller.turn_off_all()
        self.thid = 0

    def start(self):
        self.thid += 1
        self.ctrl_thread = threading.Thread(target=self.loop_event, daemon=True, args=(self.thid, ))
        self.ctrl_thread.start()

    def stop(self):
        self.thid = 0
        self.ctrl_thread = None

    @abstractclassmethod
    def loop_event(self, thid):
        pass


class WS2812BlinkMode(AbstractWS2812Thread):

    def __init__(self, controller: WS2812Controller, period: float, duty: float = 0.5, blink_colors=None) -> None:
        super().__init__(controller)
        self.period = period
        self.duty = duty
        if blink_colors != None:
            self.blink_colors = blink_colors
        else:
            self.blink_colors = controller.color_status

    def loop_event(self, thid):
        while thid == self.thid:
            self.controller.set_colors(self.blink_colors)
            time.sleep(self.period * self.duty)
            self.controller.turn_off_all()
            time.sleep(self.period * (1 - self.duty))



class WS2812BreathMode(AbstractWS2812Thread):

    def __init__(self, controller: WS2812Controller, period: float, blink_colors=None) -> None:
        super().__init__(controller)
        self.period = period
        if blink_colors != None:
            self.blink_colors = controller.colors_formatting(blink_colors, mode="tuple")
        else:
            self.blink_colors = controller.colors_formatting(controller.color_status, mode="tuple")

    def loop_event(self, thid):
        N = 50
        while thid == self.thid:
            for i in range(N):
                k = math.sin(i * math.pi / N)
                colors = [(int(k * c[0]), int(k * c[1]), int(k * c[2])) for c in self.blink_colors]
                self.controller.set_colors(colors)
                time.sleep(self.period / N)
        
        


class WS2812StreamMode(AbstractWS2812Thread):

    def __init__(self, controller: WS2812Controller, interval_time: float, gap: int = 1, color_que=None) -> None:
        super().__init__(controller)
        self.interval_time = interval_time
        self.gap = gap
        if isinstance(color_que, (list, deque)):
            self._color_que = deque(color_que)
        else:
            self._color_que = color_que

        self.__color_lst = [LEDColorConst.BLACK] * self.controller.n_led

    def loop_event(self, thid):
        while thid == self.thid:
            for k in range(self.gap):
                if len(self._color_que) > 0:
                    self.__color_lst.insert(0, self._color_que.popleft())
                else:
                    self.__color_lst.insert(0, LEDColorConst.BLACK)
                self.__color_lst.pop()
            self.controller.set_colors(self.__color_lst)
            time.sleep(self.interval_time)

    def push_colors(self, color_arr):
        for c in color_arr:
            self._color_que.appendleft(c)


class WS2812LoopMode(AbstractWS2812Thread):

    def __init__(self, controller: WS2812Controller, interval_time: float, gap: int = 1, color_que=None) -> None:
        super().__init__(controller)
        self.interval_time = interval_time
        self.gap = gap
        if isinstance(color_que, (list, deque)):
            self._color_que = deque(color_que)
        else:
            self._color_que = color_que

        self.__color_lst = [LEDColorConst.BLACK] * self.controller.n_led

    def loop_event(self, thid):
        while thid == self.thid:
            for k in range(self.gap):
                if len(self._color_que) > 0:
                    self.__color_lst.insert(0, self._color_que.popleft())
                else:
                    self.__color_lst.insert(0, LEDColorConst.BLACK)
                c = self.__color_lst.pop()
                self._color_que.append(c)
            self.controller.set_colors(self.__color_lst)
            time.sleep(self.interval_time)


if __name__ == "__main__":
    wsc = WS2812Controller("COM3", n_led=6)
    wsc.turn_on_all()
    time.sleep(5)
    loopctrl = WS2812LoopMode(wsc,
                              0.5,
                              2,
                              color_que=[
                                  LEDColorConst.BLUE, LEDColorConst.RED, LEDColorConst.YELLOW, LEDColorConst.VIOLET,
                                  LEDColorConst.ORANGE
                              ])
    loopctrl.start()
    time.sleep(10)
    loopctrl.stop()
    time.sleep(5)
    wsc.close()