import config
import mysql.connector

# Connect to MySQL server and create a database if it doesn't exist
db = mysql.connector.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
)

cusor = db.cursor()
cusor.execute("CREATE DATABASE IF NOT EXISTS %s",(config.MYSQL_DATABASE, ))
cusor.close()

# Connect to the database 
sql_db = mysql.connector.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    database=config.MYSQL_DATABASE
)
cusor = sql_db.cursor()



cusor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account_number INT NOT NULL UNIQUE,
        account_type ENUM('savings', 'checking') NOT NULL,
        in_vault BOOLEAN NOT NULL DEFAULT FALSE,
        account_status ENUM('active', 'inactive') DEFAULT 'active',
        balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
# if an account is created, it will be created with a default balance of 0.00 and a status of active. But it users can also have the ability to put there account in the vault server. This will foward any request queries to the vault server.
# The vault server will be responsible for managing the account and its balance. The account will be created with a default balance of 0.00 and a status of active. 


cusor.execute("""
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
        account_number INT,
        FOREIGN KEY (account_number) REFERENCES accounts(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
""")
# When a new user is created it will be created with a default account type of user and a status of active. The user will also have the ability to create an account. The account will be created with a default balance of 0.00 and a status of active. 

cusor.execute("""
        CREATE TABLE IF NOT EXISTS Employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        status ENUM('active', 'inactive') DEFAULT 'active',
        privilege ENUM('admin', 'user', 'trader') DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
""")
# Employees will be able to manage the accounts and users. They will be able to create, update, delete and view accounts and users. They will also be able to manage the vault server. The employees will be created with a default status of active.

