from flask import Blueprint, request, jsonify, Response
from app.models.goal import Goal
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

    response_body = {"goal": goal.to_dict()}

    return jsonify(response_body), 200

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