import re
import uuid

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

def extract_tasks(brain_dump):
    """Converts a messy brain dump into structured task dictionaries."""
    
    normalized_text = brain_dump.lower()

    # Remove common opening phrase once at the beginning
    normalized_text = re.sub(r"^(i need to|i have to|need to|have to)\s+", "", normalized_text)

    # Normalize common separators
    normalized_text = normalized_text.replace(" and ", ",")
    normalized_text = normalized_text.replace(" . ", ",")
    normalized_text = normalized_text.replace(" ; ", ",")
    normalized_text = normalized_text.replace("\n", ",")

    # Split on "and" when it appears to introduce a new task
    normalized_text = re.sub(
        r"\s+and\s+(?=(i need to|need to|have to|finish|study|start|call|clean|schedule|pay|organize|buy|email|text|review|complete)\b)",
        ", ",
        normalized_text
    ) 

    # Split the brain dump into task chunks
    task_chunks = normalized_text.split(",")

    tasks = []

    for chunk in task_chunks:
        chunk = chunk.strip()

        if not chunk:
            continue

        due_date = extract_due_date(chunk)
        title = clean_task_title(chunk, due_date)

        urgency = determine_urgency(due_date)

        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "due_date": due_date,
            "urgency": determine_urgency(due_date),
            "completed": False
        }

        tasks.append(task)
    
    return tasks

def determine_urgency(due_date):
    """Assigns urgency based on the detected due date."""

    if due_date in ["today", "tonight"]:
        return "high"
    
    if due_date == "tomorrow":
        return "medium"
    
    if due_date in ["next week"]:
        return "low"
    
    if due_date:
        return "medium"
    
    return "normal"