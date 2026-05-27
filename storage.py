import json
import os
from pathlib import Path

TASKS_FILE = Path("tasks.json")

def ensure_tasks_file():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as file:
            json.dump([], file)

def save_tasks(tasks):
    """Saves parsed tasks to a JSON file."""

    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def load_tasks():
    ensure_tasks_file()
    """Loads tasks from the JSON file if it exists."""
    
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

def get_incomplete_tasks():
    return [task for task in load_tasks() if not task["completed"]]

def get_completed_tasks():
    return [task for task in load_tasks() if task["completed"]]

def get_high_urgency_tasks():
    return[
        task for task in load_tasks()
        if task["urgency"] == "high" and not task["completed"]
    ]

def complete_tasks(task_ids):
    tasks = load_tasks()
    updated_count = 0

    for task in tasks:
        if task.get("id") in task_ids:
            task["completed"] = True
            updated_count += 1

    save_tasks(tasks)
    return updated_count

def restore_tasks(task_ids):
    """Restores a completed task back to active."""

    tasks = load_tasks()
    updated_count = 0
    
    for task in tasks:
        if task.get("id") in task_ids:
            task["completed"] = False
            updated_count += 1

    save_tasks(tasks)
    return updated_count

def delete_tasks(task_ids):
    tasks = load_tasks()

    remaining_tasks = [
        task for task in tasks
        if task.get("id") not in task_ids
    ]

    deleted_count = len(tasks) - len(remaining_tasks)

    save_tasks(remaining_tasks)
    return deleted_count