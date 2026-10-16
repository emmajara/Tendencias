import sqlite3
from typing import Optional, List
from domain.model.task.task import Task
from domain.model.task.gateways.task_repository import TaskRepository
from .task_dbo import TaskDBO
from .task_mapper import TaskMapper

class SqliteTaskAdapter(TaskRepository):
    def __init__(self):
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL CHECK (completed IN (0, 1))
            )
        """)
        self.conn.commit()

    def save(self, task: Task) -> Task:
        dbo = TaskMapper.to_dbo(task)
        cursor = self.conn.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, ?)",
            (dbo.title, dbo.completed)
        )
        self.conn.commit()
        task.id = cursor.lastrowid
        return task

    def find_by_id(self, task_id: int) -> Optional[Task]:
        cursor = self.conn.execute("SELECT id, title, completed FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        if row:
            dbo = TaskDBO(id=row['id'], title=row['title'], completed=row['completed'])
            return TaskMapper.to_domain(dbo)
        return None

    def update(self, task: Task) -> Task:
        dbo = TaskMapper.to_dbo(task)
        self.conn.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (dbo.completed, dbo.id)
        )
        self.conn.commit()
        return task

    def find_all(self) -> List[Task]:
        cursor = self.conn.execute("SELECT id, title, completed FROM tasks")
        rows = cursor.fetchall()
        
        tasks = []
        for row in rows:
            dbo = TaskDBO(id=row['id'], title=row['title'], completed=row['completed'])
            tasks.append(TaskMapper.to_domain(dbo))
        return tasks