from datetime import datetime, timedelta


def get_demo_messages():
    now = datetime.now()
    return [
        {
            "id": "demo-1",
            "thread_id": "demo-thread-1",
            "subject": "RSVP required by Friday for capstone showcase",
            "sender": "hcde-advising@uw.edu",
            "snippet": "Please RSVP by Friday at 5pm so we can finalize attendance.",
            "body": (
                "Hi Josh, please RSVP by Friday at 5pm for the capstone showcase. "
                "We need your response before the rooming list closes."
            ),
            "timestamp": (now - timedelta(hours=5)).isoformat(),
            "label_ids": ["INBOX", "UNREAD"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-1",
        },
        {
            "id": "demo-2",
            "thread_id": "demo-thread-2",
            "subject": "Interview availability for next Tuesday",
            "sender": "recruiting@bigtech.com",
            "snippet": "Send three time slots for next Tuesday.",
            "body": (
                "Thanks for applying. Please reply with three interview time slots for next "
                "Tuesday between 10am and 2pm."
            ),
            "timestamp": (now - timedelta(days=1)).isoformat(),
            "label_ids": ["INBOX"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-2",
        },
        {
            "id": "demo-3",
            "thread_id": "demo-thread-3",
            "subject": "Tuition payment reminder due March 28",
            "sender": "studentbilling@uw.edu",
            "snippet": "Your spring tuition payment is due March 28.",
            "body": (
                "This is a reminder that your spring tuition payment is due March 28. "
                "Please pay online to avoid a late fee."
            ),
            "timestamp": (now - timedelta(days=2)).isoformat(),
            "label_ids": ["INBOX", "IMPORTANT"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-3",
        },
        {
            "id": "demo-4",
            "thread_id": "demo-thread-4",
            "subject": "Club meeting moved to tomorrow at 6:30pm",
            "sender": "officers@dubhacks.club",
            "snippet": "The design meeting is tomorrow at 6:30pm in Sieg Hall.",
            "body": (
                "Reminder: the design meeting is tomorrow at 6:30pm in Sieg Hall. "
                "Please review the agenda beforehand."
            ),
            "timestamp": (now - timedelta(days=3)).isoformat(),
            "label_ids": ["INBOX", "UNREAD"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-4",
        },
        {
            "id": "demo-5",
            "thread_id": "demo-thread-5",
            "subject": "Your weekly deals are here",
            "sender": "news@store.example",
            "snippet": "Up to 60% off select items this week.",
            "body": "Browse this week's deals and save big on electronics and home goods.",
            "timestamp": (now - timedelta(days=1, hours=4)).isoformat(),
            "label_ids": ["INBOX", "CATEGORY_PROMOTIONS"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-5",
        },
        {
            "id": "demo-6",
            "thread_id": "demo-thread-6",
            "subject": "Reference material from INFO 340",
            "sender": "classmates@uw.edu",
            "snippet": "Sharing notes from today’s lecture.",
            "body": "Attached are the notes from today. No action needed, just saving for reference.",
            "timestamp": (now - timedelta(days=4)).isoformat(),
            "label_ids": ["INBOX"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-6",
        },
        {
            "id": "demo-7",
            "thread_id": "demo-thread-7",
            "subject": "Grade posted for HCDE 310 Homework 5",
            "sender": "canvas@uw.edu",
            "snippet": "Your submission has been graded. View feedback in Canvas.",
            "body": "Your grade for Homework 5 has been posted. Log in to Canvas to view your score and instructor feedback.",
            "timestamp": (now - timedelta(hours=10)).isoformat(),
            "label_ids": ["INBOX", "UNREAD"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-7",
        },
        {
            "id": "demo-8",
            "thread_id": "demo-thread-8",
            "subject": "Internship offer letter — please sign by April 2",
            "sender": "hr@bigtech.com",
            "snippet": "Please review and sign your offer letter by April 2.",
            "body": (
                "Congratulations! Attached is your internship offer letter. "
                "Please review, sign, and return it by April 2 to secure your position."
            ),
            "timestamp": (now - timedelta(days=1, hours=2)).isoformat(),
            "label_ids": ["INBOX", "UNREAD", "IMPORTANT"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-8",
        },
        {
            "id": "demo-9",
            "thread_id": "demo-thread-9",
            "subject": "CSE 473 final project groups due Friday",
            "sender": "cse473-staff@uw.edu",
            "snippet": "Submit your project group preferences by this Friday at noon.",
            "body": (
                "Please submit your final project group preferences via the form linked below "
                "by Friday at noon. Groups of 3–4 are required."
            ),
            "timestamp": (now - timedelta(days=2, hours=1)).isoformat(),
            "label_ids": ["INBOX", "UNREAD"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-9",
        },
        {
            "id": "demo-10",
            "thread_id": "demo-thread-10",
            "subject": "Your Amazon order has shipped",
            "sender": "shipment-tracking@amazon.com",
            "snippet": "Your package will arrive by Thursday.",
            "body": "Your order #112-8834521 has shipped and is estimated to arrive by Thursday.",
            "timestamp": (now - timedelta(hours=18)).isoformat(),
            "label_ids": ["INBOX"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-10",
        },
        {
            "id": "demo-11",
            "thread_id": "demo-thread-11",
            "subject": "Advising appointment confirmation — March 25 at 2pm",
            "sender": "advising@uw.edu",
            "snippet": "Your advising appointment is confirmed for March 25 at 2pm.",
            "body": (
                "This confirms your advising appointment on March 25 at 2:00pm with your advisor. "
                "Please come prepared with your course plan."
            ),
            "timestamp": (now - timedelta(days=3, hours=5)).isoformat(),
            "label_ids": ["INBOX"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-11",
        },
        {
            "id": "demo-12",
            "thread_id": "demo-thread-12",
            "subject": "Roommate looking for subletter June–August",
            "sender": "student-housing@uw.edu",
            "snippet": "Looking for someone to sublet a room near campus this summer.",
            "body": "A fellow student is looking for a subletter for their room near the Ave from June through August. Contact them directly if interested.",
            "timestamp": (now - timedelta(days=5)).isoformat(),
            "label_ids": ["INBOX"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-12",
        },
        {
            "id": "demo-13",
            "thread_id": "demo-thread-13",
            "subject": "Overdue library book — please return or renew",
            "sender": "libraries@uw.edu",
            "snippet": "You have an overdue item. Fees may apply.",
            "body": (
                "Our records show you have an overdue library item: ‘Designing with Data’. "
                "Please return or renew it online to avoid additional fees."
            ),
            "timestamp": (now - timedelta(days=1, hours=6)).isoformat(),
            "label_ids": ["INBOX", "UNREAD"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-13",
        },
        {
            "id": "demo-14",
            "thread_id": "demo-thread-14",
            "subject": "Study abroad info session — April 4 at 5pm",
            "sender": "studyabroad@uw.edu",
            "snippet": "Join us to learn about UW exchange programs for 2025–26.",
            "body": (
                "Interested in studying abroad? Join our info session on April 4 at 5pm in the HUB. "
                "Learn about exchange programs, deadlines, and scholarships."
            ),
            "timestamp": (now - timedelta(days=2, hours=3)).isoformat(),
            "label_ids": ["INBOX"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-14",
        },
        {
            "id": "demo-15",
            "thread_id": "demo-thread-15",
            "subject": "Midterm feedback — please complete by March 22",
            "sender": "hcde310-instructor@uw.edu",
            "snippet": "Please fill out the midterm feedback survey by March 22.",
            "body": (
                "We’d like your feedback on how the course is going. "
                "Please complete the midterm survey by March 22 — it only takes 5 minutes."
            ),
            "timestamp": (now - timedelta(days=4, hours=2)).isoformat(),
            "label_ids": ["INBOX", "UNREAD"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-15",
        },
        {
            "id": "demo-16",
            "thread_id": "demo-thread-16",
            "subject": "LinkedIn: 5 new job matches for you",
            "sender": "jobs-noreply@linkedin.com",
            "snippet": "New UX and software roles matching your profile.",
            "body": "Based on your profile, we found 5 new job postings that may interest you. View them before they close.",
            "timestamp": (now - timedelta(days=1, hours=8)).isoformat(),
            "label_ids": ["INBOX"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-16",
        },
        {
            "id": "demo-17",
            "thread_id": "demo-thread-17",
            "subject": "Health insurance enrollment closes March 31",
            "sender": "benefits@uw.edu",
            "snippet": "Enroll in or waive student health insurance before March 31.",
            "body": (
                "Reminder: the student health insurance enrollment window closes March 31. "
                "Log in to MyUW to enroll or submit a waiver."
            ),
            "timestamp": (now - timedelta(days=3)).isoformat(),
            "label_ids": ["INBOX", "UNREAD", "IMPORTANT"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-17",
        },
        {
            "id": "demo-18",
            "thread_id": "demo-thread-18",
            "subject": "Peer review assigned for HCDE 310 Project 3",
            "sender": "canvas@uw.edu",
            "snippet": "You have been assigned two peer reviews due March 24.",
            "body": (
                "You have been assigned two peer reviews for Project 3. "
                "Please complete them in Canvas by March 24 at 11:59pm."
            ),
            "timestamp": (now - timedelta(hours=14)).isoformat(),
            "label_ids": ["INBOX", "UNREAD"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-18",
        },
        {
            "id": "demo-19",
            "thread_id": "demo-thread-19",
            "subject": "Campus food pantry — open Tuesdays and Thursdays",
            "sender": "basicneeds@uw.edu",
            "snippet": "The UW food pantry is open this week.",
            "body": "The UW Basic Needs food pantry is open Tuesdays and Thursdays from 11am–3pm in the HUB. No ID required.",
            "timestamp": (now - timedelta(days=6)).isoformat(),
            "label_ids": ["INBOX"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-19",
        },
        {
            "id": "demo-20",
            "thread_id": "demo-thread-20",
            "subject": "Coding interview prep — session this Saturday at 1pm",
            "sender": "officers@dubhacks.club",
            "snippet": "Join us Saturday at 1pm for mock interviews and whiteboarding practice.",
            "body": (
                "DubHacks is hosting a coding interview prep session this Saturday at 1pm in CSE 203. "
                "Practice whiteboarding and get feedback from alumni interviewers."
            ),
            "timestamp": (now - timedelta(days=2, hours=7)).isoformat(),
            "label_ids": ["INBOX", "UNREAD"],
            "thread_url": "https://mail.google.com/mail/u/0/#inbox/demo-thread-20",
        },
    ]
