from pydantic import BaseModel

class TaskResponse(BaseModel):
    session_id: str
    task_id: str
    answers: list[str]
    thought_log: list[str]
    used_tools: list[str]