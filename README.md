
# Textbook Summarizer & Question Predictor (Demo)

## What this is
A simple demo web app (Flask) that summarizes pasted textbook text and attempts to generate questions using Hugging Face transformer models.

## Setup (Linux / Mac / Windows WSL)
1. Clone or unzip project.
2. Create a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   python app.py
   ```
5. Open http://127.0.0.1:5000 in your browser.

## Notes & Tips
- Models like `facebook/bart-large-cnn` are large and require memory and disk space. If you have limited resources, replace with smaller models such as `sshleifer/distilbart-cnn-12-6` and `t5-small`.
- For long textbooks, chunk the input and summarize per chunk, then optionally summarize the summaries.
- This repo is a demo scaffold. For production, add file uploads, authentication, background jobs (Celery/RQ), and a DB to store results.

## Files
- `app.py` — Flask routes
- `models/ai_model.py` — model pipelines
- `templates/` — HTML templates
- `static/` — CSS

## License
MIT
