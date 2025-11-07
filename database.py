"""Database setup and connection management"""
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def create_database():
    """Create database if it doesn't exist"""
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"Database '{DB_CONFIG['database']}' is ready")
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error creating database: {e}")
        raise


def get_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def create_table():
    """Create tasks table"""
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
                    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
                    due_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
            print("Table 'tasks' is ready")
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error creating table: {e}")
            raise
    else:
        raise Exception("Could not connect to database")


def test_connection():
    """Test database connection"""
    try:
        # First test basic MySQL connection
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        connection.close()
        return True
    except Error as e:
        raise Exception(f"MySQL connection failed: {e}")


def initialize_database():
    """Initialize database and tables"""
    print("Testing MySQL connection...")
    test_connection()
    print("Creating database...")
    create_database()
    print("Creating table...")
    create_table()
    print("Database initialization complete!")
