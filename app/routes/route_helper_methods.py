from flask import abort, make_response
from ..db import db
import os
import requests

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response = {"details": f"{cls.__name__} id {model_id} is invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"details": f"{cls.__name__} with id {model_id} not found"}
        abort(make_response(response, 404))

    return model


def create_model_instance(cls, data):
    try:
        new_instance = cls.from_dict(data)
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_instance)
    db.session.commit()

    return new_instance


def create_model_response(cls, data):
    new_instance = create_model_instance(cls, data)
    key = cls.__name__.lower()
    return {key: new_instance.to_dict()}, 201


def send_slack_msg(message, channel="test-slack-api"):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    if not slack_token:
        return

    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {slack_token}",
            "Content-Type": "application/json"
        },
        json={
            "channel": channel,
            "text": message
        }
    )