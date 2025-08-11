from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

# Load font from file in the project directory
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "DS-DIGI.TTF")

def render_clock_text(text, bg, fg, size):
    """Render text to an image and return a Tk PhotoImage."""
    # Make an image large enough to hold the text
    FONT = ImageFont.truetype(FONT_PATH, size)
    image = Image.new("RGB", (400, 150), color=bg)
    draw = ImageDraw.Draw(image)
    draw.text((10, 20), text, font=FONT, fill=fg)  # classic LED red
    return ImageTk.PhotoImage(image)