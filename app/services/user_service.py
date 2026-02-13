from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models import User

async def get_user_by_email(email: str, db: Session):
    db_user = db.query(User).filter(User.email == email).first()
    
    return db_user