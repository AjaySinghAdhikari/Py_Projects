# Py_Projects (Python)

A collection of small Python utilities to improve daily productivity.

## Requirements

- Python 3.10+
- Install dependencies: `pip install -r requirements.txt`

---

## Projects

### 1. To-Do List App

A command-line to-do list with persistent JSON storage.

**Features:**
- Add, list, edit, and delete tasks
- Mark tasks as complete
- Filter to show only open tasks
- Tasks saved automatically to `tasks.json`

**Run:**
```bash
python todo_app/main.py
```

---

### 2. Notification Scheduler

Sends recurring desktop notifications on a configurable schedule.

**Features:**
- Fully driven by `notification_scheduler/config.json` — no code changes needed
- Supports a set number of cycles or infinite mode
- Graceful fallback if `plyer` is not installed (logs to console instead)

**Run (one cycle):**
```bash
python notification_scheduler/main.py
```

**Run forever:**
```bash
python notification_scheduler/main.py --infinite
```

**Run 5 cycles:**
```bash
python notification_scheduler/main.py --cycles 5
```

**Use a custom config file:**
```bash
python notification_scheduler/main.py --config path/to/my_config.json
```

**Edit notifications** by modifying `notification_scheduler/config.json`:
```json
{
  "app_name": "My Scheduler",
  "default_timeout": 10,
  "notifications": [
    {
      "title": "Drink Water",
      "message": "Stay hydrated!",
      "interval_seconds": 3600
    }
  ]
}
```

---

## Files

```
Py_Projects/
├── todo_app/
│   └── main.py              # To-Do List app
├── notification_scheduler/
│   ├── main.py              # Notification scheduler
│   └── config.json          # Edit this to change notifications
├── requirements.txt
├── .gitignore
└── README.md
```

## Notes

- Task data is stored locally in `todo_app/tasks.json` (auto-created, git-ignored).
- If `tasks.json` is deleted, the app starts with an empty list.
- If `plyer` is unavailable, the scheduler prints notifications to the terminal instead.
