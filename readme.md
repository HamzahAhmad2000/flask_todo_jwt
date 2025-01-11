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
