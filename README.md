# Student Gmail Assistant

My HCDE 310 final project built as an interactive Flask app. It turns recent email messages into a student-focused action queue with category labels, urgency signals, explainable priority scores, suggested next actions, and quick inbox actions for live Gmail.

## What it does

- Pulls recent Gmail messages with the Gmail API when Google OAuth is configured and `Live Gmail` is selected.
- Falls back to a realistic demo inbox so the interface is still interactive during development, testing, and demos.
- Classifies emails into `academics`, `career`, `club logistics`, `finance`, `personal`, and `promotions`.
- Extracts future date and deadline language from email text.
- Computes a transparent priority score based on deadlines, known senders, action language, unread state, and message category.
- Lets the user analyze an inbox, then sort and filter the analyzed results from the UI by tag, sender familiarity, score range, search text, and sort order.
- Supports live Gmail actions including star/unstar, mark read/unread, trash, undo trash, opening the thread in Gmail, and loading more analyzed messages.

## Setup

Python `3.10+` is recommended. The app works on the current machine's Python `3.9.6`, but newer Python versions are a better fit for the Google libraries.

1. Install dependencies:

   ```bash
   python3 -m pip install --user -r requirements.txt
   ```

2. Copy the environment example:

   ```bash
   cp .env.example .env
   ```

3. Optional but recommended for live Gmail mode:
   Place your Google OAuth client file at `credentials.json`.

4. For Google OAuth, create a Google Cloud OAuth client and add both redirect URIs:
   - `http://127.0.0.1:5000/oauth2callback`
   - `http://localhost:5000/oauth2callback`

5. Start the app:

   ```bash
   python3 app.py
   ```

6. Open `http://127.0.0.1:5000`.

## Notes

- Without `credentials.json`, the app runs in demo mode only.
- Connecting Google does not automatically switch the source to live Gmail; choose `Demo data` or `Live Gmail` in the UI, then click `Analyze inbox`.
- OAuth tokens are stored in `instance/token.json` and excluded from git.
- The scoring and classification logic is in `student_gmail_assistant/email_analyzer.py`.
- The Google API integration is in `student_gmail_assistant/google_services.py`.
