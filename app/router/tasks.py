from fastapi import APIRouter, Depends, HTTPException
from schemas.task import CreateTask
from db.session import get_db
from sqlalchemy.orm import Session
from db.models import Task, User
from core.security import get_current_user
from services.task_service import get_users_tasks, get_user_task_by_id

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("")
async def create_task(task: CreateTask, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = Task(title=task.title, description=task.description, owner_id=current_user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created successfully", "data": new_task}

@router.get("")
async def get_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = await get_users_tasks(user_id=current_user.id, db=db)

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    
    return {"message": "Tasks retrieved successfully", "data": tasks}

@router.get("/{task_id}")
async def get_task_details(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = await get_user_task_by_id(task_id=task_id, user_id=current_user, db=db)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task details retrieved successfully", "data": task}

@router.put("/{task_id}")
async def update_task(task_id: int, task_data: CreateTask, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = await get_user_task_by_id(task_id=task_id, user_id=current_user, db=db)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_data.title
    task.description = task_data.description
    db.commit()
    db.refresh(task)

    return {"message": "Task updated successfully", "data": task}

@router.patch("/{task_id}/complete")
async def mark_task_completed(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = await get_user_task_by_id(task_id=task_id, user_id=current_user, db=db)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = True
    db.commit()
    db.refresh(task)

    return {"message": "Task marked as completed successfully", "data": task}

@router.delete("/{task_id}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = await get_user_task_by_id(task_id=task_id, user_id=current_user, db=db)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}