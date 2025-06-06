import pymysql


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "tiger123"
DB_NAME = "event_system"

def get_connection():
    """
    Creates and returns a new database connection.
    """
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor  
    )
