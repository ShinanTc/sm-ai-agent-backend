import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Ask user for background choice
bg_choice = input("Choose background color (A: Green / B: Yellow): ").strip().upper()
if bg_choice == "A":
    bg_choice = "green"
    text_color = "#dcfb73"  # Text color for green background
elif bg_choice == "B":
    bg_choice = "yellow"
    text_color = "#02ba80"  # Text color for yellow background
else:
    print("Invalid choice. Defaulting to green.")
    bg_choice = "green"
    text_color = "#dcfb73"  # Default text color for green background

# Paths
text_file = "content.txt"
heading_template = f"templates/carousel-contents/bg-{bg_choice}/heading.png"
content_template = f"templates/carousel-contents/bg-{bg_choice}/content.png"
output_folder = "generated_carousel"
font_path = "BricolageGrotesque_72pt-Bold.ttf"

# Font settings
font_size = 60
padding_x = 100  # Horizontal padding
padding_y = 80   # Vertical padding

# Ensure output folder is cleared before generating new images
if os.path.exists(output_folder):
    for file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
os.makedirs(output_folder, exist_ok=True)

# Load text content
def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip().split("---")

# Wrap text function
def wrap_text(draw, text, font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        wrapped_lines = textwrap.wrap(paragraph, width=max_width // (font_size // 2))
        lines.extend(wrapped_lines + [""])  # Add space between paragraphs
    return [line.strip() for line in lines if line.strip()]

# Function to generate image
def generate_image(template_path, text, output_name):
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)

    image_width, image_height = image.size
    max_text_width = image_width - (2 * padding_x)

    # Wrap text dynamically based on image width
    lines = wrap_text(draw, text, font, max_text_width)
    line_height = font_size + 10
    total_text_height = len(lines) * line_height

    # Start Y position so text is centered properly
    y_start = (image_height - total_text_height) // 2

    for i, line in enumerate(lines):
        text_width = draw.textbbox((0, 0), line, font=font)[2]
        x = (image_width - text_width) // 2
        y = y_start + (i * line_height)
        draw.text((x, y), line, font=font, fill=text_color)
    
    image.save(os.path.join(output_folder, output_name))
    print(f"✅ Generated: {output_name}")

# Load content
content = load_text(text_file)

# Generate heading image
generate_image(heading_template, content[0], "carousel_1.png")

# Generate content images
for i, text in enumerate(content[1:], start=2):
    generate_image(content_template, text, f"carousel_{i}.png")

print("🎉 Carousel images generated successfully!")
