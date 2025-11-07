# task-manager-python-mysql
A simple desktop Task Manager application built with Python, Tkinter GUI, and MySQL. Add, view, update, and delete tasks with an intuitive interface.
# Task Manager - Python & MySQL

A desktop task management application with a graphical user interface built using Python's Tkinter and MySQL database.

## Features

- ✅ Add new tasks with title and description
- 📋 View all tasks in a organized table
- 🔄 Update task status (Pending, In Progress, Completed)
- 🗑️ Delete tasks
- 💾 MySQL database for persistent storage
- 🎨 Clean and intuitive GUI

## Technologies Used

- Python 3.x
- Tkinter (GUI)
- MySQL
- mysql-connector-python

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/task-manager-python-mysql.git
cd task-manager-python-mysql
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure MySQL:
   - Make sure MySQL is installed and running
   - Update `config.py` with your MySQL credentials:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'task_manager'
}
```

## Usage

Run the application:
```bash
python main.py
```

The application will automatically:
- Create the database if it doesn't exist
- Create the tasks table
- Launch the GUI

## Database Schema

**Table: tasks**
- `id` - INT (Primary Key, Auto Increment)
- `title` - VARCHAR(255)
- `description` - TEXT
- `status` - ENUM('pending', 'in_progress', 'completed')
- `created_at` - TIMESTAMP

## Screenshots

[Add screenshots of your application here]

## License

MIT License
