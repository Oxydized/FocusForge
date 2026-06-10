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