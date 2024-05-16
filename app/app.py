from flask import Flask, request, jsonify, render_template, redirect,url_for
import sqlite3
import atexit
from functools import wraps

app = Flask(__name__)

users = {
    'username': 'password'
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        # Redirect to /index on successful login without generating a JWT token
        return redirect(url_for('index'))
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    

#SQLite database initialization
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )
''')
conn.commit()

# Function to close the SQLite connection when the program exits
def close_database_connection():
    conn.close()

# Register the function to be called on exit
atexit.register(close_database_connection)

@app.route('/index')
def index():
    token = request.args.get('token')
    # Fetch all tasks from the database
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task_content = request.form['task']
        # Insert task into the database
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task_content,))
        conn.commit()
        conn.close()
    return redirect('/index')

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    # Delete task from the database
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error deleting task: {e}")

    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    if request.method == 'POST':
        updated_task_content = request.form['updated_task']
        # Update task in the database
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET task = ? WHERE id = ?', (updated_task_content, task_id))
        conn.commit()
        conn.close()
    return redirect('/index')

    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8010)
