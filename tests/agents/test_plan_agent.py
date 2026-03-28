import pytest
from rich.pretty import pprint
from src.nodes import plan_agent
from src.workflow.plan_workfolw_v1 import prepare_execute_step
from src.model import PlanAgentResponse
from typing import cast

@pytest.mark.asyncio
async def test_plan_agent():
    
    user_message = {"messages": [{"role": "user", "content": "Xác định hồ sơ điện lực và kiểm tra ngày phát hành."}]}
    result = plan_agent.invoke(user_message)

    print("--------------------------------")
    pprint(result)

    assert result.get("structured_response") is not None

@pytest.mark.asyncio
async def test_plan_agent_and_prepare_execute_step():
    user_message = {"messages": [{"role": "user", "content": "Xác định hồ sơ điện lực và kiểm tra ngày phát hành."}]}

    result = plan_agent.invoke(user_message)

    messages_history = result.get("messages", [])
    plan_response = cast(PlanAgentResponse, result.get("structured_response"))

    messages, agent_context = prepare_execute_step(plan_response, messages_history)

    pprint(messages)