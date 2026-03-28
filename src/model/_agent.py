from pydantic import BaseModel, Field
from typing import Any, Literal
from ._plan import Step, ValidationStep, PlanStep

class ExecutorAgentResponse(BaseModel):
    answers: list[dict[str, Any]] | None = Field(
        default=None,
        description=(
            "Đáp án cuối cùng của nhiệm vụ. Định dạng theo `final_output_template` của plan.\n"
            "Để trống nếu `progress` là `in_progress`.",
        ),
    )

    progress: Literal["in_progress", "completed"] = Field(
        default="in_progress",
        description=(
            "- `in_progress`: nếu chưa phải đáp án cuối và chưa đúng định dạng `final_output_template` của plan."
            "- `completed`: nếu đã đáp án cuối và đúng định dạng `final_output_template` của plan."
        ),
    )

    next_step: str | None = Field(
        default=None,
        description=(
            "Bước tiếp theo cần thực hiện. Chỉ điền khi `progress` là `in_progress`.",
        ),
    )


class ValidatorAgentResponse(BaseModel):
    """
    Kết quả kiểm tra sau mỗi bước thực thi.
    """
    status: Literal["pass", "retry", "replan"] = Field(
        ...,
        description=(
            "- `pass`: kết quả hợp lệ, tiếp tục bước tiếp theo.\n"
            "- `retry`: kết quả chưa đạt, thử lại bước hiện tại với gợi ý bên dưới.\n"
            "- `replan`: cần bổ sung thêm bước vào kế hoạch trước khi tiếp tục.\n"
        ),
    )
    issues: list[str] = Field(
        default_factory=list,
        description="Danh sách các vấn đề phát hiện được. Để trống nếu `status` là `pass`.",
    )
    retry_hint: str | None = Field(
        default=None,
        description="Gợi ý cách thử lại. Chỉ điền khi `status` là `retry`.",
    )
    suggested_steps: list[Step] = Field(
        default_factory=list,
        description="Các bước bổ sung đề xuất. Chỉ điền khi `status` là `replan`.",
    )


class PlanAgentResponse(BaseModel):
    # task_name: str = Field(
    #     ...,
    #     description="Tên nhiệm vụ được xác định từ yêu cầu người dùng.",
    # )
    execution_process: str = Field(
        default="",
        description=(
            "Mô tả ngắn gọn quy trình thực hiện để hoàn thành nhiệm vụ."
        ),
    )
    steps: list[PlanStep] = Field(
        default_factory=list,
        description=(
            "- Danh sách các bước (steps) cần thực hiện để hoàn thành nhiệm vụ.\n"
            "- Mỗi bước chỉ đại diện cho một bước thực hiện duy nhất.\n"
        ),
    )
    expected_output: str = Field(
        ...,
        description="Kết quả đầu ra mong đợi sau khi hoàn thành nhiệm vụ.",
    )
    final_output_template: dict[str, Any] = Field(
        ...,
        description=(
            "Định dạng kết quả cuối sau khi hoàn thành nhiệm vụ: dict với key là tên nhiệm vụ "
            "(tiếng Anh), value là mô tả đầu ra mong đợi.\n"
            "Ví dụ yêu cầu người dùng: xác định phiếu kết quả thử nghiệm và kiểm tra điện trở cách điện.\n"
            'Template mẫu: {"Identify test report": "...", "Check insulation resistance": "..."}'
        ),
    )
