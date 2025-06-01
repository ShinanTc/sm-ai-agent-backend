import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from generators.generate_quotes import generate_quotes

# Template options mapping
template_map = {
    "A": {
        "path": "templates/motivation-quotes/freakin-monday.png",
        "prompt": (
            "Generate a short, punchy motivational quote with a humorous and sarcastic tone, perfect for a Monday post. Each quote should capture grit, hustle, or a witty attitude toward overcoming the Monday blues. Avoid repeating ideas and do not use numbers or list formatting. Make the quotes sound fresh, clever, and meme-worthy — similar to: “Hate Mondays? Try being broke."
        )
    },
    "B": {
        "path": "templates/motivation-quotes/weekend-mode.png",
        "prompt": (
            "Create a light-hearted, witty, and motivational quote related to relaxation, self-care, or chill productivity. The tone should be gentle, feel-good, and perfect for a weekend vibe. Avoid repeating the same phrases or ideas and do not number the quotes. Focus on themes like slowing down, recharging, soft success, and finding balance."
        )
    },
    "C": {
        "path": "templates/motivation-quotes/generic.png",
        "prompt": (
            "Generate a unique, motivational quote tailored for people in tech or coding. Avoid clichés like 'One line of code…' and instead focus on themes such as problem-solving, persistence, debugging, creativity, and innovation. Each quote should be under 25 words, inspirational, and without numbering. Aim for a tone similar to: “Code is poetry with logic” or “Even bugs teach lessons worth learning."
        )
    },
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
