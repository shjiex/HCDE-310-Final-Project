import re
from datetime import datetime, timedelta
from email.utils import parseaddr

from dateparser.search import search_dates


CATEGORY_RULES = {
    "academics": [
        r"uw\.edu", r"washington\.edu", r"instructure", r"canvas",
        r"class", r"lecture", r"assignment", r"advising", r"office hours",
        r"hcde", r"graded", r"grade", r"course", r"quarter", r"scholarship",
        r"research symposium", r"honor society",
    ],
    "career": [
        r"recruit", r"interview", r"career", r"resume", r"linkedin",
        r"offer letter", r"internship", r"job", r"posted a role",
        r"handshake", r"joinhandshake", r"hiring",
    ],
    "club logistics": [r"club", r"meeting", r"rsvp", r"volunteer", r"officers@", r"chapter"],
    "finance": [r"bill", r"payment", r"tuition", r"invoice", r"fee", r"financial"],
    "personal": [r"family", r"friend", r"personal", r"birthday"],
    "promotions": [r"deal", r"sale", r"discount", r"newsletter", r"promo", r"unsubscribe"],
}

# Maps suggested actions to keyword patterns that trigger them.
# Order matters: first match wins. "save" is before "submit" so that
# Canvas "Submission Posted" notifications are not mistaken for tasks.
ACTION_RULES = {
    "reply": [r"reply", r"respond", r"rsvp", r"confirm", r"sign"],
    "attend": [r"schedule", r"time slot", r"availability", r"meeting", r"info session", r"join us"],
    "pay": [r"pay", r"payment", r"invoice", r"bill"],
    "save": [r"submission posted", r"grade changes", r"graded", r"grade", r"reference", r"notes", r"attached", r"for your records"],
    "submit": [r"form", r"survey", r"submit", r"registration", r"register", r"apply", r"deadline", r"application"],
    "ignore": [r"sale", r"discount", r"newsletter", r"promo", r"unsubscribe"],
}

KNOWN_SENDER_MARKERS = ["uw.edu", "washington.edu", "instructure.com", "billing", "advising", "recruiting"]


def analyze_messages(messages):
    analyzed = []
    now = datetime.now()

    for message in messages:
        text_blob = build_search_text(message)

        category = classify_category(text_blob)
        detected_dates = extract_dates(text_blob)
        suggested_action = detect_action(text_blob)
        score, reasons = calculate_score(message, category, suggested_action, detected_dates, now)

        raw_sender = message.get("sender", "")
        display_name, addr = parseaddr(raw_sender)
        sender_name = display_name or addr.split("@")[0] or raw_sender

        analyzed.append({
            **message,
            "sender_name": sender_name,
            "category": category,
            "detected_dates": [dt.isoformat() for dt in detected_dates[:2]],
            "detected_date_label": _format_date_label(detected_dates[0])
                if detected_dates else "No date detected",
            "suggested_action": suggested_action,
            "priority_score": min(score, 10),
            "urgency_reason": reasons[0] if reasons else "No urgent signals found.",
            "explanations": reasons,
        })

    return sorted(analyzed, key=lambda item: item["priority_score"], reverse=True)


def build_search_text(message):
    # Combine subject, sender, snippet, and body into one string for easier matching
    parts = [
        message.get("subject", ""),
        message.get("sender", ""),
        message.get("snippet", ""),
        strip_replies(message.get("body", "")),
    ]
    return " ".join(parts)


def strip_replies(text):
    # Remove common quoted reply patterns so old message text doesn't skew analysis
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Stop at "On [date] ... wrote:" reply headers
        if re.match(r"On .{10,100} wrote:?$", stripped):
            break
        # Stop at Outlook-style "From: / Sent: / To:" blocks
        if re.match(r"(From|Sent|To|Subject)\s*:", stripped):
            break
        # Stop at separator lines like "---- Original Message ----"
        if re.match(r"-{4,}", stripped) or re.match(r"_{4,}", stripped):
            break
        # Skip lines that are purely quoted (start with >)
        if stripped.startswith(">"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def calculate_score(message, category, suggested_action, detected_dates, now):
    score = 0
    reasons = []

    if category in ["academics", "career", "finance"]:
        score += 1
        reasons.append("important category")

    if is_known_sender(message.get("sender", "")):
        score += 2
        reasons.append("known sender")

    if detected_dates:
        next_date = detected_dates[0]
        days_until = max((next_date - now).days, 0)
        # Closer deadlines get a higher boost (max +3, min +1)
        score += max(3 - min(days_until, 3), 1)
        reasons.append(f"date: {next_date.strftime('%b %d')}")

    if suggested_action not in ["save", "ignore"]:
        score += 3
        reasons.append(f"needs {suggested_action}")

    if "UNREAD" in message.get("label_ids", []):
        score += 1
        reasons.append("unread")

    return score, reasons


def _match_rules(text, rules, default):
    lowered = text.lower()
    for key, patterns in rules.items():
        if any(re.search(p, lowered) for p in patterns):
            return key
    return default


def classify_category(text):
    return _match_rules(text, CATEGORY_RULES, "personal")


def detect_action(text):
    return _match_rules(text, ACTION_RULES, "save")


def is_known_sender(sender):
    lowered = sender.lower()
    return any(marker in lowered for marker in KNOWN_SENDER_MARKERS)


def _format_date_label(dt):
    if dt.hour == 0 and dt.minute == 0:
        return dt.strftime("%a, %b %d")
    return dt.strftime("%a, %b %d at %I:%M %p")


def extract_dates(text, now=None):
    if now is None:
        now = datetime.now()

    matches = search_dates(
        text,
        settings={
            "PREFER_DATES_FROM": "future",
            "RETURN_AS_TIMEZONE_AWARE": False,
            "RELATIVE_BASE": now,
        },
        languages=["en"],
    )
    if not matches:
        return []

    one_year_out = now.replace(year=now.year + 1)

    seen = set()
    cleaned = []
    tomorrow = (now + timedelta(days=1)).date()

    for _, date_value in matches:
        # Skip same-day times and past/far-future dates
        if date_value.date() < tomorrow or date_value > one_year_out:
            continue
        normalized = date_value.replace(second=0, microsecond=0)
        key = normalized.isoformat()
        if key not in seen:
            cleaned.append(normalized)
            seen.add(key)

    return sorted(cleaned)
