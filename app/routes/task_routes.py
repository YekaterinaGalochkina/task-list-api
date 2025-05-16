from flask import Blueprint, request, Response
from app.models.task import Task
from .route_helper_methods import validate_model, create_model_response, send_slack_msg
from ..db import db
from datetime import datetime
from sqlalchemy import delete, select

bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    return create_model_response(Task, request_body)


@bp.get("")
def get_all_tasks():
    sort_order = request.args.get("sort")
    query = select(Task)

    if sort_order == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_order == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)
    response = [task.to_dict() for task in tasks]
    
    return response


@bp.get("/<task_id>")
def get_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.update(request_body)
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

    send_slack_msg(f"Yekaterina just completed {task.title}")

    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")


@bp.delete("")
def delete_all_tasks():
    delete_all_tasks = delete(Task)
    db.session.execute(delete_all_tasks)
    db.session.commit()

    return Response(status=204, mimetype="application/json")