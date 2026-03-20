from flask import Flask
from db import get_db_connection
from routes.event_routes import event_bp

app = Flask(__name__)

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
    app.run(debug=True)