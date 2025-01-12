# Flask To-Do Application (JWT Auth)

This repository contains a simple Flask-based To-Do application with JWT-based user authentication. 
Users can register, log in, and manage their tasks. The focus is on **backend** functionality only, 
so there is no frontend implementation.

## Features

1. **User Registration**  
   - Validates password complexity: 
     - At least 8 characters
     - At least one uppercase letter
     - At least one lowercase letter
     - At least one number
     - At least one special character

2. **User Login**  
   - Returns a JWT token upon successful login.

3. **JWT-Protected Endpoints**  
   - All task management routes (Add, Edit, Delete, Mark Done, and View Tasks) 
     require a valid JWT token in the `Authorization` header as a Bearer token.

4. **Task Management**  
   - **Add Task**: Create a task with title and optional description.  
   - **Edit Task**: Update the title and/or description.  
   - **Delete Task**: Remove a task permanently.  
   - **Mark as Done**: Mark a task as completed.  
   - **View Tasks**: View all tasks for the current user.  

## Getting Started

### 1. Clone or Download the Repository

```bash
git clone https://github.com/yourusername/flask_todo_jwt.git
cd flask_todo_jwt



### 2. API Endpoints Usage

Use a REST client (cURL) to interact with the following endpoints. Below are example cURL commands tailored for PowerShell.

## Prerequisites

- **Flask Application Running**: Ensure your Flask application is running at `http://127.0.0.1:5000`.
- **PowerShell Environment**: The commands are optimized for PowerShell on Windows.
- **JWT Token**: Obtain a JWT token by registering and logging in before accessing protected routes.

---

## 1. Register a New User

**Endpoint**: `POST /auth/register`  
**Description**: Creates a new user account.

### cURL Command:
```powershell
curl.exe -X POST http://127.0.0.1:5000/auth/register `
  -H "Content-Type: application/json" `
  --data '{ "username": "yourUsername", "password": "P@ssw0rdExample" }'
```

### Example:
```powershell
curl.exe -X POST http://127.0.0.1:5000/auth/register `
  -H "Content-Type: application/json" `
  --data '{ "username": "john_doe", "password": "SecureP@ssw0rd" }'
```

### Expected Response:
```json
{
  "message": "User registered successfully"
}
```

---

## 2. Login to Obtain JWT Token

**Endpoint**: `POST /auth/login`  
**Description**: Authenticates a user and returns a JWT token for authorized access to protected routes.

### cURL Command:
```powershell
curl.exe -X POST http://127.0.0.1:5000/auth/login `
  -H "Content-Type: application/json" `
  --data '{ "username": "yourUsername", "password": "P@ssw0rdExample" }'
```

### Example:
```powershell
curl.exe -X POST http://127.0.0.1:5000/auth/login `
  -H "Content-Type: application/json" `
  --data '{ "username": "john_doe", "password": "SecureP@ssw0rd" }'
```

### Expected Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Set the JWT Token in PowerShell**:
```powershell
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```
Replace the ellipsis (...) with your actual token string.

---

## 3. Add a New Task

**Endpoint**: `POST /tasks/`  
**Description**: Creates a new task for the authenticated user.

### cURL Command:
```powershell
curl.exe -X POST http://127.0.0.1:5000/tasks/ `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  --data '{ "title": "Buy groceries", "description": "Milk, Bread, Eggs" }'
```

### Expected Response:
```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, Bread, Eggs"
  }
}
```

---

## 4. View All Tasks

**Endpoint**: `GET /tasks/`  
**Description**: Retrieves all tasks associated with the authenticated user.

### cURL Command:
```powershell
curl.exe -X GET http://127.0.0.1:5000/tasks/ `
  -H "Authorization: Bearer $token"
```

### Expected Response:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, Bread, Eggs",
      "is_done": false,
      "created_at": "2025-01-11 12:00:00"
    }
  ]
}
```

---

## 5. Update an Existing Task

**Endpoint**: `PUT /tasks/<task_id>`  
**Description**: Updates the title and/or description of a specific task.  

### Parameters:
- `<task_id>`: The ID of the task to update (e.g., `1`).

### cURL Command:
```powershell
curl.exe -X PUT http://127.0.0.1:5000/tasks/<task_id> `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  --data '{ "title": "Buy groceries and fruits", "description": "Milk, Bread, Eggs, Apples" }'
```

### Expected Response:
```json
{
  "message": "Task updated successfully",
  "task": {
    "id": 1,
    "title": "Buy groceries and fruits",
    "description": "Milk, Bread, Eggs, Apples",
    "is_done": false
  }
}
```

---

## 6. Delete a Task

**Endpoint**: `DELETE /tasks/<task_id>`  
**Description**: Removes a specific task from the user's task list.

### Parameters:
- `<task_id>`: The ID of the task to delete (e.g., `1`).

### cURL Command:
```powershell
curl.exe -X DELETE http://127.0.0.1:5000/tasks/<task_id> `
  -H "Authorization: Bearer $token"
```

### Expected Response:
```json
{
  "message": "Task deleted successfully"
}
```

---

## 7. Mark a Task as Done

**Endpoint**: `PATCH /tasks/<task_id>/done`  
**Description**: Marks a specific task as completed.

### Parameters:
- `<task_id>`: The ID of the task to mark as done (e.g., `1`).

### cURL Command:
```powershell
curl.exe -X PATCH http://127.0.0.1:5000/tasks/<task_id>/done `
  -H "Authorization: Bearer $token"
```

### Expected Response:
```json
{
  "message": "Task marked as done",
  "task": {
    "id": 1,
    "title": "Buy groceries and fruits",
    "description": "Milk, Bread, Eggs, Apples",
    "is_done": true
  }
}
```
```