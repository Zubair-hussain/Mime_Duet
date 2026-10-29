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


