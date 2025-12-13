from utils.db_utils import get_db_connection

def test_connection():
    conn = get_db_connection()
    print("Connected to PostgreSQL successfully!")
    conn.close()

if __name__ == "__main__":
    test_connection()
