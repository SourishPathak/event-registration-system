from db import get_connection
from datetime import datetime

def validate_student_login(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return student

def register_for_event(student_id, event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registrations WHERE student_id = %s AND event_id = %s", (student_id, event_id))
    if cursor.fetchone():
        return False
    cursor.execute(
        "INSERT INTO registrations (student_id, event_id, registration_date) VALUES (%s, %s, %s)",
        (student_id, event_id, datetime.today().strftime('%Y-%m-%d'))
    )
    conn.commit()
    conn.close()
    return True
