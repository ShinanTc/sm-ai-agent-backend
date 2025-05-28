# Instagram Content Automation

### TECH STACK USED:

Programming Language: Python 🐍  
Image Processing: Pillow (PIL) 🎨  
Data Handling: Pandas 📊  
Font Management: Custom TTF Font (Bricolage Grotesque) 🎨  
Scheduling: Schedule library 📅

---

## HOW TO RUN?

### 1. Create and Activate a Virtual Environment
```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate on macOS/Linux
venv\Scripts\activate  # Activate on Windows
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
pip install -r quote_scheduler/requirements.txt
```

### 3. Start the FastAPI Server
```bash
uvicorn app.main:app --reload
```

### 4. Run the Quote Scheduler
```bash
python quote_scheduler/scheduler.py
```

## Features

### 1. Quote Generation API
- Generate motivational quotes using Gemini AI
- Support for different templates based on the day
- Image processing with proper text wrapping
- API endpoints for template management and carousel generation

### 2. Automated Quote Scheduler
- Runs daily at 5:40 PM IST
- Automatically selects templates based on the day:
  - Monday: Uses "Freaking Monday" template
  - Friday: Uses "Weekend Mode" template
  - Other days: Uses generic template
- Ensures quote uniqueness by maintaining a history
- Generates and saves quotes with proper formatting

### 3. Carousel Generation
- Support for multi-slide carousel posts
- Custom background colors (green/yellow)
- Proper text formatting and positioning

## Project Structure

```
├── app/                    # FastAPI application
├── generators/             # Quote and carousel generation scripts
├── quote_scheduler/        # Automated scheduling system
│   ├── scheduler.py       # Main scheduler script
│   ├── requirements.txt   # Scheduler-specific dependencies
│   └── quotes.csv         # Quote history database
├── templates/             # Image templates
└── assets/               # Fonts and other assets
```

## Configuration

### Quote Scheduler
- Runs daily at 5:40 PM IST
- Maintains quote history in `quote_scheduler/quotes.csv`
- Automatically selects appropriate templates
- Prevents duplicate quotes

### Templates
- `freakin-monday.png`: Used for Monday posts
- `weekend-mode.png`: Used for Friday/weekend posts
- `generic.png`: Used for other days
- Carousel templates in both green and yellow variants

## Development Notes

1. **Adding New Templates**
   - Place templates in `templates/motivation-quotes/`
   - Update `template_map` in `generate_quotes_content.py`

2. **Modifying Schedule**
   - Edit the time in `quote_scheduler/scheduler.py`
   - Default: 5:40 PM IST

3. **Quote Generation**
   - Uses Gemini AI API
   - Requires API key in `.env` file
   - Ensures uniqueness through CSV history

4. **Instagram Integration**
   - TODO: Add Instagram posting logic in scheduler
   - Current version generates images locally

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Future Improvements

- [ ] Add Instagram API integration
- [ ] Implement retry mechanism for failed generations
- [ ] Add monitoring and notifications
- [ ] Create admin dashboard for quote management
- [ ] Add support for multiple social media platforms

Happy Generating! 🚀# sm-ai-agent-v2.0
