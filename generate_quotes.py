import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from generate_csv import generate_quotes  # Import function from generate_csv.py

# Template options mapping
template_map = {
    "A": {
        "path": "templates/motivation-quotes/freakin-monday.png",
        "prompt": "Hate Mondays? Try being broke - Directly give me 50 motivational quotes like that, Nothing else. It shouldn't feel repetitive. Also do not put numbers on each quote."
    },
    "B": {
        "path": "templates/motivation-quotes/weekend-mode.png",
        "prompt": "Weekend loading. Please wait forever. - Directly give me 50 light-hearted motivational quotes related to relaxation, self-care, or chill productivity. Nothing else. Also do not put numbers on each quote."
    },
    "C": {
        "path": "templates/motivation-quotes/generic.png",
        "prompt": "Co cola sold only 26 bottles in their first year, never give up - Directly give me 50 motivational quotes related to tech like this, Nothing else. Also do not put numbers on each quote."
    }
}

# Ask the user for template choice
print("Select a template:")
print("A) Freaking Monday post")
print("B) Weekend Mode post")
print("C) Generic Motivation post")
template_choice = input("Enter A, B, or C: ").strip().upper()

# Validate user input
while template_choice not in template_map:
    template_choice = input("Invalid choice. Please enter A, B, or C: ").strip().upper()

# Get the prompt and template path for the selected template
selected_template = template_map[template_choice]
template_path = selected_template["path"]
prompt = selected_template["prompt"]

# Use the prompt to generate quotes
print(f"Generating quotes for: {template_choice}...")

# Generate quotes using the generate_quotes function from generate_csv.py
quotes_data = generate_quotes(prompt)

# Convert to pandas DataFrame
df = pd.DataFrame(quotes_data)

# Save quotes to CSV file
csv_file = "content.csv"
df.to_csv(csv_file, index=False)

text_color = "#02ba80" if template_choice == "C" else "#dcfb73"

print(f"✅ Quotes saved to '{csv_file}'")

# Now, generate the images based on the CSV file
# Define font settings
font_path = "BricolageGrotesque_72pt-Bold.ttf"
font_size = 60
padding = 80  # Space from left & right edges

# Define output folder
output_folder = "generated_posts"

# Clear existing files in output folder
if os.path.exists(output_folder):
    for file in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, file))
else:
    os.makedirs(output_folder, exist_ok=True)

# Open template to get image size
image = Image.open(template_path)
image_width, image_height = image.size

# Define max text width considering padding
max_text_width = image_width - (2 * padding)  # Leaves equal space on both sides

# Process each quote
for index, row in df.iterrows():
    quote = row["Quote"]

    # Open template image
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Load custom font
    font = ImageFont.truetype(font_path, font_size)

    # Function to wrap text within max width
    def wrap_text(text):
        words = text.split()
        wrapped_lines = []
        line = ""

        for word in words:
            test_line = f"{line} {word}".strip()
            text_width = draw.textbbox((0, 0), test_line, font=font)[2]  # Get text width
            if text_width < max_text_width:
                line = test_line  # Add word to current line
            else:
                wrapped_lines.append(line)  # Store the full line
                line = word  # Start a new line with current word
        wrapped_lines.append(line)  # Add last line
        return wrapped_lines

    # Wrap the entire quote naturally
    lines = wrap_text(quote)

    # Calculate total text height
    line_height = font_size + 10  # Adjust line spacing
    total_text_height = len(lines) * line_height

    # Calculate starting Y position for centering
    y_start = (image_height - total_text_height) // 2

    # Draw each line
    for i, line in enumerate(lines):
        text_width = draw.textbbox((0, 0), line, font=font)[2]  # Get text width
        x = (image_width - text_width) // 2  # Center text with padding
        x = max(x, padding)  # Ensure it doesn't go beyond the left padding
        draw.text((x, y_start + i * line_height), line, font=font, fill=text_color)

    # Save the generated image
    output_path = os.path.join(output_folder, f"quote_{index+1}.png")
    image.save(output_path)

    print(f"✅ Generated: {output_path}")

print("🎉 All posts have been generated successfully!")
