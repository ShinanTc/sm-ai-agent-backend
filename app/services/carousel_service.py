from fastapi import UploadFile
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from typing import List

async def generate_carousel_images(file: UploadFile, bg_color: str) -> List[str]:
    """
    Generate carousel images from uploaded text file.
    """
    # Read content from uploaded file
    content = await file.read()
    text_content = content.decode().strip().split("---")
    
    # Define paths
    output_folder = "generated_carousel"
    font_path = "BricolageGrotesque_72pt-Bold.ttf"
    heading_template = f"templates/carousel-contents/bg-{bg_color}/heading.png"
    content_template = f"templates/carousel-contents/bg-{bg_color}/content.png"
    
    # Create output directory
    os.makedirs(output_folder, exist_ok=True)
    
    # Clear existing files
    for existing_file in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, existing_file))
    
    generated_images = []
    text_color = "#dcfb73" if bg_color == "green" else "#02ba80"
    
    # Generate images
    for i, text in enumerate(text_content):
        template = heading_template if i == 0 else content_template
        output_path = os.path.join(output_folder, f"carousel_{i+1}.png")
        
        # Generate image using PIL
        image = Image.open(template)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, 60)
        
        # Text wrapping and positioning logic (from your original code)
        image_width, image_height = image.size
        padding_x = 100
        padding_y = 80
        max_width = image_width - (2 * padding_x)
        
        # Wrap text
        lines = textwrap.wrap(text.strip(), width=max_width // 30)
        line_height = 70
        total_height = len(lines) * line_height
        current_y = (image_height - total_height) // 2
        
        for line in lines:
            text_width = draw.textbbox((0, 0), line, font=font)[2]
            x = (image_width - text_width) // 2
            draw.text((x, current_y), line, font=font, fill=text_color)
            current_y += line_height
        
        image.save(output_path)
        generated_images.append(output_path)
    
    return generated_images