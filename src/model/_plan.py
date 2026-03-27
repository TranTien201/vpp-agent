from typing import Literal

from pydantic import BaseModel, Field

class Step(BaseModel):
    """
    Đại diện cho một bước thực hiện duy nhất.
    """
    step_expected_input: str | None = Field(
        default=None,
        description=(
            "Thông tin đầu vào của bước để thực hiện nhiệm vụ.\n"
        )
    )
    step_name: str = Field(
        ...,
        description="Tên nhiệm vụ con cần thực hiện để hoàn thành nhiệm vụ nhỏ.",
    )
    step_expected_output: str = Field(
        ...,
        description="Kết quả đầu ra mong đợi sau khi hoàn thành bước.",
    )
    used_tools: list[str] = Field(
        default_factory=list,
        description=(
            "Dựa vào input và nhiệm vụ. Xem xét có nên sử dụng tool không. Đối với các tool search thông tin thì nếu dã có thông tin trước đó thì không cần sử dụng thêm.\n"
        ),
    ),
    status: Literal["pending", "in_progress", "completed", "retry"] = Field(
        default="pending",
        description="Trạng thái của bước.",
    )


class SubTask(BaseModel):
    """
    Nhiệm vụ nhỏ được tách ra từ yêu cầu/nhiệm vụ của khách hàng.
    """
    task_name: str = Field(
        ...,
        description="Tên nhiệm vụ nhỏ được tách ra từ yêu cầu của khách hàng.",
    )
    
    steps: list[Step] = Field(
        default_factory=list,
        description="Danh sách bước (steps) cần thực hiện để hoàn thành sub-task. Mỗi bước chỉ đại diện cho một bước thực hiện duy nhất.",
    )
    
    execution_input: str | None = Field(
        default=None,
        description=(
            "Thông tin đầu vào của sub-task để thực hiện nhiệm vụ.\n"
            "- Nếu `sequential` thì input của sub-task sau sẽ là output của sub-task trước.\n"
            "- Nếu là task đầu tiên thì không cần input vì đã có thông tin từ yêu cầu của khách hàng."
        )
    )
    expected_output: str = Field(
        ...,
        description="Kết quả đầu ra mong đợi sau khi hoàn thành nhiệm vụ.",
    )
    
    execution_process: str = Field(
        default="",
        description=(
            "Mô tả quy trình thực hiện để hoàn thành nhiệm vụ."
        ),
    )


class Plan(BaseModel):
    task_summary: str = Field(
        ...,
        description="Mô tả tổng quan về nhiệm vụ cần thực hiện.",
    )
    tasks_execution_mode: Literal["sequential", "parallel"] = Field(
        default="sequential",
        description=(
            "Chế độ thực thi cho toàn bộ danh sách `sub_tasks` trong response.\n"
            "- `sequential`: output của sub_task trước sẽ được dùng làm input cho sub_task sau.\n"
            "- `parallel`: thực hiện các sub_task không phụ thuộc lẫn nhau."
        ),
    )
    sub_task: list[SubTask] = Field(
        default_factory=list,
        description="Danh sách các sub-task được tách ra từ yêu cầu của khách hàng. Các sub-task cần được thực hiện để hoàn thành nhiệm vụ của khách hàng.",
    )
    nums_sub_task: int = Field(
        default=0,
        description="Số lượng sub-task được tách ra từ yêu cầu của khách hàng.",
    )


class PlanExecutionParams(BaseModel):
    steps: list[Step] = Field(
        ...,
        description="Danh sách các bước cần thực hiện để hoàn thành nhiệm vụ.",
    )
    update_type: Literal["update_task_status", "add_new_task"] = Field(
        default="update_task_status",
        description=(
            "- `update_task_status`: chỉ đổi trạng thái công việc.\n"
            "- `add_new_task`: có công việc phát sinh cần bổ sung task mới vào plan."
        ),
    )
    reason: str = Field(
        ...,
        description=(
            "Mô tả ngắn gọn lý do cần cập nhập."
        ),
    )