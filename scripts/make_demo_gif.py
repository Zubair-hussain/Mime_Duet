"""Draw the animated demo GIF used in the README and on the website.

The GIF shows a sample run with the demo inbox. It is an illustration, not a screen recording.

    python scripts/make_demo_gif.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "demo.gif"
FONTS = "C:/Windows/Fonts/"
W, H = 960, 540

BG = (255, 255, 255)
WINDOW = (12, 12, 16)
BAR = (26, 26, 32)
TEXT = (226, 232, 240)
DIM = (161, 161, 170)
PROMPT = (252, 165, 165)
ACCENT = (248, 113, 113)
WARN = (253, 224, 71)
OK = (134, 239, 172)

# Each frame is (list of (text, colour) lines, how long to show it in ms).
COMMAND = "python -m duet --once"
DRAFT = "  Hi Sara! Yes, invoice #42 went out this morning."
SCRIPT = [
    ("> " + COMMAND, PROMPT),
    ("", TEXT),
    ("Mini Duet wants to send to Sara (client):", WARN),
    (DRAFT, TEXT),
    ("Approve? (y/n) ", WARN),
    ("Sent.", OK),
    ("", TEXT),
    ("--- Your brief ---", ACCENT),
    ("- Sara asked about invoice #42: reply sent.", TEXT),
    ("- Dentist at 4:30 PM today. Leave by 4:00.", TEXT),
]


def load_font(size):
    """Consolas on Windows, otherwise whatever monospace Pillow can find."""
    for name in (FONTS + "consola.ttf", "DejaVuSansMono.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_frame(lines, cursor=True):
    """One frame: a white page with a dark terminal window in the middle."""
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle([40, 30, W - 40, H - 30], radius=18, fill=WINDOW)
    draw.rounded_rectangle([40, 30, W - 40, 80], radius=18, fill=BAR)
    draw.rectangle([40, 60, W - 40, 80], fill=BAR)
    for index, colour in enumerate(((248, 113, 113), (251, 191, 36), (74, 222, 128))):
        x = 68 + index * 28
        draw.ellipse([x, 47, x + 14, 61], fill=colour)
    draw.text((W / 2, 55), "mini-duet  -  demo", font=load_font(18), fill=DIM, anchor="mm")
    font = load_font(23)
    y = 105
    for text, colour in lines:
        draw.text((72, y), text, font=font, fill=colour)
        y += 36
    if cursor and lines:
        last_text = lines[-1][0]
        x = 72 + font.getlength(last_text)
        draw.rectangle([x + 2, y - 36 + 4, x + 14, y - 36 + 30], fill=TEXT)
    return image


def build_frames():
    """Turn the script into (image, duration) pairs: typing, pause, answer, result."""
    frames = []
    shown = []
    typed = ""
    for char in "> " + COMMAND:
        typed += char
        frames.append((draw_frame([(typed, PROMPT)]), 45))
    frames.append((draw_frame([(typed, PROMPT)]), 500))
    shown = [SCRIPT[0], SCRIPT[1]]
    for line in SCRIPT[2:4]:
        shown.append(line)
        frames.append((draw_frame(shown), 450))
    shown.append(SCRIPT[4])
    frames.append((draw_frame(shown), 1100))
    answered = shown[:-1] + [("Approve? (y/n) y", WARN)]
    frames.append((draw_frame(answered, cursor=False), 600))
    shown = answered
    for line in SCRIPT[5:]:
        shown = shown + [line]
        frames.append((draw_frame(shown, cursor=False), 380))
    frames.append((draw_frame(shown, cursor=False), 2600))
    return frames


