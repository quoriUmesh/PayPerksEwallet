import mysql.connector
from mysql.connector import Error

#  Database configuration dictionary
db_config = {
    'host': 'payperksprojectserver.mysql.database.azure.com',
    'user': 'quoriumesh',
    'password': 'server1DBMSproject',
    'database': 'payperks',
    'ssl_ca': 'payperks_ssl.pem'  # Path to your SSL certificate
}

# Create a connection
def create_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Connection successful")
            return conn
    except Error as e:
        print("Error while connecting:", e)
        return None

#  Close the connection
def close_connection(conn):
    if conn and conn.is_connected():
        conn.close()
        print("Connection closed.")

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        # Perform database operations here
        pass
    close_connection(connection)