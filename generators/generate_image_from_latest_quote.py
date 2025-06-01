import os
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from generators.generate_quotes_content import template_map

def get_latest_quote(csv_path="post_scheduler/instagram/quotes.csv"):
    """Read the latest quote from the CSV file."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError("quotes.csv not found.")
    
    df = pd.read_csv(csv_path)
    if df.empty:
        raise ValueError("quotes.csv is empty.")
    
    return df.iloc[-1]["Quote"]

def get_template_for_today():
    """Select template based on the day of the week."""
    today = datetime.now().strftime("%A")
    if today == "Monday":
        return "A"
    elif today == "Friday":
        return "B"
    else:
        return "C"

def wrap_text(draw, text, font, max_width):
    """Wrap text based on max width."""
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if draw.textbbox((0, 0), test_line, font=font)[2] < max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines

def create_image_with_latest_quote():
    """Generate an image using the latest quote from CSV."""
    quote = get_latest_quote()
    template_choice = get_template_for_today()
    template_path = template_map[template_choice]["path"]

    font_path = "assets/BricolageGrotesque_72pt-Bold.ttf"
    font_size = 60
    padding = 80
    output_folder = "generated_posts"
    text_color = "#02ba80" if template_choice == "C" else "#dcfb73"

    os.makedirs(output_folder, exist_ok=True)

    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)

    image_width, image_height = image.size
    max_text_width = image_width - 2 * padding

    lines = wrap_text(draw, quote, font, max_text_width)
    line_height = font_size + 10
    total_text_height = len(lines) * line_height
    y_start = (image_height - total_text_height) // 2

    for i, line in enumerate(lines):
        text_width = draw.textbbox((0, 0), line, font=font)[2]
        x = max((image_width - text_width) // 2, padding)
        draw.text((x, y_start + i * line_height), line, font=font, fill=text_color)

    output_path = os.path.join(output_folder, "latest_quote.png")
    image.save(output_path)
    print(f"✅ Image saved to {output_path}")

if __name__ == "__main__":
    create_image_with_latest_quote()
