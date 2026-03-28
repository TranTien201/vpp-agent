import logging
import json
from typing import cast
from src.model import TaskRequest, PlanAgentResponse, AgentContext, ExecutorAgentResponse
from src.nodes import plan_agent, executor_agent
from langchain.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.messages.base import BaseMessage
from langchain_core.messages.tool import tool_call

logger = logging.getLogger(__name__)

class Setting():

    pass


def create_message_for_update_plan(plan: PlanAgentResponse) -> list[BaseMessage]:
    steps = plan.steps

    first_step = steps[0]
    steps[0].status = "in_progress"

    steps_dump = [step.model_dump() for step in steps]
    content = {
        "steps": steps_dump,
        "progress": f"0/{len(steps)}",
        "current_step": first_step.step_name
    }

    tool_call_message = AIMessage(
        content="",
        id="__fake_id__",
        tool_calls=[
            tool_call(
                name="update_plan",
                args={"steps": steps_dump},
                id="__fake_tool_call_id__",
            )
        ],
        invalid_tool_calls=[]
    )

    tool_return_message = ToolMessage(
        content=json.dumps(content, ensure_ascii=False),
        name="update_plan",
        id="__fake_id__",
        tool_call_id="__fake_tool_call_id__",
    )

    return [tool_call_message, tool_return_message]


# def create_message_for_create_plan(plan: PlanAgentResponse) -> list[BaseMessage]:

#     query = sub_task.task_name
#     steps = sub_task.steps

#     task_message = HumanMessage(content=sub_task.task_name)
    
#     # Tạo tin nhắn gọi tool để tạo plan
#     tool_call_create_plan_message = AIMessage(
#         content="",
#         id="__fake_id__",
#         tool_calls=[
#             {"name": "create_plan", "args": {"query": query}, "id": "__fake_tool_call_id__", "type": "tool_call"}
#         ],
#         invalid_tool_calls=[]
#     )

#     content = {
#         "steps": [step.model_dump() for step in steps],
#         "progress": f"0/{len(steps)}"
#     }
    
#     tool_return_create_plan_message = ToolMessage(
#         content=json.dumps(content),
#         name="create_plan",
#         id="__fake_id__",
#         tool_call_id="__fake_tool_call_id__",
#     )

#     return [task_message, tool_call_create_plan_message, tool_return_create_plan_message]
    

def prepare_execute_step(plan_response: PlanAgentResponse, messages: list[BaseMessage]) -> tuple[list[BaseMessage], AgentContext]:

    first_step = plan_response.steps[0]
    final_output_template = plan_response.final_output_template

    agent_context = AgentContext(
        plan=plan_response,
        current_step=first_step,
        current_tool_enabled=first_step.used_tools,
        final_output_template=final_output_template
    )
    
    messages = messages + create_message_for_update_plan(plan_response)
    return messages, agent_context


async def run_workflow(
    task_request: TaskRequest
):
    
    # Xử lý dữ liệu


    # Run Agent
    user_message = {"messages": [{"role": "user", "content": task_request.prompt_template}]}

    # Tạo plan
    plan_result = await plan_agent.ainvoke(
        user_message
    )

    plan_messages_history = plan_result.get("messages", [])
    plan_response_dict = plan_result.get("plan_response", {})
    if not plan_response_dict:
        logger.error("No plan response received from the agent.")
        return

    # Khởi tạo context và message của turn đầu tiên
    plan_response = cast(PlanAgentResponse, plan_response_dict)
    messages, agent_context = prepare_execute_step(plan_response, [user_message] + plan_messages_history)

    # Thực hiện theo từng task
    
    while True:
        executor_result = await executor_agent.ainvoke(
            messages, context=agent_context
        )

        executor_messages_history = executor_result.get("messages", [])
        executor_response_dict = executor_result.get("executor_response", {})
        
        if not executor_response_dict:
            logger.error("No executor response received from the agent.")
            return

        executor_response = cast(ExecutorAgentResponse, executor_response_dict)

        if executor_response.progress == "completed":
            # TODO: Thêm 1 bước validation schema output trước khi tạo kết quả submit
            
            return

        # TODO: Kiểm tra xem thử executor_messages_history đã có chứa messages trước đó chưa.
        next_step = executor_response.next_step
        messages = executor_messages_history + HumanMessage(content=next_step)