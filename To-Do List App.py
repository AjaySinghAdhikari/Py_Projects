from pathlib import Path
import json

TASKS_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    if TASKS_FILE.exists():
        try:
            with TASKS_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, OSError):
            pass
    return []


def save_tasks(tasks):
    try:
        with TASKS_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2)
    except OSError as exc:
        print(f"Error saving tasks: {exc}")


def add_task(tasks):
    task = input("Enter a new task: ").strip()
    if not task:
        print("Task cannot be empty.")
        return

    tasks.append({"task": task, "done": False})
    save_tasks(tasks)
    print(f"Task added: {task}")


def list_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return

    print("Tasks:")
    for i, item in enumerate(tasks, 1):
        status = "Done" if item["done"] else "Pending"
        print(f"{i}. [{status}] {item['task']}")


def get_task_number(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid number.")
        return None


def mark_complete(tasks):
    if not tasks:
        print("No tasks to mark as complete.")
        return

    list_tasks(tasks)
    task_number = get_task_number("Enter the task number to mark as complete: ")
    if task_number is None:
        return

    if 1 <= task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        print(f"Task marked as complete: {tasks[task_number - 1]['task']}")
    else:
        print("Invalid task number.")


def delete_task(tasks):
    if not tasks:
        print("No tasks to delete.")
        return

    list_tasks(tasks)
    task_number = get_task_number("Enter the task number to delete: ")
    if task_number is None:
        return

    if 1 <= task_number <= len(tasks):
        removed = tasks.pop(task_number - 1)
        save_tasks(tasks)
        print(f"Task deleted: {removed['task']}")
    else:
        print("Invalid task number.")


def main():
    tasks = load_tasks()

    while True:
        print("\nMenu:")
        print("1. Add a task")
        print("2. List tasks")
        print("3. Mark a task as complete")
        print("4. Delete a task")
        print("5. Quit")

        choice = input("Enter your choice (1/2/3/4/5): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            mark_complete(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()