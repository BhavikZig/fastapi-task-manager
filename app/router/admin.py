from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from db.session import get_db
from core.security import get_current_user, hash_password
from db.models import User, Task
from schemas.admin import UpdateTaskDetails, UpdateUserDetails, PaginatedTasks, PaginatedUsers
from typing import List
from services.pagination import paginate

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=PaginatedUsers)
async def get_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), page: int = Query(1, ge=1, description="Page number"), limit: int = Query(10, ge=1, description="Number of users per page"), sort_by: str = Query("creaeted_at", description="Field to sort by"), order: str = Query("desc", regex="^(asc|desc)$", description="Order of users (asc or desc)")):
    if (current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # users = db.query(User).options(joinedload(User.tasks)).all()
    query = db.query(User).options(joinedload(User.tasks))

    message = "Users retrieved successfully"

    users = paginate(query, page, limit, sort_by, order, message)

    if not users:
        return {"message": "No users found", "items": []}
    
    # return {"message": "Users retrieved successfully", "data": users}
    return users

@router.get("/tasks", response_model=PaginatedTasks)
async def get_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), page: int = Query(1, ge=1, decription="Page number"), limit: int = Query(10, ge=1, description="Number of tasks per page"),sort_by: str = Query("creaeted_at", description="Field to sort by"), order: str = Query("desc", regex="^(asc|desc)$", description="Order of tasks (asc or desc)")):
    if (current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # tasks = db.query(Task).options(joinedload(Task.owner)).all()
    query = db.query(Task).options(joinedload(Task.owner))

    message = "Tasks retrieved successfully"

    tasks = paginate(query, page, limit, sort_by, order, message)

    if not tasks:
        return {"message": "No tasks found", "data": []}
    
    # return {"message": "Tasks retrieved successfully", "data": tasks}
    return tasks

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