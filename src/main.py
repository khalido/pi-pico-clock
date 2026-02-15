# using micropython from https://github.com/pimoroni/pimoroni-pico
import json
import os
import time

import deflate
import jpegdec  # show simple jpegs
import machine
import network
import ntptime
import requests
from picographics import DISPLAY_PICO_DISPLAY_2, PicoGraphics

# pimonori libraries
from pimoroni import RGBLED, Button

import env

# pimoniri display + buttons setup
# Pico Display 2 - 320x240 SPI LCD with 4 buttons and a RGB led
# https://shop.pimoroni.com/products/pico-display-pack-2-0
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=0)

WIDTH, HEIGHT = display.get_bounds()

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

led = RGBLED(6, 7, 8)  # the rgb led on the display board itself


# List of available pen colours, add more if necessary
RED = display.create_pen(209, 34, 41)
ORANGE = display.create_pen(246, 138, 30)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)

# raspberry pico w setup
# setup the led, defaulting to off
pico_led = machine.Pin("LED", machine.Pin.OUT, value=0)
# use led.off() or led.on() to turn on and off


# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()


def blink_led(N: int = 1, rgb=(209, 34, 41), T=0.08):
    """blinks led n times"""
    for _ in range(N):
        led.set_rgb(*rgb)
        time.sleep(T)
        led.set_rgb(0, 0, 0)
        if N > 1:
            time.sleep(0.05)


# boot process
print(f"booting...\n{os.uname().machine} running {os.uname().version}")
time.sleep(0.15)
clear()

# blink the front led, why not?
display.set_pen(GREEN)
display.text("Booting....", 2, 0, scale=3)
display.text(f"Running on {os.uname().machine}", 6, 40, WIDTH, scale=2)
display.update()
for _ in range(4):
    led.set_rgb(209, 34, 41)
    time.sleep(0.1)
    led.set_rgb(0, 0, 0)
    time.sleep(0.05)

clear()

display.set_backlight(0.5)
display.set_font("bitmap8")
display.set_pen(GREEN)
display.text("Hello World", 2, 0, scale=4)

display.set_pen(CYAN)
display.text(
    "Ok so the very basics work, now to do something useful.", 3, 40, WIDTH, scale=2
)

# Display the result
display.update()


# connect to wifi
ssid = env.WIFI_SSID
password = env.WIFI_PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 25
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print("waiting for connection...")
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError("network connection failed")
else:
    status = wlan.ifconfig()
    ip = status[0]
    print(f"connected, ip = {ip}")
    # set time from internet
    ntptime.settime()
    print(f"Time: {time.localtime()}")


# connect to web
print("attempting to fetch a url to test internet")
r = requests.get("https://httpbin.org/get")
if r.status_code == 200:
    print(r.text)  # if a print than this worked
else:
    print(f"something went wrong, status: {r.status_code} ")


display.set_backlight(0.5)
display.set_font("bitmap8")
display.set_pen(GREEN)
display.text("Hello World", 2, 0, scale=4)

display.set_pen(CYAN)
display.text(
    "Ok so the very basics work, now to do something useful.", 3, 40, WIDTH, scale=2
)

display.set_pen(GREEN)
display.text("wifi ip = " + status[0], 6, 140, WIDTH, scale=2)

# Display the result
display.update()
time.sleep(1)


def get_time():
    """returns current time in 00:00 format"""
    t = time.localtime()
    # t = (2024, 4, 20, 2, 48, 6, 5, 111)
    return f"{t[3]:02}:{t[4]:02}"


def open_quotes(hour="00"):
    print(f"attempting to open quotes file for hour {hour}")

    with gzip.open(f"quotes/{hour}.json.gz", "rb") as f:
        decompressed_data = f.read()  # data returned as bytes

    quotes = json.loads(decompressed_data.decode("utf-8"))

    print(f"loaded quotes file for hour {hour}.")

    print(quotes.keys())
    return quotes


def get_quote(time_str):
    try:
        quote = quotes[time_str]
    except:
        quote = "fake quote"
    print(quote)
    return quote


file_hour = None

# load file if necessary
time_str = get_time()
hour = time_str[:2]
if file_hour != hour:
    quotes = open_quotes(hour)
    file_hour = hour


# do the buttons
clear()
while True:

    # load file if necessary
    time_str = get_time()
    hour = time_str[:2]
    if file_hour != hour:
        quotes = open_quotes(hour)
        file_hour = hour
        print(f"loaded quotes for {hour} at time {time_str}")

    quote = get_quote(time_str)

    if button_a.read():
        blink_led()
        clear()
        display.set_pen(WHITE)
        display.text("Button A pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    elif button_b.read():
        blink_led()
        clear()
        display.set_pen(CYAN)
        display.text("Button B pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    elif button_x.read():
        blink_led()
        clear()
        display.set_pen(MAGENTA)
        display.text("Button X pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    elif button_y.read():
        blink_led()
        clear()
        display.set_pen(YELLOW)
        display.text("Button Y pressed, exiting while loop", 10, 10, 240, 3)
        display.update()
        time.sleep(1)
        clear()
        break
    else:
        clear()
        display.set_pen(GREEN)
        display.text("Press any button!", 10, 10, 240, 3)
        display.text(f"{get_time()}", 10, 70, 240, 3)
        display.text(f"{quote}", 10, 100, WIDTH, 2)
        display.update()
    time.sleep(2)  # this number is how frequently the Pico checks for button presses
