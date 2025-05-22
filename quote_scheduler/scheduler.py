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

def save_quote(quote, csv_path="quote_scheduler/quotes.csv"):
    """Save the quote to CSV file."""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    new_quote = pd.DataFrame([{"Quote": quote, "Date": datetime.now().strftime("%Y-%m-%d")}])
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df = pd.concat([df, new_quote], ignore_index=True)
    else:
        df = new_quote
        
    df.to_csv(csv_path, index=False)

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
    # Convert 5:40 PM IST to system's local time
    ist = pytz.timezone('Asia/Kolkata')
    target_time = "17:40"
    
    schedule.every().day.at(target_time).do(generate_daily_quote)
    
    print(f"Scheduler started. Will generate quotes daily at {target_time} IST")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()