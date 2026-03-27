from src.model import SubTask

def build_executor_plan_prompt(sub_task: SubTask) -> str:
    lines: list[str] = [
        f"- **Tổng quan công việc:** {sub_task.execution_process}",
    ]

    if sub_task.execution_input:
        lines.append(f"- **Dữ liệu đầu vào:** {sub_task.execution_input}")

    lines.extend(
        [
            f"- **Kết quả mong muốn:** {sub_task.expected_output}",
            "Công việc cần thực hiện:",
        ]
    )

    for i, step in enumerate(sub_task.steps, start=1):
        lines.append(f"- {i}. Task: {step.step_name}")
        if step.step_expected_input:
            lines.append(f"  - **Expected Input:** {step.step_expected_input}")
        lines.append(f"  - **Expected Result:** {step.step_expected_output}")
        lines.append(f"  - **Used Tools:** {', '.join(step.used_tools)}")
        lines.append(f"  - **Task Status:** {step.status}")

    return "\n".join(lines)