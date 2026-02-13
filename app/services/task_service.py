from sqlalchemy.orm import Session
from db.models import Task

async def get_users_tasks(user_id: int, db: Session):
    tasks = db.query(Task).filter(Task.owner_id == user_id).all()
    return tasks

async def get_user_task_by_id(task_id: int, user_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id.id).first()
    return task