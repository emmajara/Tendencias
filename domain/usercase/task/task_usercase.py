from ...model.task.task import Task
from ...model.task.gateways.task_repository import TaskRepository

class TaskUseCase:
    def __init__(self, task_repository: TaskRepository):        
        self.task_repository = task_repository

    def create_task(self, title: str) -> Task:
        if not title or len(title.strip()) < 3:
            raise ValueError("El título debe tener al menos 3 caracteres.")
        
        new_task = Task(id=0, title=title.strip(), completed=False)
        return self.task_repository.save(new_task)

    def complete_task(self, task_id: int) -> Task:
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise LookupError(f"La tarea con ID {task_id} no existe.")
        
        task.completed = True
        return self.task_repository.update(task)

    def get_all_tasks(self) -> list[Task]:
        return self.task_repository.find_all()