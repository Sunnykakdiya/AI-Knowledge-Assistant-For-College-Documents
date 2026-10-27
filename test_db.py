from app.db.session import test_connection

if __name__ == "__main__":
    try:
        version = test_connection()
        print("SUCCESS: Connected to PostgreSQL!")
        print("Database server:", version)
    except Exception as error:
        print("DATABASE CONNECTION FAILED")
        print(type(error).__name__ + ":", error)
