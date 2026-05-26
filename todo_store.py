import json
import os

DATA_FILE = "todos.json"

def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_todos(todos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=4)

def add_todo(text):
    if not text.strip():
        return load_todos()  

    todos = load_todos()
    new_todo = {
        "id": len(todos) + 1,  
        "text": text,
        "completed": False,  
    }
    todos.append(new_todo)
    save_todos(todos)
    return todos

def toggle_todo(todo_id):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            break
    save_todos(todos)
    return todos

def remove_todo(todo_id):
    todos = load_todos()
    todos = [todo for todo in todos if todo["id"] != todo_id]
    save_todos(todos)
    return todos