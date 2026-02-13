from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate
from db.session import get_db
from sqlalchemy.orm import Session
from db.models import User
from core.security import hash_password, verify_password, create_access_token
from services.user_service import get_user_by_email
from core.logger import logger

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = await get_user_by_email(user.email, db)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(email=user.email, hashed_password=hash_password(user.password), role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user": new_user}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info("Login endpoint called")
    db_user = await get_user_by_email(form_data.username, db)

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    token  = create_access_token(data = {"sub": db_user.email})

    return {"message": "User logged in successfully", "access_token": token, "token_type": "bearer"}