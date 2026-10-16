from typing import Optional
from domain.model.task.task import Task
from domain.model.task.gateways.task_repository import TaskRepository
from .task_dbo import TaskDBO
from .task_mapper import TaskMapper

class InMemoryTaskRepository(TaskRepository): 
    def __init__(self):
        self._db: dict[int, TaskDBO] = {}
        self._next_id = 1

    def save(self, task: Task) -> Task:
        task.id = self._next_id
        dbo = TaskMapper.to_dbo(task)
        self._db[self._next_id] = dbo
        self._next_id += 1
        return task

    def find_by_id(self, task_id: int) -> Optional[Task]:
        dbo = self._db.get(task_id)
        if not dbo:
            return None
        return TaskMapper.to_domain(dbo)

    def update(self, task: Task) -> Task:
        dbo = TaskMapper.to_dbo(task)
        self._db[task.id] = dbo
        return task

    def find_all(self) -> list[Task]:
        return [TaskMapper.to_domain(dbo) for dbo in self._db.values()]