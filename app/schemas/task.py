from pydantic import BaseModel
from typing import Optional

class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None