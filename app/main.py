from fastapi import FastAPI
from db.models import User, Task
from db.session import engine
from router import auth, tasks, admin, profile

app = FastAPI(title = "Task Manager API", description = "API for managing tasks", version = "1.0.0")

# Create database tables
User.metadata.create_all(bind=engine)
Task.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(admin.router)
app.include_router(profile.router)