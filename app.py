from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Connect to the database
conn = sqlite3.connect('tasks.db')
c = conn.cursor()

# Create the tasks table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              description TEXT NOT NULL,
              completed BOOLEAN NOT NULL DEFAULT 0)''')

# Close the cursor and connection
c.close()
conn.close()

# Create a task
@app.route('/tasks', methods=['POST'])
def create_task():
    # Get the data from the request
    data = request.json
    title = data['title']
    description = data['description']

    # Insert the task into the database
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
    task_id = c.lastrowid
    conn.commit()

    # Close the cursor and connection
    c.close()
    conn.close()

    # Return the new task
    return jsonify({'id': task_id, 'title': title, 'description': description, 'completed': False}), 201

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    # Connect to the database
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    # Get all tasks
    c.execute("SELECT id, title, description, completed FROM tasks")
    tasks = c.fetchall()

    # Close the cursor and connection
    c.close()
    conn.close()

    # Return the tasks
    return jsonify({'tasks': [{'id': task[0], 'title': task[1], 'description': task[2], 'completed': task[3]} for task in tasks]}), 200

# Get a task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    # Connect to the database
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    # Get the task by ID
    c.execute("SELECT id, title, description, completed FROM tasks WHERE id=?", (task_id,))
    task = c.fetchone()

    # Close the cursor and connection
    c.close()
    conn.close()

    # Return the task
    if task:
        return jsonify({'id': task[0], 'title': task[1], 'description': task[2], 'completed': task[3]}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

# Update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # Get the data from the request
    data = request.json
    title = data['title']
    description = data['description']
    completed = data['completed']

    # Update the task in the database
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET title=?, description=?, completed=? WHERE id=?", (title, description, completed, task_id))
    conn.commit()

    # Close the cursor
    conn.close()

    # Return the updated task
    return jsonify({'id': task_id, 'title': title, 'description': description, 'completed': completed}), 200

#Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Delete the task from the database
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    # Close the cursor and connection
    c.close()
    conn.close()

    # Return a success message
    return jsonify({'message': 'Task deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)