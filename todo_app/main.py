from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks.json")


@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    created_at: str = ""


def load_tasks() -> list[Task]:
    if not TASKS_FILE.exists():
        return []

    # FIX: wrap json.load in try/except — corrupted file used to crash the app
    try:
        with TASKS_FILE.open("r", encoding="utf-8") as task_file:
            raw_tasks = json.load(task_file)
    except json.JSONDecodeError:
        print("Warning: tasks file is corrupted. Starting with an empty task list.")
        return []

    tasks: list[Task] = []
    for item in raw_tasks:
        tasks.append(
            Task(
                id=int(item["id"]),
                title=str(item["title"]),
                completed=bool(item.get("completed", False)),
                created_at=str(item.get("created_at", "")),
            )
        )
    return tasks


def save_tasks(tasks: list[Task]) -> None:
    with TASKS_FILE.open("w", encoding="utf-8") as task_file:
        json.dump([asdict(task) for task in tasks], task_file, indent=2)


def next_task_id(tasks: list[Task]) -> int:
    return max((task.id for task in tasks), default=0) + 1


def list_tasks(tasks: list[Task], only_open: bool = False) -> None:
    filtered = [t for t in tasks if not t.completed] if only_open else tasks
    if not filtered:
        print("No tasks yet." if not only_open else "No open tasks.")
        return

    label = "Open Tasks" if only_open else "All Tasks"
    print(f"\n{label}:")
    for task in filtered:
        status = "done" if task.completed else "open"
        print(f"  {task.id}. [{status}] {task.title}")


def add_task(tasks: list[Task]) -> None:
    title = input("Enter a new task: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return

    tasks.append(
        Task(
            id=next_task_id(tasks),
            title=title,
            completed=False,
            created_at=datetime.now().isoformat(timespec="seconds"),
        )
    )
    save_tasks(tasks)
    print(f"Task added: {title}")


def mark_complete(tasks: list[Task]) -> None:
    if not tasks:
        print("No tasks to complete.")
        return

    list_tasks(tasks)
    try:
        task_id = int(input("Enter task ID to mark complete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for task in tasks:
        if task.id == task_id:
            task.completed = True
            save_tasks(tasks)
            print(f"Task marked complete: {task.title}")
            return

    print("Task ID not found.")


# FIX: new feature — edit an existing task's title
def edit_task(tasks: list[Task]) -> None:
    if not tasks:
        print("No tasks to edit.")
        return

    list_tasks(tasks)
    try:
        task_id = int(input("Enter task ID to edit: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for task in tasks:
        if task.id == task_id:
            new_title = input(f"New title (current: \"{task.title}\"): ").strip()
            if not new_title:
                print("Title cannot be empty. Edit cancelled.")
                return
            task.title = new_title
            save_tasks(tasks)
            print(f"Task updated to: {task.title}")
            return

    print("Task ID not found.")


def delete_task(tasks: list[Task]) -> None:
    if not tasks:
        print("No tasks to delete.")
        return

    list_tasks(tasks)
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    original_length = len(tasks)
    tasks[:] = [task for task in tasks if task.id != task_id]
    if len(tasks) == original_length:
        print("Task ID not found.")
        return

    save_tasks(tasks)
    print("Task deleted.")


def show_menu() -> None:
    print("\nMenu:")
    print("1. Add a task")
    print("2. List all tasks")
    print("3. List open tasks only")   # FIX: new filter option
    print("4. Mark a task as complete")
    print("5. Edit a task")            # FIX: new edit option
    print("6. Delete a task")
    print("7. Quit")


def main() -> None:
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            list_tasks(tasks, only_open=True)
        elif choice == "4":
            mark_complete(tasks)
        elif choice == "5":
            edit_task(tasks)
        elif choice == "6":
            delete_task(tasks)
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
