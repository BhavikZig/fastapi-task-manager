# Task Manager API

A comprehensive RESTful API for managing tasks with user authentication, role-based access control, and profile management built with FastAPI and PostgreSQL.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Task Management**: Create, read, update, and delete tasks
- **User Profiles**: Manage user profiles with profile images
- **Role-Based Access Control**: Support for different user roles (user, admin)
- **Database Migrations**: Alembic for database schema versioning
- **File Upload**: Support for uploading profile images
- **Logging**: Comprehensive logging system

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd task_manager
```

### 2. Create and Activate Virtual Environment

```bash
# Using venv
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add the following:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/task_manager
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Set Up the Database

```bash
# Run migrations
alembic upgrade head
```

## Running the Application

### Development Server

```bash
cd app
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Access API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure

```
task_manager/
├── app/
│   ├── alembic/              # Database migrations
│   │   └── versions/
│   ├── core/                 # Core configuration
│   │   ├── config.py         # Settings and environment variables
│   │   ├── logger.py         # Logging configuration
│   │   └── security.py       # Security utilities
│   ├── db/                   # Database layer
│   │   ├── base.py           # SQLAlchemy base
│   │   ├── models.py         # Database models
│   │   └── session.py        # Database session
│   ├── router/               # API routes
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── tasks.py          # Task management endpoints
│   │   ├── admin.py          # Admin endpoints
│   │   └── profile.py        # User profile endpoints
│   ├── schemas/              # Pydantic models
│   │   ├── user.py           # User schemas
│   │   ├── task.py           # Task schemas
│   │   └── admin.py          # Admin schemas
│   ├── services/             # Business logic
│   │   ├── user_service.py   # User management logic
│   │   └── task_service.py   # Task management logic
│   ├── uploads/              # Uploaded files
│   ├── main.py               # Application entry point
│   └── alembic.ini           # Alembic configuration
├── env/                      # Virtual environment
└── README.md                 # This file
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Tasks
- `GET /tasks/` - List all tasks for the current user
- `POST /tasks/` - Create a new task
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task

### User Profile
- `GET /profile/` - Get current user profile
- `PUT /profile/` - Update current user profile
- `POST /profile/upload-image` - Upload profile image

### Admin
- `GET /admin/users` - List all users (admin only)
- `GET /admin/users/{id}` - Get user details (admin only)
- `PUT /admin/users/{id}` - Update user role (admin only)

## Database Models

### User Model
- `id`: Primary key
- `email`: Unique user email
- `hashed_password`: Encrypted password
- `is_active`: User status
- `role`: User role (user/admin)
- `profile_image`: Path to profile image
- `created_at`: User creation timestamp
- `updated_at`: Last update timestamp

### Task Model
- `id`: Primary key
- `title`: Task title
- `description`: Task description
- `completed`: Completion status
- `owner_id`: Foreign key to User
- `created_at`: Task creation timestamp
- `updated_at`: Last update timestamp

## Database Migrations

### Run Migrations
```bash
cd app
alembic upgrade head
```

### Create New Migration
```bash
cd app
alembic revision --autogenerate -m "migration description"
```

### View Migration History
```bash
cd app
alembic history
```

## Development

### Running Tests

```bash
pytest
```

### Linting

```bash
flake8 app/
black app/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 1.0.0
- Initial release
- User authentication with JWT
- Task management CRUD operations
- User profile management
- Admin features
- Database migrations with Alembic
