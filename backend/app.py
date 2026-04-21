from flask import Flask, jsonify, request
from event_service import fetch_events, insert_event
from db import get_db_connection

app = Flask(__name__)

# 🔹 HOME
@app.route("/")
def home():
    return "Event Aggregator Backend Running 🚀"


# 🔹 GET EVENTS
@app.route("/events", methods=["GET"])
def get_events():
    category = request.args.get("category")
    event_type = request.args.get("type")

    events = fetch_events(category, event_type)
    return jsonify({"events": events})


# 🔹 ADD EVENT (POST)
@app.route("/events", methods=["POST"])
def add_event():
    data = request.json
    result = insert_event(data)
    return jsonify(result)


# 🔹 DELETE EVENT
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Event deleted successfully ✅"})

    except Exception as e:
        return jsonify({"error": str(e)})


# 🔹 TEST DB
@app.route("/test-db")
def test_db():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return f"Database Connection Successful ✅ Result: {result}"
    except Exception as e:
        return f"Database Connection Failed ❌ {str(e)}"


# 🔹 RUN
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)