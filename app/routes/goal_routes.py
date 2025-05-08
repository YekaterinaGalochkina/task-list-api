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
    goals_response = []

    for goal in goals:
        goals_response.append(goal.to_dict())

    return goals_response

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return  {"goal": goal.to_dict()}


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/delete_all")
def delete_all_goals():
    Goal.query.delete()
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal_with_id(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    for task in goal.tasks:
        task.goal_id = None

    for task_id in task_ids:
        task = validate_model(Task, task_id) 
        task.goal_id = goal.id
        
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }

@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []
    for task in goal.tasks:
        task_dict = task.to_dict()
        task_dict["goal_id"] = goal.id 
        tasks_response.append(task_dict)

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }
