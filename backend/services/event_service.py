from db import get_db_connection
from datetime import datetime, timezone


# 🔹 FETCH EVENTS (FINAL STABLE VERSION)
def fetch_events(category=None, event_type=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM events WHERE 1=1"
    params = []

    if category:
        query += " AND category = %s"
        params.append(category)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    # Convert to dict
    columns = [desc[0] for desc in cursor.description]
    events = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    connection.close()

    # ✅ USE UTC (IMPORTANT FIX)
    today = datetime.now(timezone.utc).date()

    cleaned_events = []

    for event in events:
        try:
            start = event.get("start_date")
            end = event.get("end_date")

            # ❌ Skip bad data
            if not start or not end:
                continue

            # ✅ Convert datetime → date safely
            if hasattr(start, "date"):
                start = start.date()
            if hasattr(end, "date"):
                end = end.date()

            # ❌ REMOVE PAST EVENTS (REAL FIX)
            if end < today:
                continue

            # ✅ ADD STATUS (for frontend filter)
            if start > today:
                event["status"] = "upcoming"
            else:
                event["status"] = "ongoing"

            cleaned_events.append(event)

        except Exception as e:
            print("Error processing event:", e)
            continue

    # ✅ APPLY FILTER AFTER CLEANING
    if event_type:
        return [e for e in cleaned_events if e.get("status") == event_type]

    return cleaned_events


# 🔹 INSERT EVENT (SAFE)
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
        connection.commit()

        cursor.close()
        connection.close()

        return {"message": "Event added successfully ✅"}

    except Exception as e:
        if "Duplicate entry" in str(e):
            return {"message": "Event already exists ⚠️"}
        return {"error": str(e)}