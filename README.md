# Student Gmail Assistant

My HCDE 310 final project built as an interactive Flask app. It turns recent Gmail messages into a student-focused action queue with category labels, urgency signals, explainable priority scores, suggested next actions, and optional Google Calendar reminders.

## What it does

- Pulls recent Gmail messages with the Gmail API when Google OAuth is configured.
- Falls back to a realistic demo inbox so the interface is still interactive during development and demos.
- Classifies emails into `academics`, `career`, `club logistics`, `finance`, `personal`, and `promotions`.
- Extracts date and deadline language from email text.
- Computes a transparent priority score based on deadlines, known senders, action language, unread state, and user-selected category focus.
- Lets the user change scoring weights and search filters from the UI.
- Creates a Google Calendar reminder for an email when a date is detected and the user is connected to Google.

## Setup

Python `3.10+` is recommended. The app works on the current machine's Python `3.9.6`, but Google libraries emit deprecation warnings there.

1. Install dependencies:

   ```bash
   python3 -m pip install --user -r requirements.txt
   ```

2. Copy the environment example:

   ```bash
   cp .env.example .env
   ```

3. Optional but recommended for live Gmail and Calendar mode:
   Place your Google OAuth client file at `credentials.json`.

4. For Google OAuth, create a Google Cloud OAuth client and add both redirect URIs:
   - `http://127.0.0.1:5000/oauth2callback`
   - `http://localhost:5000/oauth2callback`

5. Start the Flask app:

   ```bash
   python3 -m flask --app app run --debug
   ```

6. Open `http://127.0.0.1:5000`.

## Notes

- Without `credentials.json`, the app runs in demo mode only.
- OAuth tokens are stored in `instance/token.json` and excluded from git.
- The scoring logic is in `student_gmail_assistant/email_analyzer.py`.
- The Google API integration is in `student_gmail_assistant/google_services.py`.
