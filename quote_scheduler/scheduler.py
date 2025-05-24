import schedule
import time
from datetime import datetime
import pytz
import os
import sys
import pandas as pd

# Add the project root to Python path to import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators.generate_quotes import generate_quotes
from generators.generate_quotes_content import template_map

def get_template_for_day():
    """Determine which template to use based on the day of the week."""
    today = datetime.now().strftime("%A")
    
    if today == "Monday":
        return "A", template_map["A"]["prompt"]  # Monday template
    elif today == "Friday":
        return "B", template_map["B"]["prompt"]  # Weekend template
    else:
        return "C", template_map["C"]["prompt"]  # Generic template

def is_quote_unique(quote, csv_path="quote_scheduler/quotes.csv"):
    """Check if the quote already exists in the CSV file."""
    if not os.path.exists(csv_path):
        return True
        
    df = pd.read_csv(csv_path)
    return quote not in df["Quote"].values

from datetime import datetime
import os
import csv

from generators.generate_image_from_latest_quote import create_image_with_latest_quote

def save_quote(quote, csv_path="quote_scheduler/quotes.csv"):
    """Save a quote to CSV and generate image."""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    # Save to CSV
    with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if os.path.getsize(csv_path) == 0:
            writer.writerow(["Quote", "Date"])
        writer.writerow([quote, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    
    print("✅ Quote saved to CSV.")

    # Generate image using the latest quote
    create_image_with_latest_quote()


def generate_daily_quote():
    """Generate and process daily quote."""
    print(f"Starting quote generation at {datetime.now()}")
    
    # Get template and prompt based on day
    template_choice, prompt = get_template_for_day()
    
    # Generate quotes until we get a unique one
    while True:
        quotes = generate_quotes(prompt)
        if not quotes:
            print("Failed to generate quotes")
            return
            
        quote = quotes[0]["Quote"]
        if is_quote_unique(quote):
            break
            
        print("Generated quote already exists, trying again...")
    
    # Save the unique quote
    save_quote(quote)
    
    # Import here to avoid circular imports
    from generators.generate_quotes_content import template_map
    
    # Set up the environment for quote generation
    os.environ["TEMPLATE_CHOICE"] = template_choice
    os.environ["QUOTE_TEXT"] = quote
    
    print(f"Generated quote for {datetime.now().strftime('%A')}: {quote}")
    print(f"Using template: {template_map[template_choice]['path']}")
    
    # TODO: Add Instagram posting logic here
    
def run_scheduler():
    """Run the scheduler."""
    # Convert 5:00 PM IST to system's local time
    ist = pytz.timezone('Asia/Kolkata')
    target_time = "18:00"
    
    schedule.every().day.at(target_time).do(generate_daily_quote)
    
    print(f"Scheduler started. Will generate quotes daily at {target_time} IST")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()