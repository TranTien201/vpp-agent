from pydantic import BaseModel, Field
from src.model import Plan, SubTask


class AgentContext(BaseModel):
    plan: Plan = Field(description="Kế hoạch công việc được xây dựng bởi `Plan Agent`")
    
    current_task: SubTask = Field(description="Công việc hiện tại đang được thực hiện")
    current_tool_enabled: list[str] = Field(
        description="Danh sách các tool được sử dụng tại bước này",
        default_factory=list
    )

    agent_turn_log: list[str]