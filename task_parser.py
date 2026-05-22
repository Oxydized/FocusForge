import re

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
]

def extract_due_date(text):
    """Finds a simple due date keyword inside a task."""
    lower_text = text.lower()

    for keyword in DATE_KEYWORDS:
        if keyword in lower_text:
            return keyword
        
    return None

def clean_task_title(text, due_date):
    """Removes filler words and due date phrases from the task title."""
    cleaned = text.strip()

    # Remove common opening phraes
    cleaned = re.sub(r"^(i need to|i have to|need to|have to)\s+", "", cleaned, flags=re.IGNORECASE)

    # Remove due date keyword from the title
    if due_date:
        cleaned = re.sub(rf"\b(by|on|before)?\s*{re.escape(due_date)}\b", "", cleaned, flags=re.IGNORECASE)

    # Clean extra spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned.capitalize()

def extrac_tasks(brain_dump):
    """Converts a messy brain dump into structured task dictionaries."""

    # Turn common separators into commas
    normalized_text = brain_dump.replace(" and ", ",")

    # Split the brain dump into task chunks
    task_chunks = normalized_text.split(",")

    tasks = []

    for chunk in task_chunks:
        chunk = chunk.strip()

        if not chunk:
            continue

        due_date = extract_due_date(chunk)
        title = clean_task_title(chunk, due_date)

        task = {
            "title": title,
            "due_date": due_date,
            "urgency": "normal",
            "completed": False
        }

        tasks.append(task)
    
    return tasks