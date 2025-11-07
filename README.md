# Task Manager - Python & MySQL Project

A simple command-line task management application demonstrating CRUD operations with MySQL.

## Features

- Add new tasks with title and description
- View all tasks
- Update task status (pending, in_progress, completed)
- Delete tasks
- Automatic database and table creation

## Setup

1. Install MySQL Server on your system

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Update database credentials in `config.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # Change this
    'database': 'task_manager'
}
```

4. Run the application:
```bash
python main.py
```

## Project Structure

- `main.py` - Application entry point with CLI interface
- `task_manager.py` - CRUD operations for tasks
- `database.py` - Database connection and setup
- `config.py` - Database configuration
- `requirements.txt` - Python dependencies

## Usage

The application will automatically create the database and table on first run. Use the menu to:
- Add tasks
- View all tasks
- Update task status
- Delete tasks
