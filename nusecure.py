from flask import Flask
import mysql.connector
import bcrypt

app = Flask(__name__)

def establish_sql_connection():
    db = mysql.connector.connect(
        host = "database", 
        user = "user",
        password = "dsa3101",
        database = "secdb"
        )
    return db
        
@app.route("/")
def nusecure():
    return "<p>Welcome to NUSecure!</p>"

@app.route("/add_user", methods = ["POST"])
def add_user(email, username, role_id, password):
    email = request.args.get('email')
    username = request.args.get('username')
    role_id = request.args.get('role_id')
    password = request.args.get('password')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password, salt)

    db = establish_sql_connection()
    cursor = db.cursor
    query = f"\
        INSERT INTO Users\
        (email, username, role_id, salt, hash)\
        VALUES ('{email}', '{username}', {role_id}, '{salt}', '{hash}')"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
