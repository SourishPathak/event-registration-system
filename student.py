from db import get_connection
from datetime import datetime


def student_login():
    try:
        student_id = int(input("Enter your Student ID: "))
    except ValueError:
        print("❗ Invalid ID.")
        return None

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()
        if student:
            print(f"✅ Welcome, {student['student_name']}!")
            return student_id
        else:
            print("❌ Student not found.")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    finally:
        conn.close()


def view_available_events():
    print("\n--- Available Events ---")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        if not events:
            print("No events available.")
            return
        for event in events:
            print(f"ID: {event['event_id']}, Name: {event['event_name']}, Date: {event['event_date']}, Venue: {event['venue']}")
    except Exception as e:
        print(f"❌ Error fetching events: {e}")
    finally:
        conn.close()


def register_for_event(student_id):
    try:
        event_id = int(input("Enter Event ID to register for: "))
    except ValueError:
        print("❗ Invalid ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM registrations WHERE student_id = %s AND event_id = %s", (student_id, event_id))
        if cursor.fetchone():
            print("⚠️ Already registered for this event.")
            return

        cursor.execute(
            "INSERT INTO registrations (student_id, event_id, registration_date) VALUES (%s, %s, %s)",
            (student_id, event_id, datetime.today().strftime('%Y-%m-%d'))
        )
        conn.commit()
        print("✅ Registration successful.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()


def student_menu(student_id):
    while True:
        print("\n--- Student Menu ---")
        print("1. View Available Events")
        print("2. Register for Event")
        print("3. Logout")

        choice = input("Enter choice: ")
        if choice == '1':
            view_available_events()
        elif choice == '2':
            register_for_event(student_id)
        elif choice == '3':
            print("🔒 Logged out.")
            break
        else:
            print("❗ Invalid choice.")
