from machine import I2C, Pin, PWM
from lcd_pcf8574 import I2cLcd
import time
import network
import urequests

import sys; print(sys.version)

# ========== WiFi ==========
WIFI_SSID = "SSID"
WIFI_PASSWORD = "PASSWORD"

# =========================
# WIFI
# =========================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 20
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("WiFi connected:", wlan.ifconfig())
        return True
    else:
        print("WiFi failed")
        return False

# =========================
# LCD
# =========================
i2c = I2C(0, scl=Pin(33), sda=Pin(25), freq=100000)
lcd = I2cLcd(i2c, 0x27, rows=4, cols=20)

# Backlight brightness (optional)
pwm = PWM(Pin(26), freq=1000)
pwm.duty(600)

def show_lines(lines):
    lcd.clear()
    for i in range(4):
        lcd.move(0, i)
        lcd.write(lines[i][:20])

# =========================
# API FETCH
# =========================
WORKER_URL = "https://misty-hill-1007.darshanaswath.workers.dev/"

def fetch_data():
    try:
        print("fetching data...")
        r = urequests.get(WORKER_URL)
        data = r.json()
        r.close()
        return data
    except Exception as e:
        print("Fetch error:", e)
        return None

def format_line(left, right, width=20):
    right = str(right)
    spaces = width - len(left) - len(right)
    if spaces < 1:
        spaces = 1
    return left + (" " * spaces) + right


# =========================
# DISPLAY UPDATE
# =========================
def update_lcd():
    data = fetch_data()

    if not data:
        show_lines([
            "API Error",
            "Check network",
            "",
            ""
        ])
        return

    try:
        lines = [
            format_line("2F Cardio:", f"{data['marino2f']}%"),
            format_line("2F Gym:", f"{data['gym']}%"),
            format_line("3F Weights:", f"{data['weights']}%"),
            format_line("3F Cardio:", f"{data['cardio']}%")
        ]

        show_lines(lines)

    except Exception as e:
        show_lines([
            "Parse error",
            str(e)[:20],
            "",
            ""
        ])

# =========================
# MAIN
# =========================
def run():
    show_lines(["Booting...", "", "", ""])

    if not connect_wifi():
        show_lines(["WiFi failed", "", "", ""])
        return

    show_lines(["Connected", "Fetching data...", "", ""])

    while True:
        update_lcd()
        time.sleep(600)


