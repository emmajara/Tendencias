from dataclasses import dataclass

@dataclass
class TaskDBO:
    id: int
    title: str
    completed: bool