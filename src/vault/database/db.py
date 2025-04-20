import mysql.connector
import config

my_sql = mysql.connector.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    database=config.MYSQL_DATABASE,
)

cursor = my_sql.cursor(dictionary=True)

cursor.execute("CREATE DATABASE IF NOT EXISTS vault")

cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_number VARCHAR(255) PRIMARY KEY,
                balance DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                in_vault BOOLEAN DEFAULT FALSE
            )""")

my_sql.commit()
cursor.close()


def get_cursor(dictionary=False):
    """
    Get a cursor for the database connection.
    """
    if dictionary:
        return my_sql.cursor(dictionary=True), my_sql
    return my_sql.cursor(), my_sql



def create_account(account_number, account_type, in_vault, user_id):
    """
    Create a new account in the database.
    """
    cursor, sql_db = get_cursor(dictionary=True)
    query = """
        INSERT INTO accounts (account_number, account_type, user_id, account_status, balance, in_vault)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (account_number, account_type, user_id, 'active', 0.00, in_vault))
    sql_db.commit()
    return cursor.lastrowid if cursor.lastrowid else None

def fetch_row(query, params=None):
    """
    Fetch a single row from the database.
    """
    cursor, sql_db = get_cursor(dictionary=True)
    cursor.execute(query, params or ())
    return cursor.fetchone()

def do_query(query, params=None):
    """
    Execute a query in the database.
    """
    cursor, sql_db = get_cursor(dictionary=True)
    cursor.execute(query, params or ())
    sql_db.commit()
    return cursor.lastrowid if cursor.lastrowid else None