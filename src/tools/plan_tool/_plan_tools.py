from langchain.tools import tool, ToolRuntime
from src.model import AgentContext
from src.model import Plan, PlanExecutionParams
from typing import Literal

@tool(
    "update_plan",
    args_schema=PlanExecutionParams,
    description=(
        "Tool dùng để cập nhật kế hoạch công việc.\n"
        "**Sử dụng khi:**\n"
        "   - Cần đổi trạng thái công việc khi thực hiện xong công việc.\n"
        "   - Cần bổ sung task mới vào plan khi có công việc phát sinh.\n"
        "**Quy tắc:**\n"
        "   - Chỉ có MỘT task ở trạng thái `in_progress` tại một thời điểm.\n"

    ),
)
def update_plan(
    runtime: ToolRuntime[AgentContext],
    plan: Plan, 
    update_type: Literal["update_task_status", "update_new_plan"], 
    reason_update_new_plan: str | None = None,
) -> str:

    return "Cập nhật kế hoạch công việc thành công."