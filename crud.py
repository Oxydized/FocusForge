from sqlalchemy.orm import Session

from models import Task

def create_task(db: Session, task_data: dict):
    """Creates one task record in the database"""

    task = Task(**task_data)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_tasks(db: Session):
    """Returns all task records from the database."""

    return db.query(Task).all()

def delete_task(db: Session, task_id: str):
    """Deletes a task by ID."""

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return False
    
    db.delete(task)
    db.commit()

    return True

def delete_tasks_by_ids(db: Session, task_id: list[str]):
    """Deletes multiple task records by ID."""

    deleted_count = (
        db.query(Task)
        .filter(Task.id.in_(task_id))
        .delete(synchronize_session=False)
    )

    db.commit()

    return deleted_count

def get_task_by_id(db: Session, task_id: str):
    """Returns one task by ID."""

    return(
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

def update_task(db: Session, task_id: str, updated_fields: dict):
    """Updates one task record by ID using only provided fields."""

    task = get_task_by_id(db, task_id)

    if not task:
        return None
    
    for field, value in updated_fields.items():
        if hasattr(task, field):
            setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task

def set_tasks_completed_status(db: Session, task_ids: list[str], completed: bool):
    """Updates completed status for multiple tasks."""

    updated_count = (
        db.query(Task)
        .filter(Task.id.in_(task_ids))
        .update(
            {"completed": completed},
            synchronize_session=False
        )
    )

    db.commit()

    return updated_count