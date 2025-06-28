import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="tiger123",  
        database="event_system",
        cursorclass=pymysql.cursors.DictCursor
    )
