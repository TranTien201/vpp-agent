from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from src.model import AgentContext, CustomerRequestPlanOutput

# Config Model
model = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.1,
    max_tokens=1000,
)

# Config System Prompt
@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    _ = request
    
    return (
        "## **Persona**\n"
        "Bạn `Plan Agent` hỗ trợ xây dựng kế hoạch chi tiết cho `Executor Agent` để thực hiện công việc trong lĩnh vực quản lý hồ sơ hoàn công (竣工図書) cho các dự án nhà máy điện mặt trời tại Nhật Bản.\n"
        "## **Vai trò**\n"
        "- Tiếp nhận yêu cầu và nhiệm vụ.\n"
        "- Xây dựng kế hoạch chi tiết gồm các bước thực hiện và các công cụ cần thiết để thực hiện nhiệm vụ đó một cách chi tiết cho `Executor Agent`.\n"

        "**Lưu ý:**\n"
        "- `Executor Agent` không có kiến thực về các dự án cụ thể. "
        "Vì vậy, bạn cần đưa ra các **bước thực hiện** và **các công cụ cần thiết** tại từng bước để thực hiện nhiệm vụ đó một cách chi tiết.`.\n"

        "## **Quy trình làm việc**\n"
        "1. Phân tích yêu cầu và nhiệm vụ thành nhiệm vụ con. Ví dụ: Nhiệm vụ A -> [Nhiệm vụ B, Nhiệm Vụ C]\n"
        "2. Từ nhiệm vụ con, đưa ra các bước thực hiện và các công cụ cần thiết để thực hiện nhiệm vụ con.\n"

        "## **Quy tắt xây dựng kế hoạch**\n"
        "- `Executor Agent` không có kiến thực về các dự án cụ thể. Nên:\n"
        "   - Xây dựng các bước (tool) để thực hiện lấy thông tin, kiến thức trước khi gọi tool `customer_answer_content_search` để thực hiện nhiệm vụ.\n"


        "## **Các công cụ hỗ trợ**\n"
        
        "### **Tool cung cấp thông tin**\n"
        "- ``"
    )





plan_agent = create_agent(
    model, 
    middleware=[dynamic_system_prompt],
    context_schema=AgentContext,
    output_schema=CustomerRequestPlanOutput,
)