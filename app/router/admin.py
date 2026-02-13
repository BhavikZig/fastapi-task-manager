from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.session import get_db
from core.security import get_current_user, hash_password
from db.models import User, Task
from schemas.admin import AdminTasksListResponse, AdminUsersListResponse, UpdateTaskDetails, UpdateUserDetails
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=AdminUsersListResponse)
async def get_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if (current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    users = db.query(User).options(joinedload(User.tasks)).all()

    if not users:
        return {"message": "No users found", "data": []}
    
    return {"message": "Users retrieved successfully", "data": users}

@router.get("/tasks", response_model=AdminTasksListResponse)
async def get_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if (current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    tasks = db.query(Task).options(joinedload(Task.owner)).all()

    if not tasks:
        return {"message": "No tasks found", "data": []}
    
    return {"message": "Tasks retrieved successfully", "data": tasks}

@router.patch("/users/{user_id}/password")
async def update_user_password(user_id: int, new_password: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if (current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)

    return {"message": "User password updated successfully", "user": user}

@router.put("/tasks/{task_id}")
async def update_task_details(task_id: int, task_data: UpdateTaskDetails, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if (current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    task = db.query(Task).get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
        
    db.commit()
    db.refresh(task)

    return {"message": "Task details updated successfully", "task": task}

@router.put("/user/{user_id}")
async def update_user_details(user_id: int, user_data: UpdateUserDetails, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if (current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.role is not None:
        user.role = user_data.role
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
        
    db.commit()
    db.refresh(user)

    return {"message": "User details updated successfully", "user": user}