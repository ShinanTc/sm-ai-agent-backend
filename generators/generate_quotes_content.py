import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from generators.generate_quotes import generate_quotes

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

def main():
    # Ask the user for template choice
    print("Select a template:")
    print("A) Freaking Monday post")
    print("B) Weekend Mode post")
    print("C) Generic Motivation post")
    template_choice = input("Enter A, B, or C: ").strip().upper()

    # Validate user input
    while template_choice not in template_map:
        template_choice = input("Invalid choice. Please enter A, B, or C: ").strip().upper()

    selected_template = template_map[template_choice]
    template_path = selected_template["path"]
    prompt = selected_template["prompt"]

    print(f"Generating quotes for: {template_choice}...")

    quotes_data = generate_quotes(prompt)
    df = pd.DataFrame(quotes_data)

    csv_file = "content.csv"
    df.to_csv(csv_file, index=False)

    text_color = "#02ba80" if template_choice == "C" else "#dcfb73"

    print(f"✅ Quotes saved to '{csv_file}'")

    font_path = "assets/BricolageGrotesque_72pt-Bold.ttf"
    font_size = 60
    padding = 80
    output_folder = "generated_posts"

    if os.path.exists(output_folder):
        for file in os.listdir(output_folder):
            os.remove(os.path.join(output_folder, file))
    else:
        os.makedirs(output_folder, exist_ok=True)

    image = Image.open(template_path)
    image_width, image_height = image.size
    max_text_width = image_width - (2 * padding)

    for index, row in df.iterrows():
        quote = row["Quote"]
        image = Image.open(template_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size)

        def wrap_text(text):
            words = text.split()
            wrapped_lines, line = [], ""
            for word in words:
                test_line = f"{line} {word}".strip()
                if draw.textbbox((0, 0), test_line, font=font)[2] < max_text_width:
                    line = test_line
                else:
                    wrapped_lines.append(line)
                    line = word
            wrapped_lines.append(line)
            return wrapped_lines

        lines = wrap_text(quote)
        line_height = font_size + 10
        total_text_height = len(lines) * line_height
        y_start = (image_height - total_text_height) // 2

        for i, line in enumerate(lines):
            text_width = draw.textbbox((0, 0), line, font=font)[2]
            x = max((image_width - text_width) // 2, padding)
            draw.text((x, y_start + i * line_height), line, font=font, fill=text_color)

        output_path = os.path.join(output_folder, f"quote_{index+1}.png")
        image.save(output_path)
        print(f"✅ Generated: {output_path}")

    print("🎉 All posts have been generated successfully!")

if __name__ == "__main__":
    main()
