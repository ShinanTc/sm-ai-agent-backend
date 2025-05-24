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

    # Extract the generated text
    quotes_list = response.text.strip().split("\n")

    # Store up to 50 quotes
    for quote in quotes_list[:50]:
        quotes.append({"Quote": quote.strip()})

    return quotes

# Optional: test the function directly
if __name__ == "__main__":
    prompt = "Generate a motivational quote about success."
    generated_quotes = generate_quotes(prompt)
    print(generated_quotes)
