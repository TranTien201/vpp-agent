from pydoc import describe
from typing import Literal

from pydantic import BaseModel, Field


class SubTaskOutput(BaseModel):
    sub_task_name: str = Field(
        ...,
        description="Tên nhiệm vụ con cần thực hiện để hoàn thành nhiệm vụ nhỏ.",
    )
    expected_result: str = Field(
        ...,
        description="Kết quả đầu ra mong đợi sau khi hoàn thành nhiệm vụ.",
    )
    used_tools: list[str] = Field(
        default_factory=list,
        description=(
            "Danh sách các tool được sử dụng để thực nhiệm vụ."
        ),
    )
    status: Literal["pending", "in_progress", "completed", "retry"] = Field(
        default="pending",
        description="Trạng thái của nhiệm vụ.",
    )


class TaskOutput(BaseModel):
    task_name: str = Field(
        ...,
        description="Tên nhiệm vụ nhỏ được tách ra từ yêu cầu của khách hàng.",
    )
    content_types: list[Literal["text", "image", "table", "chart"]] = Field(
        default_factory=list,
        description=(
            "Danh sách loại nội dung có thể hỗ trợ thực hiện nhiệm vụ."
        )
    )
    sub_tasks: list[SubTaskOutput] = Field(
        default_factory=list,
        description="Danh sách các nhiệm vụ con để hoàn thành nhiệm vụ nhỏ.",
    )
    expected_result: str = Field(
        ...,
        description="Kết quả đầu ra mong đợi sau khi hoàn thành nhiệm vụ.",
    )
    


class CustomerRequestPlanOutput(BaseModel):
    customer_request_summary: str = Field(
        ...,
        description="Tóm tắt ngắn gọn và chính xác yêu cầu chính của khách hàng.",
    )
    business_goal: str = Field(
        ...,
        description="Mục tiêu nghiệp vụ mà khách hàng muốn đạt được sau khi xử lý yêu cầu.",
    )
    tasks: list[TaskOutput] = Field(
        default_factory=list,
        description="Danh sách các nhiệm vụ nhỏ được lập kế hoạch từ yêu cầu khách hàng.",
    )