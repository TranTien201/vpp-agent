import json

from langchain.tools import tool, ToolRuntime

from src.model import AgentContext, PlanExecutionParams, PlanStep


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
    steps: list[PlanStep],
    runtime: ToolRuntime[AgentContext],
) -> str:
    runtime.context.plan.steps = list(steps)

    current_step_name: str | None = None
    nums_completed = 0
    in_progress: PlanStep | None = None

    for step in steps:
        if step.status == "completed":
            nums_completed += 1

        if step.status == "in_progress":
            current_step_name = step.step_name
            runtime.context.current_tool_enabled = list(step.used_tools)
            in_progress = step
            break

    if in_progress is not None:
        runtime.context.current_step = in_progress

    progress = f"{nums_completed}/{len(steps)}"

    content = {
        "steps": [step.model_dump() for step in steps],
        "progress": progress,
        "current_step": current_step_name,
    }

    return json.dumps(content, ensure_ascii=False)


@tool(
    "replan",
    description="Tool dùng để cập nhật kế hoạch công việc.",
)
def replan(
    runtime: ToolRuntime[AgentContext]
) -> str:

    pass
