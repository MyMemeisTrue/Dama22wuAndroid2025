import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_FILE = "todos.json"


# -------------------------------
# Helper functions
# -------------------------------

def load_todos():
    """Load todos from file if it exists."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_todos(todos):
    """Save todos to file."""
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=4)


# -------------------------------
# In-memory list but backed by file
# -------------------------------
todos = load_todos()


# -------------------------------
# API routes
# -------------------------------

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200


@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()

    if not data or not all(k in data for k in ("name", "task", "description")):
        return jsonify({"error": "Missing fields"}), 400

    todo_item = {
        "id": len(todos) + 1,
        "name": data["name"],
        "task": data["task"],
        "description": data["description"]
    }

    todos.append(todo_item)
    save_todos(todos)   # <- SAVE TO JSON FILE

    return jsonify(todo_item), 201


# -------------------------------
# Start the server
# -------------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

