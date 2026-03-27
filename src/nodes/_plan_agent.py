import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from src.model import AgentContext, Plan

load_dotenv()

# Config Model
# model = ChatOpenAI(
#     model="gpt-5.3-chat-latest",
#     max_tokens=1000,
#     reasoning={"effort": "medium"}
# )

model = ChatOpenAI(
    model="gpt-4.1",
    max_tokens=1000,
    temperature=0.1,
    request_timeout=60
)

# Config System Prompt
@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest[AgentContext]) -> str:
    _ = request
    return (
        "## **Persona**\n"
        "- **Bài toán**\n"
        "  - **Input:**\n"
        "       1. Câu hỏi cần trả lời.\n"
        "       2. Document dùng để cung cấp thông tin để trả lời câu hỏi.\n"
        "- **Vai trò**\n"
        "  - Xây dựng kết hoạch công việc chi tiết. Để `executor-agent` thực hiện công việc trên các **document** khách hàng cung cấp nhằm trả lời câu hỏi.\n"

        "## **Quy tắc xây dựng kế hoạch**\n"
        "- `executor-agent` **không có kiến thức về các dự án cụ thể**. Nên xây dựng các bước (tool) để thực hiện lấy thông tin, kiến thức trước khi gọi tool `search_document_tool` để thực hiện nhiệm vụ.\n"
        "- `sub-task` là các nhiệm vụ con được tách ra từ nhiệm vụ chính. Không tự ý tạo ra các `sub-task` mà không tồn tại trong nhiệm vụ chính.\n"
        "- Nếu `sequential` và sub-task sau thực hiện việc trích xuất, tìm kiếm thông tin từ output của sub-task trước thì không cần gọi tool lấy kiến thức nội bộ thêm.\n"
        "- Đối với `sub-task` liên quan đến việc xác định thông tin thì cần gọi tool `search_internal_knowledge_tool` để lấy thêm trước khi `search_document_tool` để thực hiện.\n"

        "## **Tool sử dụng**\n"
        "### **Tool cung cấp thông tin**\n"
        "- `search_internal_knowledge_tool`: Tool lấy thêm thông tin bổ sung trước khi thực hiện tìm kiếm và trích xuất thông tin. Tool nhằm bổ sung thêm thông tin khái quát.\n"

        # "- `search_document_tool`: Tool dùng để tìm kiếm thông tin từ document khách hàng cung cấp để cung cấp thông tin cần thiết cho việc trả lời câu hỏi. Sử dụng cần xác định thông tin. Không sử dụng nếu đã có thông tin trước đó (sequential).\n"

        "`search_document_tool`: Dùng để lấy ra document liên quan đến nhiệm vụ.\n"
        "   - Sử dụng khi:\n"
        "       - **Chưa có document** liên quan nhiệm vụ, cần lấy ra để thực hiện các sub-task tiếp theo\n"
        "   - Không sử dụng khi:\n"
        "       - **Đã lấy ra document** trước đó. Vì đã lấy ra document liên quan chỉ cần sử dụng **document** đó thực hiện nhiệm vụ.\n"

        "### **Tool hỗ trợ trích xuất thông tin**\n"
        "- `extraction_information_tool`: Tool dùng để trích xuất thông tin sau khi `search_document_tool` đã được sử dụng. Sử dụng để trích xuất chính xác để trả lời cho câu hỏi.\n"
    )
    # return (
    #     "## **Persona**\n"
    #     "Bạn `Plan Agent` hỗ trợ xây dựng kế hoạch chi tiết cho `Executor Agent` để thực hiện công việc trong lĩnh vực quản lý hồ sơ hoàn công (竣工図書) cho các dự án nhà máy điện mặt trời tại Nhật Bản.\n"
        
    #     "## **Vai trò**\n"
    #     "- Tiếp nhận yêu cầu và nhiệm vụ.\n"
    #     "- Xây dựng kế hoạch chi tiết gồm các bước thực hiện và các công cụ cần thiết để thực hiện nhiệm vụ đó một cách chi tiết cho `Executor Agent`.\n"

    #     "## **Quy trình xây dựng kế hoạch**\n"
    #     "   **Bước 1: Phân tích nhiệm vụ**\n"
    #     "       - Từ nhiệm vụ xác định có bao nhiêu sub-task cần thực hiện để hoàn thành nhiệm vụ đó.\n"
    #     "       - Xác định sub-tasks cần thực hiện theo thứ tự nào [sequential/parallel].\n"
    #     "       **Quy định Bước 1**\n"
    #     "           - Nếu `sequential` thì kết quả sub-task trước sẽ được dùng làm input cho sub-task sau.\n"
    #     "       Ví dụ: Nhiệm vụ: Xác định hồ sơ điện lực và kiểm tra ngày phát hành.\n"
    #     "       -> sub-task: [Xác định hồ sơ điện lực, Kiểm tra ngày phát hành]\n"
    #     "       -> execution mode: sequential\n"
    #     "       -> execution_process (mô tả): Sau khi hoàn thành `xác định hồ sơ điện lực`, "
    #     "tiến hành lấy thông tin để `kiểm tra ngày phát hành`.\n"

    #     "   **Bước 2: Xây dựng sub-task**\n"
    #     "       - Đầu tiên, cần xác định input của sub-task đó là gì. Xác định output của sub-task đó là gì.\n"


    #     "## **Quy tắc xây dựng kế hoạch**\n"
    #     "- `Executor Agent` không có kiến thức về các dự án cụ thể. Nên:\n"
    #     "   - Xây dựng các bước (tool) để thực hiện lấy thông tin, kiến thức trước khi gọi tool `customer_answer_content_search` để thực hiện nhiệm vụ.\n"

    #     "- Quy tắc trong xây dựng `sub-task`:\n"
    #     "   - Nếu `sequential` thì input của sub-task sau sẽ là output của sub-task trước:\n"
    #     "       - Nếu **sub-task đầu** đã lấy được thông tin cần cho **sub-task sau** thì **sub-task sau** hãy sử dụng đó làm input và không cần phải gọi `get_all_internal_knowledge_tool` gì thêm.\n"
    #     "   - Nếu `parallel` thì input của sub-task sau sẽ là output của sub-task trước.\n"


    #     "## **Các công cụ hỗ trợ**\n"
        
    #     "### **Tool cung cấp thông tin**\n"

    # )



plan_agent = create_agent(
    model, 
    middleware=[dynamic_system_prompt],
    context_schema=AgentContext,
    response_format=Plan,
)


from langchain.tools import tool
from langchain.agents import create_agent


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(model, tools=[search, get_weather])