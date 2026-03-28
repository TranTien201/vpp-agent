from pydantic import BaseModel, Field
from typing import Any
from ._plan import PlanStep
from ._agent import PlanAgentResponse


class AgentContext(BaseModel):
    plan: PlanAgentResponse = Field(description="Kế hoạch công việc được xây dựng bởi `Plan Agent`")
    
    current_step: PlanStep = Field(description="Bước hiện tại đang được thực hiện")
    current_tool_enabled: list[str] = Field(
        description="Danh sách các tool được sử dụng tại bước này",
        default_factory=list
    )

    # agent_turn_log: list[str]

    # Validator và retry agent để kiểm tra định dạng lần cuối.
    final_output_template: dict[str, Any] = Field(
        description="Định dạng của kết quả đầu ra mong đợi sau khi hoàn thành nhiệm vụ.",
        default_factory=dict
    )