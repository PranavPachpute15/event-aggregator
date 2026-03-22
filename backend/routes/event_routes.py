from flask import Blueprint, request, jsonify
from services.event_service import fetch_events

event_bp = Blueprint("event_bp", __name__)

@event_bp.route("/events", methods=["GET"])
def get_events():
    try:
        category = request.args.get("category")
        event_type = request.args.get("type")
        events = fetch_events(category, event_type)
        return jsonify({"events": events})
    except Exception as e:
        return {"error": str(e)}

from services.event_service import insert_event

@event_bp.route("/add-event", methods=["POST"])
def add_event():
    try:
        data = request.get_json()
        result = insert_event(data)
        return result
    except Exception as e:
        return {"error": str(e)}