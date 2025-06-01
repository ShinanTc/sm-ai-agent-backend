import schedule
import time
from datetime import datetime
import os
import sys
import pandas as pd
import csv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators.generate_quotes import generate_quotes
from generators.generate_quotes_content import template_map
from generators.generate_image_from_latest_quote import create_image_with_latest_quote
from instagrapi import Client
from generators.generate_description_for_quote import generate_description_for_quote

# 🔐 Instagram credentials (replace with your actual credentials)
INSTAGRAM_USERNAME = os.getenv("IG_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("IG_PASSWORD")
SESSION_FILE = "insta_settings.json"

def get_template_for_day():
    today = datetime.now().strftime("%A")
    if today == "Monday":
        return "A", template_map["A"]["prompt"]
    elif today == "Friday":
        return "B", template_map["B"]["prompt"]
    else:
        return "C", template_map["C"]["prompt"]

def is_quote_unique(quote, csv_path="post_scheduler/instagram/quotes.csv"):
    if not os.path.exists(csv_path):
        return True
    df = pd.read_csv(csv_path)
    return quote not in df["Quote"].values

def save_quote(quote, csv_path="post_scheduler/instagram/quotes.csv"):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if os.path.getsize(csv_path) == 0:
            writer.writerow(["Quote", "Date"])
        writer.writerow([quote, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    print("✅ Quote saved to CSV.")
    create_image_with_latest_quote()

def get_instagram_client():
    client = Client()
    try:
        if os.path.exists(SESSION_FILE):
            client.load_settings(SESSION_FILE)
            client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            print("✅ Logged in using saved session.")
        else:
            raise Exception("Session not found. Performing first-time login.")
    except Exception as e:
        print(f"🔐 {e}")
        print("⚠️ Performing fresh login...")
        client = Client()
        client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        client.dump_settings(SESSION_FILE)
        print("✅ Session saved to file.")
    return client

def post_to_instagram():
    image_path = "generated_posts/latest_quote.png"
    caption = os.environ.get("QUOTE_TEXT", "Daily Inspiration")

    try:
        client = get_instagram_client()
        client.photo_upload(image_path, caption)
        print("✅ Successfully posted to Instagram.")
    except Exception as e:
        print(f"❌ Failed to post to Instagram: {e}")

def generate_daily_quote():
    print(f"📅 Starting quote generation at {datetime.now()}")
    template_choice, prompt = get_template_for_day()

    while True:
        quotes = generate_quotes(prompt)
        if not quotes:
            print("❌ Failed to generate quotes")
            return

        quote = quotes[0]["Quote"]
        if is_quote_unique(quote):
            break

        print("🔁 Generated quote already exists, trying again...")

    save_quote(quote)

    os.environ["TEMPLATE_CHOICE"] = template_choice
    description = generate_description_for_quote(quote)
    os.environ["QUOTE_TEXT"] = description


    print(f"✅ Generated quote for {datetime.now().strftime('%A')}: {quote}")
    print(f"🧩 Using template: {template_map[template_choice]['path']}")

    post_to_instagram()

def run_scheduler():
    target_time = "16:28"
    schedule.every().day.at(target_time).do(generate_daily_quote)
    print(f"⏰ Scheduler started. Will generate and post daily at {target_time} IST")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()
