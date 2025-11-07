"""Main application entry point with Tkinter GUI"""
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from database import initialize_database
from task_manager import TaskManager


class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("900x600")
        # self.root.resizable(False, False)
        
        # Initialize database
        try:
            initialize_database()
            self.manager = TaskManager()
        except Exception as e:
            messagebox.showerror("Database Error", 
                f"Failed to connect to database!\n\n"
                f"Error: {str(e)}\n\n"
                f"Please check your MySQL credentials in config.py")
            root.destroy()
            return
        
        # Create GUI components
        self.create_widgets()
        self.refresh_tasks()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="TASK MANAGER", font=("Arial", 20, "bold"), bg="#4CAF50", fg="white", pady=10)
        title_label.pack(fill=tk.X)
        
        # Statistics Frame
        stats_frame = tk.Frame(self.root, bg="#f0f0f0", pady=5)
        stats_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Loading statistics...", font=("Arial", 10), bg="#f0f0f0")
        self.stats_label.pack()
        
        # Input Frame
        input_frame = tk.LabelFrame(self.root, text="Add New Task", font=("Arial", 12, "bold"), padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(input_frame, text="Title:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = tk.Entry(input_frame, width=40, font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(input_frame, text="Description:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.desc_entry = tk.Entry(input_frame, width=40, font=("Arial", 10))
        self.desc_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(input_frame, text="Priority:", font=("Arial", 10)).grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20,0))
        self.priority_var = tk.StringVar(value="medium")
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, values=["low", "medium", "high"], state="readonly", width=10, font=("Arial", 10))
        priority_combo.grid(row=0, column=3, pady=5, padx=10)
        
        tk.Label(input_frame, text="Due Date:", font=("Arial", 10)).grid(row=1, column=2, sticky=tk.W, pady=5, padx=(20,0))
        self.due_date_entry = DateEntry(input_frame, width=10, font=("Arial", 10), date_pattern='yyyy-mm-dd')
        self.due_date_entry.grid(row=1, column=3, pady=5, padx=10)
        
        add_btn = tk.Button(input_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15)
        add_btn.grid(row=2, column=3, pady=10, sticky=tk.E)
        
        # Search Frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30, font=("Arial", 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_tasks, bg="#2196F3", fg="white", font=("Arial", 9), width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Label(search_frame, text="Filter:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(20,5))
        self.filter_var = tk.StringVar(value="all")
        filter_combo = ttk.Combobox(search_frame, textvariable=self.filter_var, values=["all", "pending", "in_progress", "completed"], state="readonly", width=12, font=("Arial", 9))
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())
        
        tk.Button(search_frame, text="Clear", command=self.refresh_tasks, bg="#9E9E9E", fg="white", font=("Arial", 9), width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Export", command=self.export_tasks, bg="#FF9800", fg="white", font=("Arial", 9), width=10).pack(side=tk.LEFT, padx=5)
        
        # Task List Frame
        list_frame = tk.LabelFrame(self.root, text="Task List", font=("Arial", 12, "bold"), padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ("ID", "Title", "Description", "Priority", "Status", "Due Date", "Created At")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Created At", text="Created At")
        
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Title", width=150)
        self.tree.column("Description", width=200)
        self.tree.column("Priority", width=80, anchor=tk.CENTER)
        self.tree.column("Status", width=100, anchor=tk.CENTER)
        self.tree.column("Due Date", width=100, anchor=tk.CENTER)
        self.tree.column("Created At", width=130, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons Frame
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack(fill=tk.X, padx=20)
        
        tk.Button(btn_frame, text="Mark Pending", command=lambda: self.update_status("pending"), bg="#FFC107", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Mark In Progress", command=lambda: self.update_status("in_progress"), bg="#2196F3", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Mark Completed", command=lambda: self.update_status("completed"), bg="#4CAF50", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_task, bg="#f44336", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_tasks, bg="#9E9E9E", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
    
    def add_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get_date().strftime('%Y-%m-%d')
        
        if not title:
            messagebox.showwarning("Input Error", "Title cannot be empty!")
            return
        
        if self.manager.add_task(title, description, priority, due_date):
            messagebox.showinfo("Success", f"Task '{title}' added successfully!")
            self.title_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.priority_var.set("medium")
            self.refresh_tasks()
    
    def refresh_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        tasks = self.manager.view_all_tasks()
        self.display_tasks(tasks)
        self.update_statistics()
    
    def display_tasks(self, tasks):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if tasks:
            for task in tasks:
                # Color code by priority
                tags = ()
                if task.get('priority') == 'high':
                    tags = ('high_priority',)
                elif task.get('priority') == 'low':
                    tags = ('low_priority',)
                
                self.tree.insert("", tk.END, values=(
                    task['id'],
                    task['title'],
                    task['description'] or "",
                    task.get('priority', 'medium'),
                    task['status'],
                    str(task.get('due_date', '')) if task.get('due_date') else "",
                    str(task['created_at'])
                ), tags=tags)
        
        # Configure tag colors
        self.tree.tag_configure('high_priority', background='#ffcccc')
        self.tree.tag_configure('low_priority', background='#e8f5e9')
    
    def search_tasks(self):
        search_term = self.search_entry.get().strip()
        if search_term:
            tasks = self.manager.search_tasks(search_term)
            self.display_tasks(tasks)
        else:
            messagebox.showwarning("Input Error", "Please enter a search term!")
    
    def apply_filter(self):
        filter_value = self.filter_var.get()
        if filter_value == "all":
            self.refresh_tasks()
        else:
            tasks = self.manager.filter_by_status(filter_value)
            self.display_tasks(tasks)
    
    def update_statistics(self):
        stats = self.manager.get_statistics()
        if stats:
            self.stats_label.config(
                text=f"Total: {stats['total']} | Pending: {stats['pending']} | "
                     f"In Progress: {stats['in_progress']} | Completed: {stats['completed']} | "
                     f"High Priority: {stats['high_priority']}"
            )
    
    def export_tasks(self):
        tasks = self.manager.view_all_tasks()
        if not tasks:
            messagebox.showinfo("Export", "No tasks to export!")
            return
        
        try:
            filename = f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("TASK MANAGER - EXPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                for task in tasks:
                    f.write(f"ID: {task['id']}\n")
                    f.write(f"Title: {task['title']}\n")
                    f.write(f"Description: {task['description'] or 'N/A'}\n")
                    f.write(f"Priority: {task.get('priority', 'medium')}\n")
                    f.write(f"Status: {task['status']}\n")
                    f.write(f"Due Date: {task.get('due_date', 'N/A')}\n")
                    f.write(f"Created: {task['created_at']}\n")
                    f.write("-" * 80 + "\n\n")
            
            messagebox.showinfo("Export Success", f"Tasks exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export tasks: {str(e)}")
    
    def update_status(self, status):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task!")
            return
        
        task_id = self.tree.item(selected[0])['values'][0]
        if self.manager.update_task_status(task_id, status):
            messagebox.showinfo("Success", f"Task updated to '{status}'")
            self.refresh_tasks()
    
    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task!")
            return
        
        task_id = self.tree.item(selected[0])['values'][0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete task {task_id}?")
        
        if confirm:
            if self.manager.delete_task(task_id):
                messagebox.showinfo("Success", "Task deleted successfully!")
                self.refresh_tasks()


def main():
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
