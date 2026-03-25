from pydantic import BaseModel, Field


class AgentContext(BaseModel):
    enable_tool: list[str] = Field(description="Danh sách các tool được sử dụng tại bước này")

    agent_turn_log: list[str]