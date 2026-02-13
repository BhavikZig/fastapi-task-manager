from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    creaeted_at: datetime
    updated_at: datetime

class PaginatedTasks(BaseModel):
    message: str
    total: int
    page: int
    limit: int
    items: List[TaskResponse]