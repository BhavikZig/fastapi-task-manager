from fastapi import APIRouter, UploadFile, File, Depends
from typing import List
from db.models import User
from core.security import get_current_user
from sqlalchemy.orm import Session
from db.session import get_db
from uuid import uuid4
import os
import shutil

router = APIRouter(prefix="/me", tags=["Profile"])

UPLOAD_DIR = "./uploads"

@router.post("/upload-profile-image")
async def get_profile(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update DB
    current_user.profile_image = file_path
    db.add(current_user)
    db.commit()
    
    return {
        "message": "Profile image uploaded successfully",
        "profile_image": file_path
    }

@router.post("/multiple")
async def upload_multiple_profile(file: List[UploadFile] = File(...)):
    return {"fileNames": [file.filename for file in file], "message": "success"}