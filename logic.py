from db import get_connection
from datetime import datetime

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def authenticate_user(username, password):
    """
    Authenticate either an admin or student based on credentials.
    """
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return "admin", {"username": ADMIN_USERNAME}

    # Check student credentials
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE username = %s AND password = %s", (username, password))
    student = cursor.fetchone()
    conn.close()

    if student:
        return "student", student
    else:
        return None, None

def get_all_events():
    """
    Fetch all events from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()
    return events

def get_registered_events(student_id):
    """
    Return a list of events a student has registered for.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.event_name, e.event_date, e.venue
        FROM registrations r
        JOIN events e ON r.event_id = e.event_id
        WHERE r.student_id = %s
    """, (student_id,))
    events = cursor.fetchall()
    conn.close()
    return events

def register_event(student_id, event_id):
    """
    Register a student for a specific event if not already registered.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Check if already registered
    cursor.execute("SELECT * FROM registrations WHERE student_id = %s AND event_id = %s", (student_id, event_id))
    if cursor.fetchone():
        conn.close()
        return "⚠️ Already Registered"

    # Register new
    cursor.execute(
        "INSERT INTO registrations (student_id, event_id, registration_date) VALUES (%s, %s, %s)",
        (student_id, event_id, datetime.today().strftime('%Y-%m-%d'))
    )
    conn.commit()
    conn.close()
    return "✅ Registered Successfully"

def create_event(name, date, venue):
    """
    Admin creates a new event.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (event_name, event_date, venue) VALUES (%s, %s, %s)", (name, date, venue))
    conn.commit()
    conn.close()

def delete_event(event_id):
    """
    Admin deletes an existing event by event_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE event_id = %s", (event_id,))
    conn.commit()
    conn.close()

def get_all_registrations():
    """
    Admin fetches all event registrations.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.registration_id, s.student_name, e.event_name, r.registration_date
        FROM registrations r
        JOIN students s ON r.student_id = s.student_id
        JOIN events e ON r.event_id = e.event_id
    """)
    result = cursor.fetchall()
    conn.close()
    return result
