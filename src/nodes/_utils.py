import json

from src.model import PlanAgentResponse
from src.model._plan import Step, ValidationStep


def build_executor_plan_prompt(plan: PlanAgentResponse) -> str:
    lines: list[str] = [
        f"- **Tổng quan công việc:** {plan.execution_process}",
    ]

    lines.extend(
        [
            f"- **Kết quả mong muốn:** {plan.expected_output}",
            f"- **Định dạng kết quả:** {json.dumps(plan.final_output_template)}",
            "Công việc cần thực hiện:",
        ]
    )

    for i, step in enumerate(plan.steps, start=1):
        if isinstance(step, ValidationStep):
            lines.append(f"- {i}. Validation Step: {step.step_name}")
            lines.append(f"  - **Validation criteria:** {step.validation_criteria}")
            lines.append(f"  - **Used Tools:** {', '.join(step.used_tools)}")
            lines.append(f"  - **Task Status:** {step.status}")
            continue

        assert isinstance(step, Step)
        lines.append(f"- {i}. Step: {step.step_name}")
        if step.step_expected_input:
            lines.append(f"  - **Expected Input:** {step.step_expected_input}")
        lines.append(f"  - **Expected Result:** {step.step_expected_output}")
        lines.append(f"  - **Used Tools:** {', '.join(step.used_tools)}")
        lines.append(f"  - **Task Status:** {step.status}")

    return "\n".join(lines)