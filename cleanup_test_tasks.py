from database import SessionLocal
from models import Task

def cleanup_test_tasks():
    """Deletes old database test rows used during CRUD verification."""

    db = SessionLocal()

    try: 
        deleted_count = (
            db.query(Task)
            .filter(Task.title == "Test database task")
            .delete()
        )

        db.commit()

        print(f"Deleted test tasks: {deleted_count}")

    finally: 
        db.close()

if __name__ == "__main__":
    cleanup_test_tasks()