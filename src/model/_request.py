from pydantic import BaseModel

class ResourceInfo(BaseModel):
    file_path: str
    file_type: str

class TaskRequest(BaseModel):
    task_id: str
    prompt_template: str
    resource_count: int
    resources_info: list[ResourceInfo]
