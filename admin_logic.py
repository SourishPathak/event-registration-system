from db import get_connection

def validate_admin_login(username, password):
    return username == "admin" and password == "admin123"

def create_event(name, date, venue):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (event_name, event_date, venue) VALUES (%s, %s, %s)", (name, date, venue))
    conn.commit()
    conn.close()

def get_all_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()
    return events

def get_all_registrations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.registration_id, s.student_name, e.event_name, r.registration_date
        FROM registrations r
        JOIN students s ON r.student_id = s.student_id
        JOIN events e ON r.event_id = e.event_id
    """)
    data = cursor.fetchall()
    conn.close()
    return data
