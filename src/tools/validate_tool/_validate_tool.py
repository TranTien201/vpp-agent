from langchain.tools import tool
from src.model import AgentContext
from langchain.tools import ToolRuntime

@tool(
    "validate_step_tool",
    description="Tool dùng để kiểm tra tính hợp lệ của kết quả sau các bước tìm kiếm và trích xuất thông tin.",
)
async def validate_step_tool(
    runtime: ToolRuntime[AgentContext]
) -> str:
    pass