from db import get_db_connection

def fetch_events(category=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if category:
        query = """
        SELECT * FROM events
        WHERE start_date >= NOW() AND category = %s
        ORDER BY start_date ASC
        """
        cursor.execute(query, (category,))
    else:
        query = """
        SELECT * FROM events
        WHERE start_date >= NOW()
        ORDER BY start_date ASC
        """
        cursor.execute(query)

    events = cursor.fetchall()

    cursor.close()
    connection.close()

    return events

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