from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


from ai_parser import extract_tasks_with_ai
from storage import complete_tasks, restore_tasks, delete_tasks
from task_parser import extract_tasks
from ai_parser import extract_tasks_with_ai
from storage import (
    load_tasks,
    save_tasks,
    mark_task_completed,
    get_incomplete_tasks,
    get_completed_tasks,
    get_high_urgency_tasks,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BrainDumpRequest(BaseModel):
    text: str

class TaskBatchRequest(BaseModel):
    task_ids: list[str]

@app.get("/")
def root():
    return {"message": "FocusForge API running"}

@app.post("/tasks/parse")
def parse_tasks(request: BrainDumpRequest):
    ai_tasks = extract_tasks_with_ai(request.text)

    if ai_tasks:
        print("Using Gemini AI parser")
        new_tasks = ai_tasks
    else:
        print("Using fallback rule parser")
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

@app.patch("/tasks/complete")
def complete_multiple_tasks(request: TaskBatchRequest):
    updated_count = complete_tasks(request.task_ids)
    return {"message": f"Completed {updated_count} task(s)."}

@app.patch("/tasks/restore")
def restore_multiple_tasks(request: TaskBatchRequest):
    updated_count = restore_tasks(request.task_ids)
    return {"message": f"Restored {updated_count} task(s)."}

@app.delete("/tasks")
def delete_multiple_tasks(request: TaskBatchRequest):
    deleted_count = delete_tasks(request.task_ids)
    return {"message": f"Deleted {deleted_count} task(s)."}