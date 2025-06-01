from faker import Faker
import random
from db import get_connection
from datetime import datetime, timedelta

fake = Faker()


def generate_fake_data():
    print("🔄 Generating fake students and events...")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Insert students
        for _ in range(40):
            name = fake.name()
            class_ = random.randint(6, 12)
            email = fake.email()
            cursor.execute("INSERT INTO students (student_name, class, email) VALUES (%s, %s, %s)", (name, class_, email))

        # Insert events
        for _ in range(20):
            event_name = fake.catch_phrase()
            event_date = fake.date_between(start_date='today', end_date='+30d')
            venue = fake.city()
            cursor.execute("INSERT INTO events (event_name, event_date, venue) VALUES (%s, %s, %s)", (event_name, event_date, venue))

        conn.commit()
        print("✅ Fake data generated successfully.")
    except Exception as e:
        print(f"❌ Error generating data: {e}")
    finally:
        conn.close()
