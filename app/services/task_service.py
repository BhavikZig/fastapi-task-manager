from sqlalchemy.orm import Session
from db.models import Task
from services.pagination import paginate
from typing import Optional

async def get_users_tasks(user_id: int, db: Session, page: int, limit: int, sort_by: Optional[str], order: Optional[str]):
    query = db.query(Task).filter(Task.owner_id == user_id)
    message = "Tasks retrieved successfully"
    tasks = paginate(query, page, limit, sort_by, order, message)
    return tasks

async def get_user_task_by_id(task_id: int, user_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id.id).first()
    return task