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
    
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return[]
    
def mark_task_completed(task_id):
    """Marks a task as completed by ID."""

    tasks = load_tasks()
    task_found = False

    for task in tasks:
        if "id" in task and task["id"].startswith(task_id):
            task["completed"] = True
            task_found = True
            break

    save_tasks(tasks)
    
    return task_found