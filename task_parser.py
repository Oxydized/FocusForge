import re
import uuid
import dateparser

from datetime import datetime

DATE_KEYWORDS = [
    "today",
    "tomorrow",
    "tonight",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "next week",
    "next month",
    "this weekend",
    "before",
]

RELATIVE_DATE_PATTERNS = [
    r"in \d+ days",
    r"in \d+ weeks",
    r"in \d+ months",
    r"in one day",
    r"in two days",
    r"in one week",
    r"in two weeks",
    r"in one month",
    r"in two months",
]

TASK_STARTERS = (
    "i need to|need to|have to|i should|should|remember to|"
    "don'?t forget to|don’t forget to|finish|study|start|call|"
    "clean|schedule|pay|organize|buy|email|text|review|complete|"
    "submit|reorganize|practice|prepare|write|read|apply|fix|"
    "update|make|create|plan|follow up|send"
)

OPENING_PHRASES = (
    "i need to|i have to|need to|have to|i should|should|"
    "remember to|don'?t forget to|don’t forget to"
)


def extract_due_date(text):
    """Finds a simple due date keyword inside a task."""
    lower_text = text.lower()

    for pattern in RELATIVE_DATE_PATTERNS:
        match = re.search(pattern, lower_text)

        if match:
            return match.group(0)
        
    for keyword in DATE_KEYWORDS:
        if keyword in lower_text:
            return keyword
    
    return None


def clean_task_title(text, due_date):
    """Removes filler words and due date phrases from the task title."""
    cleaned = text.strip()

    cleaned = re.sub(
        rf"^({OPENING_PHRASES})\s+",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    if due_date:
        cleaned = re.sub(
            rf"\b(by|on|before)?\s*{re.escape(due_date)}\b",
            "",
            cleaned,
            flags=re.IGNORECASE
        )

    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned.capitalize()


def extract_tasks(brain_dump):
    """Converts a messy brain dump into structured task dictionaries."""

    normalized_text = brain_dump.lower()

    normalized_text = re.sub(
        rf"^({OPENING_PHRASES})\s+",
        "",
        normalized_text
    )

    normalized_text = normalized_text.replace(".", ",")
    normalized_text = normalized_text.replace(";", ",")
    normalized_text = normalized_text.replace("\n", ",")

    # Split on "and" only when the following phrase looks like a new task.
    normalized_text = re.sub(
        rf"\s+and\s+(?=({TASK_STARTERS})\b)",
        ", ",
        normalized_text
    )

    task_chunks = normalized_text.split(",")

    tasks = []

    for chunk in task_chunks:
        chunk = chunk.strip()

        if not chunk:
            continue

        due_date = extract_due_date(chunk)
        title = clean_task_title(chunk, due_date)

        if not title:
            continue

        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "due_date": due_date,
            "due_date_resolved": resolve_due_date(due_date),
            "urgency": determine_urgency(due_date),
            "completed": False
        }

        tasks.append(task)

    return tasks


def determine_urgency(due_date):
    """Assigns urgency based on the detected due date."""

    if not due_date:
        return "normal"

    due_date = due_date.lower().strip()

    if due_date in ["today", "tonight"]:
        return "high"

    if due_date in [
        "tomorrow",
        "tomorrow morning",
        "tomorrow afternoon",
        "tomorrow night",
    ]:
        return "medium"

    if due_date in [
        "this weekend",
        "next week",
        "next month"
    ]:
        return "low"

    return "medium"

def resolve_due_date(due_date_text):
    """Converts a natural-language due date into ISO date string when possible."""

    if not due_date_text:
        return None
    
    parsed_date = dateparser.parse(
        due_date_text,
        settings={
            "PREFER_DATES_FROM": "future"
        }
    )

    if not parsed_date:
        return None
    
    return parsed_date.date().isoformat()