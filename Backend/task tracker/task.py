import sys
from datetime import datetime
import os
import json

# JSON file to store tasks
TASK_FILE = 'tasks.json'

# Load tasks from JSON file
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, 'r') as file:
        return json.load(file)

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Add a new task
def add_task(description):
    tasks = load_tasks()
    task_id = 1 if not tasks else tasks[-1]['id'] + 1
    now = datetime.now().isoformat()
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

# Update an existing task
def update_task(task_id, new_desc):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_desc
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated successfully.")
            return
    print("Task not found.")

# Delete a task
def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]
    if len(tasks) == len(new_tasks):
        print("Task not found.")
    else:
        save_tasks(new_tasks)
        print("Task deleted successfully.")

# Mark a task with a new status
def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status}.")
            return
    print("Task not found.")

# List all or filtered tasks in a nice text table with created and updated timestamps
def list_tasks(filter_status=None):
    tasks = load_tasks()
    filtered = [t for t in tasks if (filter_status is None or t["status"] == filter_status)]

    if not filtered:
        print("\nNo tasks found.\n")
        return

    # Print header
    print("\n+----+--------------------------------------+--------------+---------------------+---------------------+")
    print("| ID | Description                          | Status       | Created At          | Updated At          |")
    print("+----+--------------------------------------+--------------+---------------------+---------------------+")

    for task in filtered:
        desc = task['description']
        if len(desc) > 36:
            desc = desc[:33] + "..."
        else:
            desc = desc.ljust(36)
        status = task['status'].ljust(12)
        created = task['createdAt'][:19]  # YYYY-MM-DDTHH:MM:SS
        updated = task['updatedAt'][:19]

        # Replace 'T' with space for better readability
        created = created.replace('T', ' ')
        updated = updated.replace('T', ' ')

        print(f"| {str(task['id']).ljust(2)} | {desc} | {status} | {created} | {updated} |")

    print("+----+--------------------------------------+--------------+---------------------+---------------------+\n")

# Text-based interactive menu GUI
def interactive_menu():
    while True:
        print("\n==== Task Manager Menu ====")
        print("1. List all tasks")
        print("2. Add a task")
        print("3. Update a task")
        print("4. Delete a task")
        print("5. Mark task as in-progress")
        print("6. Mark task as done")
        print("7. List tasks by status")
        print("8. Exit")
        choice = input("Enter choice (1-8): ").strip()

        if choice == '1':
            list_tasks()
        elif choice == '2':
            desc = input("Enter task description: ").strip()
            if desc:
                add_task(desc)
            else:
                print("Description cannot be empty.")
        elif choice == '3':
            try:
                tid = int(input("Enter task ID to update: ").strip())
                new_desc = input("Enter new description: ").strip()
                if new_desc:
                    update_task(tid, new_desc)
                else:
                    print("New description cannot be empty.")
            except ValueError:
                print("Invalid ID.")
        elif choice == '4':
            try:
                tid = int(input("Enter task ID to delete: ").strip())
                delete_task(tid)
            except ValueError:
                print("Invalid ID.")
        elif choice == '5':
            try:
                tid = int(input("Enter task ID to mark in-progress: ").strip())
                mark_task(tid, "in-progress")
            except ValueError:
                print("Invalid ID.")
        elif choice == '6':
            try:
                tid = int(input("Enter task ID to mark done: ").strip())
                mark_task(tid, "done")
            except ValueError:
                print("Invalid ID.")
        elif choice == '7':
            status = input("Enter status filter (todo, in-progress, done): ").strip().lower()
            if status in ('todo', 'in-progress', 'done'):
                list_tasks(status)
            else:
                print("Invalid status.")
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")

# CLI argument handling or interactive menu
def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "add":
            description = " ".join(sys.argv[2:])
            add_task(description)
        elif command == "update":
            try:
                task_id = int(sys.argv[2])
                new_desc = " ".join(sys.argv[3:])
                update_task(task_id, new_desc)
            except (IndexError, ValueError):
                print("Usage: task-cli update <id> <new description>")
        elif command == "delete":
            try:
                task_id = int(sys.argv[2])
                delete_task(task_id)
            except (IndexError, ValueError):
                print("Usage: task-cli delete <id>")
        elif command == "mark-in-progress":
            try:
                task_id = int(sys.argv[2])
                mark_task(task_id, "in-progress")
            except (IndexError, ValueError):
                print("Usage: task-cli mark-in-progress <id>")
        elif command == "mark-done":
            try:
                task_id = int(sys.argv[2])
                mark_task(task_id, "done")
            except (IndexError, ValueError):
                print("Usage: task-cli mark-done <id>")
        elif command == "list":
            status = sys.argv[2] if len(sys.argv) > 2 else None
            list_tasks(status)
        else:
            print("Unknown command.")
    else:
        # No arguments, launch interactive menu
        interactive_menu()

if __name__ == "__main__":
    main()
