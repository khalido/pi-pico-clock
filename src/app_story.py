import gc
import time

_story = "Press X for a fun fact!"
_loading = False
_x_was_pressed = False

_SYSTEM = (
    "You are a fun assistant for a kid. "
    "Share an interesting fun fact in 2-3 sentences, max 45 words. "
    "Be enthusiastic and surprising. "
    "Just the fact, no title or quotes."
)


def _draw(display, colors, WIDTH, HEIGHT):
    display.set_pen(colors["BLACK"])
    display.clear()

    # Border frame
    display.set_pen(colors["CYAN"])
    display.rectangle(4, 4, WIDTH - 8, HEIGHT - 8)
    display.set_pen(colors["BLACK"])
    display.rectangle(8, 8, WIDTH - 16, HEIGHT - 16)

    # Title
    display.set_pen(colors["YELLOW"])
    display.text("FUN FACTS", 80, 16, WIDTH, 3)

    # Divider line
    display.set_pen(colors["CYAN"])
    display.rectangle(20, 42, WIDTH - 40, 2)

    # Story text
    display.set_pen(colors["WHITE"])
    display.text(_story, 20, 52, 280, 2)

    # Button hint
    display.set_pen(colors["GREEN"])
    display.text("X: new fact", 20, 222, WIDTH, 2)

    display.update()


def init(display, buttons, led, colors, WIDTH, HEIGHT):
    global _story, _loading, _x_was_pressed
    _story = "Press X for a fun fact!"
    _loading = False
    _x_was_pressed = False
    _draw(display, colors, WIDTH, HEIGHT)


def update(display, buttons, led, colors, WIDTH, HEIGHT):
    global _story, _loading, _x_was_pressed

    x_pressed = buttons["X"].read()
    x_edge = x_pressed and not _x_was_pressed
    _x_was_pressed = x_pressed

    if x_edge and not _loading:
        _loading = True
        _story = "Searching..."
        _draw(display, colors, WIDTH, HEIGHT)
        led.set_rgb(0, 0, 255)

        try:
            import llm
            gc.collect()
            _story = llm.prompt(
                "Tell me a random fun fact about science, animals, space, or history",
                system=_SYSTEM,
                max_tokens=400,
                web_search=True,
            )
        except Exception as e:
            _story = f"Error: {e}"
            print(f"LLM error: {e}")

        led.set_rgb(0, 0, 0)
        _loading = False
        _draw(display, colors, WIDTH, HEIGHT)
