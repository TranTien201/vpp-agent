from src.nodes._plan_agent import plan_agent


result = plan_agent.invoke(
    {"messages": [{"role": "user", "content": "Xác định hồ sơ điện lực và kiểm tra ngày phát hành."}]}
)


from rich.pretty import pprint
pprint(result)