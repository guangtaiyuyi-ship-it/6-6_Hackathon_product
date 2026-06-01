import json
import os
from datetime import datetime

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

def add_todo(text, deadline_str="", category="その他"):
    if not text.strip():
        return load_todos()  

    todos = load_todos()
    new_todo = {
        "id": len(todos) + 1,  
        "text": text,
        "completed": False,  
        "deadline": deadline_str,
        "category": category,
        "deleted": False
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
    for todo in todos:
        if todo["id"] == todo_id:
            todo["deleted"] = True
            break
    save_todos(todos)
    return todos


def restore_todo(todo_id):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo["deleted"] = False
            break
    save_todos(todos)
    return todos


def clear_trash():
    todos = load_todos()
    todos = [todo for todo in todos if not todo["deleted"]]
    save_todos(todos)
    return todos


def update_todo_text(todo_id, new_text):
    if not new_text.strip():
        return load_todos()
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo["text"] = new_text
            break
    save_todos(todos)
    return todos


def get_deadline_status(deadline_str):
    if not deadline_str:
        return "normal", "✅", "#33FF57", 0.7  

    try:
        current_date = datetime.now().date()
        deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        days_left = (deadline_date - current_date).days

        if days_left <= 0:
            return "emergency", "🚨", "#FF3333", 3.0  
        elif days_left == 1:
            return "warning", "⏳", "#FF9900", 2.0  
        elif days_left == 2:
            return "alert", "🗓️", "#E6C300", 1.0  
        else:
            return "normal", "✅", "#33FF57", 0.7  
    except ValueError:
        return "normal", "✅", "#33FF57", 0.7
