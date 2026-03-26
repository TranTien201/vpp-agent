import json
from typing import Any

from langchain.tools import tool, ToolRuntime

from src.model import AgentContext, BusinessSearchParams, BusinessFieldRequest, SelectedCategoryInstructionsParams
from src.tools.business_tool._utils import _load_sort_folders_ja_items
from src.constants import CategoryNameJAPANESE


@tool(
    "get_all_internal_knowledge_tool",
    description=(
        "Tool dùng để lấy tất cả hướng dẫn, mô tả chi tiết thông tin trong bài toán phân loại.\n"
        "**Sử dụng khi:**\n"
        "   - Các bài toán sắp xếp dựa vào nội dung của tài liệu"
    ),
)
def get_category_instructions() -> list[dict[str, str | None]]:
    return _load_sort_folders_ja_items()


@tool(
    "get_selected_internal_knowledge_tool",
    args_schema=SelectedCategoryInstructionsParams,
    description=(
        "Tool dùng để lấy kiến thức, mô tả chi tiết về các thành phần bên trong nhiệm vụ cần thực hiện.\n"
        "Tool dùng bổ sung thông tin trước khi thực hiện gọi tool tìm kiếm và trích xuất thông tin để thực hiện nhiệm vụ.\n"
        "**Sử dụng trong các nhiệm vụ:**\n"
        "   - Nhiệm vụ cần trích xuất, kiểm tra thông tin.\n"
        "   - Xác định thông tin, lấy thông tin, kiểm tra thông tin.\n"
        "   - Kiểm tra thông tin sau khi đã phân loại tài liệu"
    ),
)
def get_selected_category_instructions(
    categories: list[CategoryNameJAPANESE], runtime: ToolRuntime[AgentContext]
) -> dict[str, Any]:
    order = {name: idx for idx, name in enumerate(categories)}
    items: list[dict[str, str | None]] = sorted(
        (
            row
            for row in _load_sort_folders_ja_items()
            if row.get("name") in order
        ),
        key=lambda r: order[str(r["name"])],
    )

    return {
        "source": "sort_folders_ja.json",
        "categories": categories,
        "items": items,
    }

########

@tool(
    "search_internal_knowledge_tool",
    args_schema=BusinessSearchParams,
    description=(
        "Tool dùng để tìm kiếm, trích xuất thông tin từ nội dung nội bộ để trả lời câu hỏi khách hàng.\n"
        "Giúp cung cấp dữ liệu cần thiết (text/image/table/chart) trước khi tổng hợp câu trả lời.\n"
        "**Sử dụng khi:**\n"
        "   - Cần trả lời câu hỏi của khách hàng dựa trên tài liệu/nội dung nội bộ.\n"
        "   - Cần kiểm tra/xác minh thông tin trước khi trả lời.\n"
        "**Không sử dụng khi:**\n"
        "   - Chỉ cần phân loại/sắp xếp tài liệu (không phải tra cứu để trả lời câu hỏi).\n"
    )
)
async def search_internal(
    information_to_extract: BusinessFieldRequest,
    runtime: ToolRuntime[AgentContext]
) -> str:

    requested_fields = information_to_extract or [
        BusinessFieldRequest(field_name="plan_summary")
    ]

    extracted: dict[str, dict[str, str]] = {}

    all_types = ["text", "image", "table", "chart"]
    for req in requested_fields:
        # Nếu yêu cầu có 'all' thì trả về đủ các loại; ngược lại chỉ trả các loại được chọn.
        if "all" in req.content_types:
            types_to_return = all_types
        else:
            types_to_return = [t for t in req.content_types if t != "all"]

        extracted[req.field_name] = {
            t: f"dummy_{t}_value_for_{req.field_name}" for t in types_to_return
        }

    payload = {
        "internal": "dummy_internal_content",
        "requested_information": [
            {"field_name": req.field_name, "content_types": req.content_types}
            for req in requested_fields
        ],
        "extracted": extracted,
        "notes": [
            "Chưa thực hiện truy vấn internal thật.",
            "Thay giá trị dummy bằng logic truy xuất internal sau.",
        ],
    }

    return json.dumps(payload, ensure_ascii=True)


# @tool(
#     "load_"
# )
# def load_internal(runtime: ToolRuntime[AgentContext]) -> dict[str, Any]:

#     pass