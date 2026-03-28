from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from src.constants import TOOL_CALL_MAX_RETRIES, TOOL_CALL_RETRY_DELAY_SECONDS
from src.middleware import ExecutorAgentMiddleware
from src.model import AgentContext, ExecutorAgentResponse
from src.nodes._utils import build_executor_plan_prompt
from src.tools import ALL_EXECUTOR_TOOLS

agent_middleware = ExecutorAgentMiddleware(
    max_retries=TOOL_CALL_MAX_RETRIES,
    retry_delay_seconds=TOOL_CALL_RETRY_DELAY_SECONDS,
)

# Config Model
model = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.1,
    max_tokens=1000,
    request_timeout=30
)


@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest[AgentContext]) -> str:

    plan_summary = build_executor_plan_prompt(request.runtime.context.plan)

    return (
        "## **Persona**\n"
        "- Bạn `executor-agent` thực hiện **tuần tự các công việc** theo kế hoạch được xây dựng bởi `plan-agent`.\n"
        "## **Quy tắc**\n"
        "   - Thực hiện các công việc (bước) đã được xây dựng trong kế hoạch theo hướng dẫn và tool đã được cung cấp tương ứng.\n"
        "   - Khi thực hiện xong một công việc thì cần thực hiện gọi tool `update_plan()` để `completed` công việc hiện tại và `in_progress` công việc tiếp theo trong kế hoạch.\n"
        "   - Khi thực hiện `validate` nếu kết quả là `pass` thì gọi tool `update_plan()` để tiếp tục các công việc tiếp. Nhưng với `status` còn lại thì thực hiện bước sau:\n"
        "       - `retry`: gọi tool `update_plan()` để thực hiện lại các công việc trước đó đã hoàn thành với gợi ý `retry_hint` để thực hiện tại công việc.\n"
        "       - `replan`: gọi tool `replan()` để cập nhật kế hoạch mới với các bước bổ sung đề xuất.\n"
        "## **Danh sách nhiệm vụ và hướng dẫn**\n"
        f"{plan_summary}\n"
    )

executor_agent = create_agent(
    model,
    tools=ALL_EXECUTOR_TOOLS,
    middleware=[agent_middleware, dynamic_system_prompt],
    context_schema=AgentContext,
    response_format=ExecutorAgentResponse,
)