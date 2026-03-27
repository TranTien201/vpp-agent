from calendar import c
from langchain.tools import tool, ToolRuntime
from src.model import AgentContext, Step, PlanExecutionParams
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
    steps: list[Step], 
    update_type: Literal["update_task_status", "add_new_task"], 
    reason: str,
    runtime: ToolRuntime[AgentContext],
) -> str:
    _ = update_type
    _ = reason

    runtime.context.current_task.steps = steps
    current_step = None
    

    nums_completed = 0
    for step in steps:
        if step.status == "completed":
            nums_completed += 1

        if step.status == "in_progress":
            current_step = step.step_name
            runtime.context.current_tool_enabled = step.used_tools
            break

    progress = f"{nums_completed}/{len(steps)}"

    content = {
        "steps": [step.model_dump() for step in steps],
        "progress": progress,
        "current_step": current_step
    }

    return content