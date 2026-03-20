# Student Gmail Assistant

My HCDE 310 final project built as an interactive Flask app. It turns recent Gmail messages into a student-focused action queue with category labels, urgency signals, explainable priority scores, suggested next actions, and quick inbox actions for live Gmail.

## What it does

- Pulls recent Gmail messages with the Gmail API when Google OAuth is configured and `Live Gmail` is selected.
- Falls back to a realistic demo inbox so the interface is still interactive without a Google account.
- Classifies emails into `academics`, `career`, `club logistics`, `finance`, `personal`, and `promotions`.
- Extracts future date and deadline language from email text.
- Computes a transparent priority score based on deadlines, known senders, action language, unread state, and message category.
- Lets the user sort and filter analyzed results by tag, sender familiarity, score range, search text, and sort order.
- Supports live Gmail actions: star/unstar, mark read/unread, trash with undo, open thread in Gmail, and load more messages in batches.

## Setup

Python `3.10+` is recommended.

1. Install dependencies:

   ```bash
   python3 -m pip install --user -r requirements.txt
   ```

2. Copy the environment file and set a secret key:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and replace `FLASK_SECRET_KEY` with a random string.

3. **For graders:** `credentials.json` is provided as a Canvas submission comment — place it in the project root. Your `jeanpamn@uw.edu` and `sdg1@uw.edu1` accounts have already been added as test users, so no Google Cloud setup is needed. When signing in, Google may show a warning screen ("Google hasn't verified this app"); click **Continue** and grant the requested permissions to proceed.

4. Start the app:

   ```bash
   python3 app.py
   ```

5. Open `http://127.0.0.1:5000`.


## Notes

- Without `credentials.json`, the app runs in demo mode only and the Google sign-in button is hidden.
- Connecting Google does not automatically switch the source to live Gmail — choose `Demo data` or `Live Gmail` in the sidebar, then click `Analyze inbox`.
- OAuth tokens are saved to `instance/token.json` and excluded from git.
- Scoring and classification logic: `student_gmail_assistant/email_analyzer.py`
- Google API integration: `student_gmail_assistant/google_services.py`
- App factory and routes: `student_gmail_assistant/__init__.py`
