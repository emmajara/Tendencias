from domain.model.task.task import Task
from .task_dbo import TaskDBO

class TaskMapper:
    @staticmethod
    def to_domain(dbo: TaskDBO) -> Task:
        return Task(
            id=dbo.id,
            title=dbo.title,
            completed=bool(dbo.completed)  # Convierte int a bool
        )

    @staticmethod
    def to_dbo(domain_model: Task) -> TaskDBO:
        return TaskDBO(
            id=domain_model.id,
            title=domain_model.title,
            completed=1 if domain_model.completed else 0  # Convierte bool a int
        )