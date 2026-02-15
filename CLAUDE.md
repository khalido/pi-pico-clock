# Project Context

A Raspberry Pi Pico W clock with quote display on a Pimoroni 2" LCD.

## Architecture

- **src/main.py**: Main loop, WiFi/NTP setup, button handling, display updates
- **src/quotes_gz/**: Gzipped JSON files (00.json.gz - 23.json.gz) containing hourly quotes
- **src/env.py**: WiFi credentials (WIFI_SSID, WIFI_PASSWORD) - gitignored
- **src/env.template**: Template showing required env variables

## Project Structure

```
pi-pico-clock/
├── src/                   # Code that goes on Pico
│   ├── main.py           # Entry point (runs on boot)
│   ├── pico_utils.py     # Helper functions
│   ├── llm.py            # OpenAI API client
│   ├── clock.py          # Clock utilities
│   ├── env.py            # WiFi secrets (gitignored)
│   ├── env.template      # Template for env.py
│   └── quotes_gz/        # Hourly quote data
├── data/                 # Source data and analysis
│   ├── quotes.json       # Source quotes (not on Pico)
│   └── analysis.ipynb    # Analysis notebook
├── tests/                # Desktop tests (if any)
├── README.md             # Project docs
└── CLAUDE.md             # Development context
```

## Hardware

- Raspberry Pi Pico W (WiFi-enabled)
- Pimoroni Pico Display Pack 2.0 (320x240 LCD, 4 buttons, RGB LED)

## Key Libraries

- `picographics`: Display driver
- `pimoroni`: Button and RGB LED control
- `network`, `ntptime`: WiFi and time sync
- `gzip`, `json`: Quote file handling

## Development Notes

- Uses MicroPython (Pimoroni firmware with built-in drivers)
- Display buffer updates only on `display.update()`
- Quotes loaded hourly to conserve memory
- 4 buttons: A (GPIO 12), B (GPIO 13), X (GPIO 14), Y (GPIO 15)

## Files to Ignore

- src/env.py (contains WiFi password)
- __pycache__/
- .DS_Store

## Development Workflow (2026)

**Recommended: mpremote CLI (Simplest for AI-assisted development)**

Install (using uv):
```bash
uv tool install mpremote
```

Or with pip/pipx:
```bash
pip install mpremote
# or
pipx install mpremote
```

Common commands:
```bash
mpremote                          # Connect to REPL
mpremote cp src/main.py :main.py  # Copy single file
mpremote cp -r src/ :             # Copy entire src folder to Pico root
mpremote run src/script.py        # Run without saving to board
mpremote connect list             # List connected devices
mpremote repl                     # Interactive REPL session

# Development workflow
mpremote cp -r src/ : + repl      # Upload all and open REPL
```

**Alternative: VS Code + MicroPico Extension**
- Install MicroPico extension
- Auto-upload on save, integrated REPL
- Good for: GUI-based development

**Firmware Updates (Feb 2026)**
- **MicroPython v1.27.0** (Dec 2025) - latest stable
- **Pimoroni v1.26.1** (Sep 2025) - for Pico W with Pimoroni hardware
- Download from [pimoroni-pico releases](https://github.com/pimoroni/pimoroni-pico/releases)
- Flash via BOOTSEL button + UF2 drag-and-drop

**Check firmware version:**
```python
import sys
sys.version
```

**Install packages:**
```python
import mip
mip.install("package-name")
```

## Code Style

- Keep functions small and focused
- Use type hints where practical
- Clear variable names over comments
- Minimal comments (code should be self-documenting)

## Agent Learnings

- **MicroPython imports**: Libraries like `picographics`, `pimoroni`, `machine` are Pico-specific and will show LSP errors on desktop - this is expected
- **Memory constraints**: Loading large files crashes the Pico - use gzip compression and load only current hour's quotes
- **Display updates**: Must call `display.update()` after drawing - changes aren't automatic
- **WiFi on Pico**: Use `network.WLAN(network.STA_IF)` - connect once at boot, not in loop
- **Time sync**: `ntptime.settime()` sets UTC - convert to local timezone manually

## TODO

- [ ] Update MicroPython firmware to v1.27.0 (or latest Pimoroni v1.26.1)
- [ ] Clean up llm.py - remove test code and add error handling
- [ ] Consider migrating from deprecated GPT-3.5 to GPT-4o-mini
- [ ] Add retry logic for WiFi connection failures
- [ ] Create sample env.py template for easier setup

## Resources

- [Pimoroni Pico MicroPython](https://github.com/pimoroni/pimoroni-pico) - Official firmware and libraries
- [PicoGraphics Documentation](https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/picographics)
- [MicroPython Documentation](https://docs.micropython.org/)
- [mpremote Documentation](https://docs.micropython.org/en/latest/reference/mpremote.html) - Official MicroPython remote control tool
- [Awesome MicroPython](https://github.com/mcauser/awesome-micropython)
