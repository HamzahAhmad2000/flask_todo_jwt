"""
Blueprint for task management (Create, Read, Update, Delete).
All endpoints are protected by JWT.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Task, User

tasks_bp = Blueprint("tasks_bp", __name__)

@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def add_task():
    """
    Add a new task for the currently authenticated user.
    Requires JSON with 'title' and (optional) 'description'.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return jsonify({"message": "Task title is required"}), 400

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    new_task = Task(title=title, description=description, owner=user)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "message": "Task created successfully",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description
        }
    }), 201

@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    """
    Retrieve all tasks for the currently authenticated user.
    """
    current_user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=current_user_id).all()

    tasks_list = []
    for task in tasks:
        tasks_list.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_done": task.is_done,
            "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({"tasks": tasks_list}), 200

@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    """
    Update an existing task (title and/or description) for the current user.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    title = data.get("title")
    description = data.get("description")

    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    if title:
        task.title = title
    if description:
        task.description = description

    db.session.commit()

    return jsonify({
        "message": "Task updated successfully",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_done": task.is_done
        }
    }), 200

@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """
    Delete a task belonging to the current user.
    """
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200

@tasks_bp.route("/<int:task_id>/done", methods=["PATCH"])
@jwt_required()
def mark_task_done(task_id):
    """
    Mark a task as done (is_done = True) for the current user.
    """
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    task.is_done = True
    db.session.commit()

    return jsonify({
        "message": "Task marked as done",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_done": task.is_done
        }
    }), 200
