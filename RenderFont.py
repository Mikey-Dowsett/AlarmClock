from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

# Load font from file in the project directory
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "DS-DIGI.TTF")

def render_clock_text(text, bg, fg, size):
    # Make an image large enough to hold the text
    font = ImageFont.truetype(FONT_PATH, size)

    # Width for widest string, e.g. "88:88:88"
    fixed_text = "88:88:88"
    bbox_fixed = font.getbbox(fixed_text)
    fixed_width = bbox_fixed[2] - bbox_fixed[0]
    fixed_height = bbox_fixed[3] - bbox_fixed[1]

    # Measure actual text bbox
    bbox_text = font.getbbox(text)
    text_width = bbox_text[2] - bbox_text[0]
    text_height = bbox_text[3] - bbox_text[1]

    img_width = fixed_width + 20
    img_height = fixed_height + 40
    image = Image.new("RGB", (img_width, img_height), color=bg)
    draw = ImageDraw.Draw(image)

    # Center text horizontally inside fixed width
    x = (img_width - text_width) // 2
    y = 10  # vertical padding

    draw.text((x, y), text, font=font, fill=fg)

    return ImageTk.PhotoImage(image)