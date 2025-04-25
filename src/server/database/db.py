import mysql.connector
from mysql.connector.types import RowItemType
import config
from lib.account import Account
from lib.user import User
from lib.employee import Employee
import random_address
from faker import Faker
import random

# Connect to the database
sql_db = mysql.connector.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    database=config.MYSQL_DATABASE
)
cursor = sql_db.cursor()

cursor.execute("""
  CREATE TABLE IF NOT EXISTS accounts (
        id INT(10) AUTO_INCREMENT PRIMARY KEY,
        account_number INT NOT NULL UNIQUE,
        account_type ENUM('savings', 'checking') NOT NULL,
        in_vault BOOLEAN NOT NULL DEFAULT FALSE,
        account_status ENUM('active', 'inactive') DEFAULT 'active',
        balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
        user_id INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        phone VARCHAR(255),
        address VARCHAR(255),
        city VARCHAR(255),
        state VARCHAR(255),
        zip VARCHAR(255),
        country VARCHAR(255),
        status ENUM('active', 'inactive') DEFAULT 'active',
        account_number INT(10),
        FOREIGN KEY (account_number) REFERENCES accounts(account_number),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
""")
# When a new user is created it will be created with a default account type of user and a status of active. The user will also have the ability to create an account. The account will be created with a default balance of 0.00 and a status of active.

cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account_number INT(10) NOT NULL,
        transaction_type ENUM('deposit', 'withdrawal') NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_number) REFERENCES accounts(account_number)
               )
        """)
cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        status ENUM('active', 'inactive') DEFAULT 'active',
        privilege ENUM('admin', 'user', 'trader') DEFAULT 'user',
        avatar_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
""")
cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat (
        id INT AUTO_INCREMENT PRIMARY KEY,
        sender_id INT NOT NULL,
        message TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_id) REFERENCES employees(id)
    )
""")
# if an account is created, it will be created with a default balance of 0.00 and a status of active. But it users can also have the ability to put there account in the vault server. This will foward any request queries to the vault server.
# The vault server will be responsible for managing the account and its balance. The account will be created with a default balance of 0.00 and a status of active.


cursor.execute("""
        CREATE TABLE IF NOT EXISTS init (
        id INT AUTO_INCREMENT PRIMARY KEY,
        flag BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
""")

# Employees will be able to manage the accounts and users. They will be able to create, update, delete and view accounts and users. They will also be able to manage the vault server. The employees will be created with a default status of active.

cursor.execute("""
    INSERT IGNORE INTO employees (username, password, email, first_name, last_name, status, privilege)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (
    config.ADMIN_USERNAME,
    config.ADMIN_PASSWORD,
    'developer@admin.com',
    'admin',
    'admin',
    'active',
    'admin'
))


# Insert the admin user into the Employees table if it doesn't exist
cursor.execute("SELECT * FROM employees WHERE username = %s", (config.ADMIN_USERNAME,))
admin_user = cursor.fetchone()
if not admin_user:
    print("ERROR: Unable to create admin user")



sql_db.commit()
cursor.close()

def get_db():
    return sql_db

def get_cursor(dictionary=True):
    sql_db = get_db()
    cursor = sql_db.cursor(dictionary=dictionary,buffered=True )
    return cursor, sql_db



def init_db(force=False):
    """
    Initialize the database with default values.
    """
    init_query = "SELECT * FROM init"
    row = fetch_row(init_query)
    if row and not force:
        print("Database already initialized")
        return False

    accounts:list[Account] = []
    # make 20 users with random data
    for i in range(200):
        fake = Faker()
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone = fake.phone_number()
        address = random_address.real_random_address()
        address_1 = address.get('address1', '123 Main St')
        city = address.get('city', 'New York')
        state = address.get('state', 'NY')
        zip_code = address.get('postalCode', '10001')
        country = "US"
        user = User.register(
            username,
            password,
            email,
            first_name,
            last_name,
            phone,
            address_1,
            city,
            state,
            zip_code,
            country)
        if not user:
            print("ERROR: Unable to create user")
            continue
        account = user.get_account()
        if not account:
            print("ERROR: Unable to create account")
            continue
        accounts.append(account)

        result = random.randint(0, 1)
        if result == 1:
            result = account.transfer_to_vault()
            if not result:
                print("ERROR: Unable to transfer account to vault")
                continue
        print(f"Created user {username} with account number {account.account_number}")

    # create a transaction for the user
    for j in range(200):
        account_from_index = random.randint(0, len(accounts) - 1)
        account_to_index = random.randint(0, len(accounts) - 1)
        amount = random.randint(1, 1000)

        account_from = accounts[account_from_index]
        account_to = accounts[account_to_index]
        if not account_from or not account_to:
            print("ERROR: Unable to create transaction")
            continue
        if account_from.account_number == account_to.account_number:
            continue

        result = account_from.transfer_funds(account_to.account_number, amount)
        print(f"Transferred {amount} from account {account_from.account_number} to account {account_to.account_number}")




    # create employees with random data
    for i in range(15):
        fake = Faker()
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()
        avatar_url = fake.image_url()
        employee = Employee.register(
            username,
            password,
            email,
            first_name,
            last_name,
            avatar_url=avatar_url
        )
        if not employee:
            print("ERROR: Unable to create employee")
            continue

        should_update = random.randint(0, 1)
        if should_update == 1:
            employee.update_privilege('trader')
            print(f"Updated password for employee {username}")

        print(f"Created employee {username} with id {employee.employee_id}")


    init_query = "INSERT INTO init (flag) VALUES (%s)"
    insert_query(init_query, (True,))
    print("Database initialized")




def insert_query(query, data):
    try:
        cursor, sql_db = get_cursor()
        cursor.execute(query, data)
        lastrowid = cursor.lastrowid
        sql_db.commit()
        cursor.close()
        return lastrowid
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def do_query(query, data=None):
    try:
        cursor, sql_db = get_cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        rowcount = cursor.rowcount
        sql_db.commit()
        cursor.close()

        return rowcount > 0
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def fetch_row(query, data=None) -> dict[str, RowItemType] | None:
    try:
        cursor, sql_db = get_cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row  # type: ignore[return-value]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_all(query, data=None) -> list[dict[str, RowItemType]] | None:
    try:
        cursor, sql_db = get_cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows  # type: ignore[return-value]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
     
