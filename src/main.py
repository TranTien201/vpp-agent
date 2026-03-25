from _settings import settings
from src.nodes._plan_agent import plan_agent


result = plan_agent.invoke(
    {"input": "What is the customer database?"},
    context={
        "user_tier": "premium",
        "language": "vi",
    },
)

from rich.pretty import pprint
pprint(result)