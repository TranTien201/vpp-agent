import logging
import json
from typing import cast
from src.model import TaskRequest, Plan, SubTask, AgentContext
from src.nodes import plan_agent, executor_agent
from langchain.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.messages.base import BaseMessage

logger = logging.getLogger(__name__)

class Setting():

    pass


def create_message_for_update_plan(sub_task: SubTask) -> list[BaseMessage]:
    steps = sub_task.steps
    first_step_name = steps[0].step_name

    steps[0].status = "in_progress"

    steps_execution = [step.model_dump() for step in steps]

    args = {
        "steps": steps_execution,
        "update_type": "update_task_status",
        "reason": f"Bắt đầu thực hiện nhiệm vụ: {first_step_name}"
    }

    content = {
        "steps": steps_execution,
        "progress": f"0/{len(steps)}",
        "current_step": first_step_name
    }

    tool_call_message = AIMessage(
        content="",
        id="__fake_id__",
        tool_calls=[
            {"name": "update_plan", "args": args, "id": "__fake_tool_call_id__", "type": "tool_call"}
        ],
        invalid_tool_calls=[]
    )

    tool_return_message = ToolMessage(
        content=json.dumps(content),
        name="update_plan",
        id="__fake_id__",
        tool_call_id="__fake_tool_call_id__",
    )

    return [tool_call_message, tool_return_message]


def create_message_for_create_plan(sub_task: SubTask) -> list[BaseMessage]:

    query = sub_task.task_name
    steps = sub_task.steps

    task_message = HumanMessage(content=sub_task.task_name)
    
    # Tạo tin nhắn gọi tool để tạo plan
    tool_call_create_plan_message = AIMessage(
        content="",
        id="__fake_id__",
        tool_calls=[
            {"name": "create_plan", "args": {"query": query}, "id": "__fake_tool_call_id__", "type": "tool_call"}
        ],
        invalid_tool_calls=[]
    )

    content = {
        "steps": [step.model_dump() for step in steps],
        "progress": f"0/{len(steps)}"
    }
    
    tool_return_create_plan_message = ToolMessage(
        content=json.dumps(content),
        name="create_plan",
        id="__fake_id__",
        tool_call_id="__fake_tool_call_id__",
    )

    return [task_message, tool_call_create_plan_message, tool_return_create_plan_message]
    

def prepare_sub_task(plan_response: Plan, sub_task: SubTask) -> tuple[list[BaseMessage], AgentContext]:
    agent_context = AgentContext(
        plan=plan_response,
        current_task=sub_task,
        current_tool_enabled=sub_task.steps[0].used_tools
    )
    
    messages = create_message_for_create_plan(sub_task) + create_message_for_update_plan(sub_task)
    return messages, agent_context


def run_workflow(
    task_request: TaskRequest
):
    
    # Xử lý dữ liệu


    # Run Agent
    user_message = HumanMessage(content=task_request.prompt_template)

    # Tạo plan
    plan_result = plan_agent.invoke(
        user_message
    )

    plan_response_dict = plan_result.get("plan_response", {})
    if not plan_response_dict:
        logger.error("No plan response received from the agent.")
        return

    plan_response = cast(Plan, plan_response_dict)

    # Từ kết quả Plan thực hiện từng Sub-Task
    for _, sub_task in enumerate(plan_response.sub_task):

        # Thực hiện
        messages, agent_context = prepare_sub_task(plan_response, sub_task)

        executor_result = executor_agent.invoke(
            messages, context=agent_context
        )

    # Thực hiện theo từng task
    