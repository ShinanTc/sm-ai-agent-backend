import google.generativeai as genai
import os

# Authenticate Gemini API (replace with your key or use .env)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_description_for_quote(quote):
    prompt = f"""
Write a 2–4 sentence Instagram description for the following motivational quote. The description should clearly explain the core message behind the quote in a way that resonates with tech professionals, students, freelancers, and a broader audience seeking motivation. Keep the tone clean, professional, and inspiring without sounding preachy or personal. Avoid using emojis. If helpful, include a relatable example or metaphor to bring the quote’s meaning to life. End the caption with these hashtags:

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
