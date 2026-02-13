from pydantic import BaseModel, EmailStr
from typing import List, Optional

class AdminUsersResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class AdminTasksResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    owner: AdminUsersResponse

    class Config:
        from_attributes = True

class AdminTasksListResponse(BaseModel):
    message: str
    data: List[AdminTasksResponse]

class TaskResponseForUser(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        from_attributes = True

class AdminUserWithTasksResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str
    tasks: List[TaskResponseForUser]

    class Config:
        from_attributes = True

class AdminUsersListResponse(BaseModel):
    message: str
    data: List[AdminUserWithTasksResponse]

class UpdateTaskDetails(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class UpdateUserDetails(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None