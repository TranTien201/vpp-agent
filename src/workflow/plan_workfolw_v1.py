import logging
from typing import cast
from src.model import TaskRequest, Plan
from src.nodes import plan_agent

logger = logging.getLogger(__name__)

class Setting():

    pass


def run_workflow(
    task_request: TaskRequest
):
    
    # Xử lý dữ liệu


    # Run Agent
    prompt_template = task_request.prompt_template
    
    user_message = {"messages": [{"role": "user", "content": prompt_template}]}

    # Tạo plan
    plan_result = plan_agent.invoke(
        user_message
    )
    
    plan = cast(Plan, plan_result.get("structured_response"))

    prepare_plan = ""

    for i, sub_task in enumerate(plan.sub_task):
        logger.info(f"Sub Task {i+1}: {sub_task.task_name}")

        prepare_plan += (
            f"- **Tổng quan công việc:** {sub_task.execution_process}\n"
            "" if not sub_task.execution_input else f"- **Dữ liệu đầu vào:** {sub_task.execution_input}\n"
            f"- **Kết quả mong muốn:** {sub_task.expected_output}"
            "Công việc cần thực hiện:\n"
        )


    # Thực hiện theo từng task
    