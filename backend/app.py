from flask import Flask
from flask_cors import CORS
from db import get_db_connection
from routes.event_routes import event_bp

app = Flask(__name__)

# 🔥 ENABLE CORS (VERY IMPORTANT)
CORS(app)

# Register Blueprint (routes)
app.register_blueprint(event_bp)


@app.route("/")
def home():
    return "Event Aggregator Backend Running Successfully 🚀"


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


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)