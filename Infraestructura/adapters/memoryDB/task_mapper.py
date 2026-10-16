from domain.model.task.task import Task
from .task_dbo import TaskDBO

class TaskMapper:
    @staticmethod
    def to_domain(dbo: TaskDBO) -> Task:
        return Task(
            id=dbo.id_db,
            title=dbo.title_db,
            completed=dbo.is_done
        )

    @staticmethod
    def to_dbo(domain_model: Task) -> TaskDBO:
        return TaskDBO(
            id=domain_model.id,
            title=domain_model.title,
            completed=domain_model.completed
        )