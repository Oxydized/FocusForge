from fastapi import FastAPI
from pydantic import BaseModel

from task_parser import extract_tasks
from storage import (
    load_tasks,
    save_tasks,
    mark_task_completed,
    get_incomplete_tasks,
    get_completed_tasks,
    get_high_urgency_tasks,
)

app = FastAPI()

class BrainDumpRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "FocusForge API running"}

@app.post("/tasks/parse")
def parse_tasks(request: BrainDumpRequest):
    new_tasks = extract_tasks(request.text)

    existing_tasks = load_tasks()
    all_tasks = existing_tasks + new_tasks

    save_tasks(all_tasks)

    return {
        "message": f"Saved {len(new_tasks)} new task(s).",
        "tasks": new_tasks,
        "total_tasks": len(all_tasks),
    }

@app.get("/tasks")
def get_tasks():
    return {"tasks": load_tasks()}

@app.get("/tasks/active")
def get_active_tasks():
    return {"tasks": get_incomplete_tasks()}

@app.get("/tasks/completed")
def get_completed_tasks_route():
    return {"tasks": get_completed_tasks()}

@app.get("/tasks/high-priority")
def get_high_priority_tasks():
    return {"tasks": get_high_urgency_tasks()}

@app.patch("/tasks/{task_id}/complete")
def complete_tasks(task_id: str):
    task_found = mark_task_completed(task_id)

    if task_found:
        return {"message": "Task marked as completed."}
    
    return {"message": "No matching task ID found."}