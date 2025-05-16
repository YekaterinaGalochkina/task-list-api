from flask import Blueprint, request, Response
from app.models.goal import Goal
from app.models.task import Task
from .route_helper_methods import create_model_instance_from_dict, validate_model
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix = "/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()

    return create_model_instance_from_dict(Goal, request_body)


@bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query.order_by(Goal.id))

    goals_response = [goal.to_dict() for goal in goals]

    return goals_response


@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return  {"goal": goal.to_dict()}


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.update(request_body)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("")
def delete_all_goals():
    Goal.query.delete()
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal_with_id(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    goal.tasks = []

    valid_tasks = [validate_model(Task, task_id) for task_id in task_ids]
    goal.tasks = valid_tasks
        
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }


@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = [task.to_dict() for task in goal.tasks]

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }
