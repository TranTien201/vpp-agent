from typing import Literal, Any

from pydantic import BaseModel, Field


class BaseStep(BaseModel):
    """
    Base class cho các loại step trong plan.
    """
    step_id: str = Field(
        ...,
        description="ID của bước.",
    )
    step_name: str = Field(
        ...,
        description="Tên bước cần thực hiện.",
    )
    used_tools: list[str] = Field(
        default_factory=list,
        description=(
            "Dựa vào input và nhiệm vụ. Xem xét có nên sử dụng tool không. Đối với các tool search thông tin thì nếu dã có thông tin trước đó thì không cần sử dụng thêm.\n"
        ),
    )
    status: Literal["pending", "in_progress", "completed", "retry"] = Field(
        default="pending",
        description=(
            "- `pending`: chưa bắt đầu thực hiện bước.\n"
            "- `in_progress`: đang thực hiện bước.\n"
            "- `completed`: đã hoàn thành bước.\n"
            "- `retry`: cần thực hiện lại bước.\n"
        ),
    )


class Step(BaseStep):
    """
    Đại diện cho một bước thực hiện duy nhất.
    """
    step_id: str = Field(
        ...,
        description="ID của bước. Prefix là `step_`.",
    )
    step_expected_input: str | None = Field(
        default=None,
        description=(
            "- Thông tin đầu vào mong muốn để thực hiện bước đó.\n"
            "- Nếu là bước đầu tiên thì không cần input.\n"
        )
    )
    # depend_on: list[str] = Field(
    #     default_factory=list,
    #     description="Danh sách các bước cần thực hiện trước khi thực hiện bước này.",
    # )
    step_expected_output: str = Field(
        ...,
        description="Kết quả đầu ra mong đợi sau khi hoàn thành bước.",
    )


class ValidationStep(BaseStep):
    """
    Bước kiểm tra (validation) dành riêng cho cơ chế self-correction.
    Luôn đứng ngay sau bước cần kiểm tra trong danh sách steps.
    """
    step_id: str = Field(
        ...,
        description="ID của bước. Prefix là `validate_`.",
    )
    step_name: str = Field(
        ...,
        description="Tên bước kiểm tra. Ví dụ: 'Kiểm tra document tìm được', 'Kiểm tra kết quả trích xuất'.",
    )
    validation_criteria: str = Field(
        ...,
        description=(
            "Yêu cầu và tiêu chí kiểm tra. Mô tả rõ cần kiểm tra điều gì và tại sao.\n"
            "Ví dụ: 'Kiểm tra document có thuộc loại hồ sơ điện lực không, có chứa thông tin ngày phát hành không'.\n"
            "Ví dụ: 'Kiểm tra ngày phát hành đã trích xuất đúng định dạng chưa, có khớp với yêu cầu nhiệm vụ không'."
        ),
    )
    used_tools: list[str] = Field(
        default_factory=lambda: ["validate_step_tool"],
        description=(
            "Tool validation cố định cho bước kiểm tra (self-correction)."
        ),
    )


PlanStep = Step | ValidationStep


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