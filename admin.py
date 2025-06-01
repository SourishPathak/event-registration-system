from db import get_connection


def create_event():
    print("\n--- Create New Event ---")
    name = input("Event Name: ")
    date = input("Event Date (YYYY-MM-DD): ")
    venue = input("Venue: ")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO events (event_name, event_date, venue) VALUES (%s, %s, %s)",
            (name, date, venue)
        )
        conn.commit()
        print("✅ Event created successfully.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()


def view_all_events():
    print("\n--- All Events ---")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        if not events:
            print("No events found.")
            return
        for event in events:
            print(f"ID: {event['event_id']}, Name: {event['event_name']}, Date: {event['event_date']}, Venue: {event['venue']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()


def view_all_registrations():
    print("\n--- All Registrations ---")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT r.registration_id, s.student_name, e.event_name, r.registration_date
            FROM registrations r
            JOIN students s ON r.student_id = s.student_id
            JOIN events e ON r.event_id = e.event_id
        """)
        registrations = cursor.fetchall()
        if not registrations:
            print("No registrations found.")
            return
        for reg in registrations:
            print(f"ID: {reg['registration_id']}, Student: {reg['student_name']}, Event: {reg['event_name']}, Date: {reg['registration_date']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()


def delete_event():
    event_id = input("\nEnter Event ID to delete: ")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM events WHERE event_id = %s", (event_id,))
        conn.commit()
        if cursor.rowcount:
            print("✅ Event deleted.")
        else:
            print("❌ No such event found.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()


def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Create Event")
        print("2. View All Events")
        print("3. View All Registrations")
        print("4. Delete Event")
        print("5. Logout")

        choice = input("Enter choice: ")
        if choice == '1':
            create_event()
        elif choice == '2':
            view_all_events()
        elif choice == '3':
            view_all_registrations()
        elif choice == '4':
            delete_event()
        elif choice == '5':
            print("🔒 Logged out.")
            break
        else:
            print("❗ Invalid choice.")

def admin_login():
    print("\n--- Admin Login ---")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == "admin" and password == "admin123":
        return True
    else:
        return False

def view_registered_students():
    print("📋 Registered students would be listed here (connect to DB).")

def view_events():
    print("📋 Event list would be shown here (connect to DB).")

