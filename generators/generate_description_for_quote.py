import google.generativeai as genai
import os

# Authenticate Gemini API (replace with your key or use .env)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_description_for_quote(quote):
    prompt = f"""
Write a small to medium-length Instagram description for the motivational quote below. 
It should be informative, talk about the message behind the quote, and sound inspiring but not preachy.
End with these hashtags:

#techmotivation #motivation #workmotivation #quote #quoteoftheday

Quote: "{quote}"
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Failed to generate description: {e}")
        return quote  # Fallback to quote itself
