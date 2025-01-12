import pytest
from app import create_app, db
from app.models import User, Task

@pytest.fixture
def client():
    """
    Pytest fixture to create a new Flask test client per test session.
    It uses an in-memory SQLite database for testing.
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_registration(client):
    """
    Test user registration with valid credentials.
    """
    # Successful registration
    res = client.post("/auth/register", json={
        "username": "testuser",
        "password": "ValidP@ssw0rd"
    })
    assert res.status_code == 201
    assert res.get_json()["message"] == "User registered successfully"

    # Registration with the same username again
    res = client.post("/auth/register", json={
        "username": "testuser",
        "password": "ValidP@ssw0rd2"
    })
    assert res.status_code == 400
    assert "Username already taken" in res.get_json()["message"]

def test_registration_invalid_password(client):
    """
    Test user registration fails with an invalid password format.
    """
    res = client.post("/auth/register", json={
        "username": "anotherUser",
        "password": "weak"  # not meeting complexity
    })
    assert res.status_code == 400
    assert "Password must be" in res.get_json()["message"]

def test_login(client):
    """
    Test user login.
    """
    # First, register a user
    client.post("/auth/register", json={
        "username": "loginUser",
        "password": "ValidP@ssw0rd"
    })

    # Correct login
    res = client.post("/auth/login", json={
        "username": "loginUser",
        "password": "ValidP@ssw0rd"
    })
    assert res.status_code == 200
    assert "access_token" in res.get_json()

    # Wrong password
    res = client.post("/auth/login", json={
        "username": "loginUser",
        "password": "WrongP@ss"
    })
    assert res.status_code == 401
    assert "Invalid username or password" in res.get_json()["message"]

def test_task_endpoints(client):
    """
    Test the task endpoints (create, read, update, delete, mark as done).
    All these endpoints require a valid JWT.
    """

    # 1) Register and login a test user
    register_res = client.post("/auth/register", json={
        "username": "taskUser",
        "password": "ValidP@ssw0rd"
    })
    assert register_res.status_code == 201

    login_res = client.post("/auth/login", json={
        "username": "taskUser",
        "password": "ValidP@ssw0rd"
    })
    assert login_res.status_code == 200
    token = login_res.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2) Add a task
    add_task_res = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Test Description"
    }, headers=headers)
    assert add_task_res.status_code == 201
    assert "Task created successfully" in add_task_res.get_json()["message"]
    new_task_id = add_task_res.get_json()["task"]["id"]

    # 3) View tasks
    view_tasks_res = client.get("/tasks/", headers=headers)
    assert view_tasks_res.status_code == 200
    tasks_list = view_tasks_res.get_json()["tasks"]
    assert len(tasks_list) == 1
    assert tasks_list[0]["title"] == "Test Task"

    # 4) Update the task
    update_res = client.put(f"/tasks/{new_task_id}", json={
        "title": "Updated Title",
        "description": "Updated Description"
    }, headers=headers)
    assert update_res.status_code == 200
    updated_task = update_res.get_json()["task"]
    assert updated_task["title"] == "Updated Title"
    assert updated_task["description"] == "Updated Description"
    assert updated_task["is_done"] == False

    # 5) Mark the task as done
    done_res = client.patch(f"/tasks/{new_task_id}/done", headers=headers)
    assert done_res.status_code == 200
    assert done_res.get_json()["task"]["is_done"] == True

    # 6) Delete the task
    delete_res = client.delete(f"/tasks/{new_task_id}", headers=headers)
    assert delete_res.status_code == 200
    assert "Task deleted successfully" in delete_res.get_json()["message"]

    # Confirm that the task is actually gone
    view_tasks_res = client.get("/tasks/", headers=headers)
    assert view_tasks_res.status_code == 200
    assert len(view_tasks_res.get_json()["tasks"]) == 0

def test_protected_routes_without_token(client):
    """
    Confirm that accessing the task routes without a token returns an error.
    """
    res = client.get("/tasks/")
    assert res.status_code == 401
    assert "Missing Authorization Header" in res.get_json()["msg"]
