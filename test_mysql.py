import os
import MySQLdb
from dotenv import load_dotenv

def test_mysql_connection():
    load_dotenv()
    
    try:
        connection = MySQLdb.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'admin'),
            passwd=os.getenv('DB_PASSWORD', 'admin'),
            db=os.getenv('DB_NAME', 'upsc_db'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"Successfully connected to MySQL. Version: {version[0]}")
        
        # Test database permissions
        print("\nTesting database permissions...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Number of tables found: {len(tables)}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")

if __name__ == "__main__":
    test_mysql_connection() 