from langchain.tools import tool
from src.model import AgentContext
from langchain.tools import ToolRuntime

@tool(
    "extraction_information_tool",
    description="Tool dùng để trích xuất thông tin cần thiết từ document đã lấy.",
)
async def extraction_information_tool(
    query: str,
    runtime: ToolRuntime[AgentContext]
) -> str:
    pass