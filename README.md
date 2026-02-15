# pi-pico-clock

A Raspberry Pi Pico W clock that displays quotes on a Pimoroni 2-inch display.

![Hardware Setup](https://shop.pimoroni.com/cdn/shop/products/pico-display-pack-2-0-1_1024x1024.jpg)

## Features

- **Real-time Clock**: Syncs time via NTP over WiFi
- **Hourly Quotes**: Displays different quotes for each hour from gzipped JSON files
- **Interactive Buttons**: 4 buttons (A, B, X, Y) for user interaction
- **RGB LED Feedback**: Visual feedback via onboard RGB LED
- **320x240 LCD Display**: Clear, colorful text rendering

## Hardware Requirements

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/) or [Pico WH](https://littlebirdelectronics.com.au/products/raspberry-pi-pico-wh) (WiFi-enabled, WH = pre-soldered headers)
- [Pimoroni Pico Display Pack 2.0](https://shop.pimoroni.com/products/pico-display-pack-2-0) (320x240 LCD + 4 buttons + RGB LED)

## Quick Start

### 1. Install Firmware

1. Download the Pimoroni MicroPython firmware from [pimoroni-pico releases](https://github.com/pimoroni/pimoroni-pico/releases)
   - Use the file named `pimoroni-picow-vX.X.X-micropython.uf2`
2. Hold the **BOOTSEL** button and plug in the USB cable
3. Copy the `.uf2` file to the **RPI-RP2** drive that appears
4. The Pico will reboot automatically

### 2. Configure WiFi

Create `src/env.py` from the template:

```bash
cp src/env.template src/env.py
```

Then edit `src/env.py` with your credentials:

```python
WIFI_SSID = "your-wifi-name"
WIFI_PASSWORD = "your-wifi-password"
```

Note: `src/env.py` is in `.gitignore` to prevent accidental commits.

### 3. Upload Code

Upload `src/main.py` and the `src/quotes_gz/` folder to your Pico using:
- [VS Code + MicroPico extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go)
- [Thonny IDE](https://thonny.org/) (beginner-friendly)
- **mpremote CLI** (recommended):
  ```bash
  mpremote cp -r src/ :
  ```

### 4. Run

The clock will:
- Connect to WiFi
- Sync time via NTP
- Display the current time and hourly quote
- Respond to button presses

## Project Structure

```
.
├── src/                   # Code that goes on Pico
│   ├── main.py           # Main application - clock + display logic
│   ├── pico_utils.py     # Helper functions
│   ├── pico_utils.py     # Helper functions
│   ├── env.py            # WiFi credentials (gitignored)
│   ├── env.template      # Template for env.py
│   └── quotes_gz/        # Hourly quotes in gzipped JSON format
│       ├── 00.json.gz
│       ├── 01.json.gz
│       └── ...
├── data/                 # Source data and analysis
│   ├── quotes.json       # Source quotes (not on Pico)
│   └── analysis.ipynb    # Analysis notebook
├── tests/                # Desktop tests
├── README.md             # Project docs
└── CLAUDE.md             # Development context
```

## Button Layout

```
┌─────────────────────────────────────┐
│           320x240 Display           │
│                                     │
│         HH:MM (current time)        │
│                                     │
│     "Quote of the hour text         │
│       displayed here..."            │
│                                     │
└─────────────────────────────────────┘
    [A]  [B]  [X]  [Y]
    ↑    ↑    ↑    ↑
  LED blink on press
```

## Development

### VS Code Setup

1. Install the [MicroPico extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go)
2. Open the project folder
3. The extension auto-connects to the Pico and enables:
   - Code upload on save
   - REPL terminal
   - File explorer for the Pico filesystem

### Installing Packages

MicroPython uses `mip` instead of pip:

```python
import mip
mip.install("package-name")
```

See available packages at [micropython-lib](https://github.com/micropython/micropython-lib).

### Display API Reference

```python
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)
display.set_backlight(0.5)  # 0.0 to 1.0

# Colors
RED = display.create_pen(209, 34, 41)
WHITE = display.create_pen(255, 255, 255)

# Drawing
display.set_pen(WHITE)
display.text("Hello", x=10, y=10, wordwrap=320, scale=3)
display.line(x1, y1, x2, y2, thickness=1)
display.circle(x, y, radius)
display.rectangle(x, y, width, height)
display.update()  # Required to show changes
```

## Quotes Format

Quotes are stored in gzipped JSON files by hour:

```json
{
  "08:00": "The early bird catches the worm.",
  "08:01": "Every moment is a fresh beginning.",
  ...
}
```

Files are named `00.json.gz` through `23.json.gz` in the `quotes_gz/` directory.

## Resources

- [Pimoroni Pico MicroPython](https://github.com/pimoroni/pimoroni-pico)
- [PicoGraphics Documentation](https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/picographics)
- [MicroPython Documentation](https://docs.micropython.org/)
- [Awesome MicroPython](https://github.com/mcauser/awesome-micropython)

## License

MIT
