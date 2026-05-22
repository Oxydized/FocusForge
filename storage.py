import json
from pathlib import Path

TASKS_FILE = Path("tasks.json")

def save_tasks(tasks):
    """Saves parsed tasks to a JSON file."""

    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def load_tasks():
    """Loads tasks from the JSON file if it exists."""

    if not TASKS_FILE.exists():
        return[]
    
    with open(TASKS_FILE, "r") as file:
        return json.load(file)