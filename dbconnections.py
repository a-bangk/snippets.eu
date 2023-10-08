import sys
import mariadb

def get_db_connection(): 
    try: 
        conn = mariadb.connect( 
            user="adam", 
            password="savagge23.3", 
            host="192.168.0.42", 
            port=3306, 
            database="personal_snippetsdb" 
        ) 
    except mariadb.Error as e: 
            print(f"Error connecting to MariaDB Platform: {e}") 
            sys.exit(1) 
    return conn 


