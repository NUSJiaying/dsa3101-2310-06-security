from connect_sql import establish_sql_connection
import mysql.connector
import pandas as pd
import bcrypt
import time

## ADD user
def add_user(username, password, role, email=None):
    
    try: 
        ## establish connection
        db, cursor = establish_sql_connection()
        if db is None:
            print("add_user_roles | Failed to establish a database connection.")
            return False

        ## generate hash and salt
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password.encode('utf-8'), salt)

        ## get role id
        query = f'SELECT id FROM User_roles \
                                    where role = \'{role}\';'
        cursor.execute(query)
        role_id=cursor.fetchone()[0]

        ## insert query
        query = f"\
            INSERT INTO Users\
            (email, username, role_id, salt, hash)\
            VALUES (\'{email}\', \'{username}\', {role_id}, \'{salt.decode('utf-8')}\', \'{hash.decode('utf-8')}\')"
        cursor.execute(query)
        db.commit()
        print(f"add_user | User added: {username}")
    
    except mysql.connector.Error as err:
        if 'Duplicate' in str(err):
            print(f"add_user | User found in database: {username}")
        else:
            print(f"add_user | database error: {err}")

    if cursor:
        cursor.close()
    if db:
        db.close()
    return True


## AUTHENTICATE user
def authenticate(user,password):
    authenticated = False
    user_role = None

    db, cursor = establish_sql_connection()
    query = f"SELECT hash from Users where username = \'{user}\'"
    cursor.execute(query)
    hash_stored = cursor.fetchall()

    ## Check username
    if len(hash_stored) == 0:
        print("authenticate | User not found")
        return False, None
    
    ## Pull hash salt
    hash_stored = hash_stored[0][0]
    query = f"SELECT salt from Users where username = \'{user}\'"
    cursor.execute(query)
    salt = cursor.fetchone()[0]
    hash_entered = bcrypt.hashpw(password.encode('utf-8'),salt.encode('utf-8'))

    ## check results and role
    authenticated = bcrypt.checkpw(password.encode('utf-8'),hash_stored.encode('utf-8'))
    if authenticated:
        query = f"SELECT User_roles.role \
            FROM Users \
            LEFT JOIN User_roles ON Users.role_id = User_roles.id\
                WHERE Users.username = '{user}';"
        cursor.execute(query)
        user_role = cursor.fetchone()[0]

    cursor.close()
    db.close()
    
    return authenticated, user_role

# checks
# print(authenticate("sec1","sec1")) ## Should be (True, security)
# print(authenticate("sec1","random")) ## Should be (False, None)
# print(authenticate("sec2","random")) ## Should be (False, None)