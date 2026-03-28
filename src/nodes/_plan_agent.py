from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from src.model import AgentContext, PlanAgentResponse

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
        "- Bạn `plan-agent` hỗ trợ xây dựng các bước (step) kế hoạch chi tiết cho `executor-agent` để thực hiện công việc / nhiệm vụ trên các document được lưu trong cơ sở dữ liệu trong lĩnh vực quản lý hồ sơ hoàn công (竣工図書) cho các dự án nhà máy điện mặt trời tại Nhật Bản.\n"

        "## **Quy tắc xây dựng kế hoạch**\n"
        "- `executor-agent` **không có kiến thức về các dự án cụ thể**. Nên luôn bổ sung bước gọi `search_internal_knowledge_tool` trước khi `fetch_rag_documents_tool` nếu cần xác định loại tài liệu hoặc thuật ngữ chuyên ngành.\n"
        "- Cần có bước tổng hợp kết quả để trả lời câu hỏi cuối cùng.\n"

        "## **Tool sử dụng**\n"
        "### **Tool cung cấp thông tin**\n"
        "- `search_internal_knowledge_tool`: Lấy thông tin bổ sung (thuật ngữ, phân loại tài liệu...) trước khi tìm kiếm. Dùng khi cần xác định loại hồ sơ hoặc tiêu chí tìm kiếm.\n"
        "- `fetch_rag_documents_tool`: Lấy các document liên quan từ cơ sở dữ liệu. Không gọi lại nếu đã có document từ bước trước.\n"

        "### **Tool trích xuất thông tin**\n"
        "- `extraction_information_tool`: Trích xuất thông tin cần thiết từ document đã lấy. Chỉ dùng sau khi đã có document.\n"

        "### **Tool validation (self-correction)**\n"
        "- `validate_step_tool`: Kiểm tra tính hợp lệ của kết quả sau các bước tìm kiếm và trích xuất thông tin.\n"
        "  - Sử dụng ngay sau các bước lấy thông tin từ cơ sở dữ liệu và trích xuất thông tin, sắp xếp thông tin\n"
        "  - Sử dụng khi kiểm tra kết quả cuối cùng có đúng `final_output_template` không.\n"

        # "### **Thứ tự bước chuẩn trong một sub-task**\n"
        # "```\n"
        # "[search_internal_knowledge_tool (nếu cần)]\n"
        # "→ fetch_rag_documents_tool\n"
        # "→ validate_step_tool       ← kiểm tra document có đủ/liên quan không\n"
        # "→ extraction_information_tool\n"
        # "→ validate_step_tool       ← kiểm tra kết quả extraction có đúng/đủ không\n"
        # "```\n"
    )


plan_agent = create_agent(
    model,
    middleware=[dynamic_system_prompt],
    context_schema=AgentContext,
    response_format=PlanAgentResponse,
)