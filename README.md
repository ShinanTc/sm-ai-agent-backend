### TECH STACK USED:

Programming Language: Python 🐍  
Image Processing: Pillow (PIL) 🎨  
Data Handling: Pandas 📊  
Font Management: Custom TTF Font (Bricolage Grotesque) 🎨  

---

## HOW TO RUN?

# Instagram Post Generator

## Description
This script generates motivational quote images based on a provided CSV or text file. The text is formatted and centered on a template image with proper line wrapping. Users can select a specific template before generating the images.

Additionally, a **Carousel Image Generator** is included, which extracts structured content from a `.txt` file and creates a carousel-style image sequence.

---

## Installation & Setup

### 1. Create and Activate a Virtual Environment
```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate on macOS/Linux
venv\Scripts\activate  # Activate on Windows
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare the Data File
- **For Instagram Post Generator**: Place a `content.csv` file with the quotes. You can generate a fresh CSV using ChatGPT or manually create one.
- **For Carousel Image Generator**: Place a `content.txt` file structured as follows:

```
Main Heading
---
Content 1
---
Content 2
---
Content 3
```

Each `---` separator will indicate the next slide in the carousel.

### 4. Provide Base Templates
Ensure that you have template images inside the `templates` directory. The project is currently optimized for specific base templates:
- `freakin-monday.png`
- `weekend-mode.png`
- `generic.png` (used for generic posts)
- `carousel_base.png` (for carousel posts)

Each generator will choose the relevant template based on the input.

### 5. Include a Font File
- Place a `.ttf` font file in the root directory.
- If missing, download the required font from [Google Fonts](https://fonts.google.com/) and place it in the root folder.
- Update the `font_path` variable in `generate_quotes.py` and `generate_carousel.py` to reflect the correct font file name.

---

## Running the Scripts

### Instagram Post Generator
```bash
python generate_quotes.py
```
When prompted, choose a template:
```
Choose a template:
A) Freaking Monday Post
B) Weekend Mode Post
C) Generic Post
```
- Enter `A` to use `freakin-monday.png`.
- Enter `B` to use `weekend-mode.png`.
- Enter `C` to use `generic.png`.

**Output:** Generated images will be saved inside the `/generated_posts/` directory.

---

### Carousel Image Generator
```bash
python generate_carousel.py
```
This script will:
- Read content from `content.txt`
- Generate images for each section
- Store them inside `/generated_carousel/`

**Output:** Generated carousel images will be saved inside the `/generated_carousel/` directory.

---

## Features
✅ Automatically wraps text to fit within the template  
✅ Padding is applied to avoid text overlapping  
✅ Allows different base templates for different content types  
✅ **Carousel Generation** for structured content  
✅ **Automatic Folder Cleanup**: Each time you generate images, the previous files are deleted to maintain a fresh output  

---

## Notes
- Ensure your CSV file has a column named `Quote`.
- Ensure your `.txt` file is structured properly for carousel generation.
- Font size and positioning are automatically adjusted for best fit.

Happy Generating! 🚀