import os
from db import get_connection
from faker import Faker
import random

def generate_fake_data():
    if os.path.exists("data_generated.flag"):
        print("✅ Fake data has already been generated. Skipping.")
        return

    fake = Faker()
    conn = get_connection()
    cursor = conn.cursor()

    # Insert fake students
    for _ in range(10):
        name = fake.name()
        email = fake.email()
        password = "password123"
        cursor.execute("INSERT INTO students (name, email, password) VALUES (%s, %s, %s)", (name, email, password))

    # Insert fake events
    for _ in range(5):
        title = fake.catch_phrase()
        description = fake.sentence()
        date = fake.date_between(start_date='today', end_date='+30d')
        cursor.execute("INSERT INTO events (title, description, date) VALUES (%s, %s, %s)", (title, description, date))

    conn.commit()
    conn.close()

    # Create the marker file
    with open("data_generated.flag", "w") as f:
        f.write("Data generated")

    print("✅ Fake data generated successfully.")
