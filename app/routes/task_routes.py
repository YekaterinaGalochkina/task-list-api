from flask import Blueprint, request
from app.models.task import Task
from .route_utilities import validate_model, create_model_instance_from_dict


bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    return create_model_instance_from_dict(Task, request_body)
