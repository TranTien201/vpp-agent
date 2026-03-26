from ._plan_agent import plan_agent
from ._executor_agent import executor_agent
from src.constants import AgentName

AGENT_REGISTRY = {
    AgentName.PLAN_AGENT: plan_agent,
    AgentName.EXECUTE_AGENT: executor_agent
}

def create_agent_by_name(agent_name: str):

    try:
        return AGENT_REGISTRY[agent_name]
    except Exception as e:
        raise Exception(f"Failed to create agent {agent_name}: {e}") from e