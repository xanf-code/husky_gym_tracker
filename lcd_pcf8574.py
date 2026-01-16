from machine import I2C
import time

class I2cLcd:
    def __init__(self, i2c, addr, rows=2, cols=16):
        self.i2c = i2c
        self.addr = addr
        self.rows = rows
        self.cols = cols
        self.backlight = 0x08

        self.init_lcd()

    def write_byte(self, data):
        self.i2c.writeto(self.addr, bytes([data | self.backlight]))

    def pulse_enable(self, data):
        self.write_byte(data | 0x04)
        time.sleep_us(1)
        self.write_byte(data & ~0x04)
        time.sleep_us(50)

    def send(self, data, mode=0):
        high = mode | (data & 0xF0)
        low  = mode | ((data << 4) & 0xF0)

        self.write_byte(high)
        self.pulse_enable(high)
        self.write_byte(low)
        self.pulse_enable(low)

    def cmd(self, cmd):
        self.send(cmd, 0)

    def write_char(self, char):
        self.send(ord(char), 1)

    def write(self, text):
        for c in text:
            self.write_char(c)

    def clear(self):
        self.cmd(0x01)
        time.sleep_ms(2)

    def move(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]

        if row >= self.rows:
            row = self.rows - 1

        self.cmd(0x80 | (col + row_offsets[row]))


    def init_lcd(self):
        time.sleep_ms(50)
        self.cmd(0x33)
        self.cmd(0x32)
        self.cmd(0x28)
        self.cmd(0x0C)
        self.cmd(0x06)
        self.clear()

