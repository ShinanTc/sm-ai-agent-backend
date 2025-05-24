import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Get API Key from environment variable
API_KEY = os.getenv('GEMINI_API_KEY')

# Configure the Gemini API
genai.configure(api_key=API_KEY)

# Function to generate quotes using Gemini
def generate_quotes(prompt):
    quotes = []

    # Use the appropriate model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Generate content from prompt
    response = model.generate_content(prompt)

    # Extract and clean the generated text
    quotes_list = response.text.strip().split("\n")

    for quote in quotes_list[:50]:
        # Remove leading *, -, or numbers with dots (e.g., "1. ", "* ", "- ")
        cleaned = quote.strip().lstrip("*-0123456789. ").strip()
        quotes.append({"Quote": cleaned})

    return quotes


# Optional: test the function directly
if __name__ == "__main__":
    prompt = "Generate a motivational quote about success."
    generated_quotes = generate_quotes(prompt)
    print(generated_quotes)
