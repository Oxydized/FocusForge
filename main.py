import os
import models

from database import Base, engine, SessionLocal
from crud import create_task, get_task_by_id, update_task as update_db_task, delete_tasks_by_ids, set_tasks_completed_status
from fastapi import FastAPI
from pydantic import BaseModel
from storage import update_task
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

Base.metadata.create_all(bind=engine)

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

class TaskUpdateRequest(BaseModel):
    """
    Request body for editing an existing task.
    All fields are optional because the user may only edit one field
    """

    title: str | None = None
    due_date: str | None = None

@app.get("/")
def root():
    return {"message": "FocusForge API running"}

@app.post("/tasks/parse")
def parse_tasks(request: BrainDumpRequest):
    ai_tasks = extract_tasks_with_ai(request.text)

    if ai_tasks:
        provider = os.getenv("AI_PROVIDER", "unknown")
        print(f"Using {provider} AI parser")
        new_tasks = ai_tasks
    else:
        print("Using fallback rule parser")
        new_tasks = extract_tasks(request.text)

    existing_tasks = load_tasks()
    all_tasks = existing_tasks + new_tasks

    save_tasks(all_tasks)

    db = SessionLocal()

    try:
        for task in new_tasks:
            existing_tasks = get_task_by_id(db, task["id"])

            if existing_tasks:
                continue

            create_task(db, task)

    finally:
        db.close()

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

    db = SessionLocal()

    try:
        set_tasks_completed_status(db, request.task_ids, True)

    finally:
        db.close()

    return {"message": f"Completed {updated_count} task(s)."}

@app.patch("/tasks/restore")
def restore_multiple_tasks(request: TaskBatchRequest):
    updated_count = restore_tasks(request.task_ids)

    db = SessionLocal()

    try:
        set_tasks_completed_status(db, request.task_ids, False)

    finally:
        db.close()

    return {"message": f"Restored {updated_count} task(s)."}

@app.delete("/tasks")
def delete_multiple_tasks(request: TaskBatchRequest):
    deleted_count = delete_tasks(request.task_ids)

    db = SessionLocal()

    try:
        delete_tasks_by_ids(db, request.task_ids)

    finally:
        db.close()

    return {"message": f"Deleted {deleted_count} task(s)."}

@app.patch("/tasks/{task_id}")
def update_single_task(task_id: str, request: TaskUpdateRequest):
    """
    Updates a task. 
    This endpoint supports editing task details after AI parsing
    """

    updated_fields = request.model_dump(exclude_none=True)

    # First update the JSON storage
    updated_task = update_task(
        task_id,
        updated_fields
    )

    if updated_task: 
        db = SessionLocal()

        try:
            # Then mirror the same updated task in SQLite
            update_db_task(db, task_id, updated_task)

        finally:
            db.close()

        return {
            "message": "Task updated successfully.",
            "task": updated_task
        }
    
    return {"message": "No matching task ID found."}

