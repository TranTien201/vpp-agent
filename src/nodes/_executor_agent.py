from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from src.model import AgentContext, Plan
from src.nodes._utils import build_executor_plan_prompt

# Config Model
model = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.1,
    max_tokens=1000,
    request_timeout=30
)


@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest[AgentContext]) -> str:

    plan_summary = build_executor_plan_prompt(request.runtime.context.current_task)

    return (
        "## **Persona**\n"
        "- Bạn `Executor Agent` thực hiện **tuần tự các công việc** theo kế hoạch được xây dựng bởi `Plan Agent`.\n"
        "## **Quy tắc**\n"
        "- Thực hiện các công việc (bước) đã được xây dựng trong kế hoạch theo hướng dẫn và tool hỗ trợ.\n"
        "- Khi thực hiện xong một công việc thì cần thực hiện gọi tool `update_plan()` để `completed` công việc hiện tại và `in_progress` công việc tiếp theo trong kế hoạch.\n"
        "- Nếu có công việc phát sinh (thiếu thông tin / cần thực hiện thêm bước) thì gọi `update_plan()` để cập nhật kế hoạch mới. Những công việc hoàn thành sẽ không bị ảnh hưởng.\n"
        "- Nếu hoàn thành hết các công việc (step) thì tổng hợp và trả lời theo đúng yêu cầu của nhiệm vụ.\n"
        "## **Danh sách nhiệm vụ và hướng dẫn**\n"
        f"{plan_summary}\n"
    )

executor_agent = create_agent(
    model,
    middleware=[dynamic_system_prompt],
    context_schema=AgentContext,
    tools=[]
)