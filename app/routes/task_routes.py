from flask import Blueprint, request, Response, jsonify
from app.models.task import Task
from .route_helper_methods import validate_model, create_model_instance_from_dict
from ..db import db
from datetime import datetime

bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    return create_model_instance_from_dict(Task, request_body)

@bp.get("")
def get_all_tasks():
    sort_order = request.args.get("sort")

    if sort_order == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_order == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:
        response.append(task.to_dict())
    
    return response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    response_body = {"task": task.to_dict()}

    return jsonify(response_body), 200

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")