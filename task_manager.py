"""Task Manager - CRUD operations"""
from database import get_connection
from mysql.connector import Error


class TaskManager:
    
    def add_task(self, title, description, priority='medium', due_date=None):
        """Create a new task"""
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO tasks (title, description, priority, due_date) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (title, description, priority, due_date))
                connection.commit()
                cursor.close()
                connection.close()
                return True
            except Error as e:
                print(f"Error adding task: {e}")
                return False
    
    def view_all_tasks(self):
        """Read all tasks"""
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
                tasks = cursor.fetchall()
                cursor.close()
                connection.close()
                return tasks
            except Error as e:
                print(f"Error fetching tasks: {e}")
                return []
        return []
    
    def update_task_status(self, task_id, status):
        """Update task status"""
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "UPDATE tasks SET status = %s WHERE id = %s"
                cursor.execute(query, (status, task_id))
                connection.commit()
                success = cursor.rowcount > 0
                cursor.close()
                connection.close()
                return success
            except Error as e:
                print(f"Error updating task: {e}")
                return False
    
    def delete_task(self, task_id):
        """Delete a task"""
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "DELETE FROM tasks WHERE id = %s"
                cursor.execute(query, (task_id,))
                connection.commit()
                success = cursor.rowcount > 0
                cursor.close()
                connection.close()
                return success
            except Error as e:
                print(f"Error deleting task: {e}")
                return False

    def search_tasks(self, search_term):
        """Search tasks by title"""
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM tasks WHERE title LIKE %s ORDER BY created_at DESC"
                cursor.execute(query, (f"%{search_term}%",))
                tasks = cursor.fetchall()
                cursor.close()
                connection.close()
                return tasks
            except Error as e:
                print(f"Error searching tasks: {e}")
                return []
        return []
    
    def filter_by_status(self, status):
        """Filter tasks by status"""
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM tasks WHERE status = %s ORDER BY created_at DESC"
                cursor.execute(query, (status,))
                tasks = cursor.fetchall()
                cursor.close()
                connection.close()
                return tasks
            except Error as e:
                print(f"Error filtering tasks: {e}")
                return []
        return []
    
    def get_statistics(self):
        """Get task statistics"""
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                        SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
                        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                        SUM(CASE WHEN priority = 'high' THEN 1 ELSE 0 END) as high_priority
                    FROM tasks
                """)
                stats = cursor.fetchone()
                cursor.close()
                connection.close()
                return stats
            except Error as e:
                print(f"Error getting statistics: {e}")
                return None
        return None
