from db import get_db_connection
from datetime import datetime


# 🔹 FETCH EVENTS (NO HARD FILTER — DEBUG + FLEXIBLE)
def fetch_events(category=None, event_type=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM events WHERE 1=1"
    params = []

    if category:
        query += " AND category = %s"
        params.append(category)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    events = cursor.fetchall()

    cursor.close()
    connection.close()

    # 🔥 APPLY FILTERING IN PYTHON (SMART WAY)
    if event_type:
        today = datetime.today().date()
        filtered_events = []

        for event in events:
            start = event.get("start_date")
            end = event.get("end_date")

            if start:
                start = start.date()
            if end:
                end = end.date()

            if event_type == "upcoming":
                if start and start >= today:
                    filtered_events.append(event)

            elif event_type == "ongoing":
                if start and end and start <= today <= end:
                    filtered_events.append(event)

            elif event_type == "past":
                if end and end < today:
                    filtered_events.append(event)

        return filtered_events

    return events


# 🔹 INSERT EVENT
def insert_event(data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO events 
        (title, description, event_url, source, category, start_date, end_date, location)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data.get("title"),
            data.get("description"),
            data.get("event_url"),
            data.get("source"),
            data.get("category"),
            data.get("start_date"),
            data.get("end_date"),
            data.get("location")
        )

        cursor.execute(query, values)
        connection.commit()   # ✅ VERY IMPORTANT

        cursor.close()
        connection.close()

        return {"message": "Event added successfully ✅"}

    except Exception as e:
        if "Duplicate entry" in str(e):
            return {"message": "Event already exists ⚠️"}
        return {"error": str(e)}