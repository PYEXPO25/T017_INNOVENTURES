from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Zuvi@3101',  # Replace with your MySQL password
    'database': 'mydatabase'
}

# Database initialization
def init_db():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        ''')
        
        # Create register table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS register (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fullname VARCHAR(100) NOT NULL,
                email VARCHAR(50) NOT NULL UNIQUE,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        print(fullname,email,username,password)

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Check if the username already exists in the users table
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            if cursor.fetchone():
                flash('Username already exists! Please choose a different username.')
                return redirect(url_for('register'))

            # Check if the email already exists in the register table
            cursor.execute('SELECT * FROM register WHERE email = %s', (email,))
            if cursor.fetchone():
                flash('Email already exists! Please use a different email.')
                return redirect(url_for('register'))

            # Insert data into the users table
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            
            # Insert data into the register table
            cursor.execute('INSERT INTO register (fullname, email, username, password) VALUES (%s, %s, %s, %s)', 
                           (fullname, email, username, password))
            
            conn.commit()
            cursor.close()
            conn.close()

            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Check if the username and password match in the users table
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                flash('Login successful!')
            else:
                flash('Invalid username or password')
        except mysql.connector.Error as err:
            flash(f'Error: {err}')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)