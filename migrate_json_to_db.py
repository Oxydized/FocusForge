from database import SessionLocal
from storage import load_tasks
from crud import create_task, get_task_by_id

def migrate_json_to_db():
    """Migrates existing tasks from task.json into the database."""

    tasks = load_tasks()
    db = SessionLocal()

    migrated_count = 0
    skipped_count = 0

    try:
        for task in tasks:
            existing_task = get_task_by_id(db, task["id"])

            if existing_task:
                skipped_count += 1 
                continue

            create_task(db, task)
            migrated_count += 1

        print("Migration complete.")
        print(f"Migrated: {migrated_count}")
        print(f"Skipped duplicates: {skipped_count}")

    finally:
        db.close()

if __name__ == "__main__":
    migrate_json_to_db()