from typing import Literal
from pydantic import BaseModel, Field
from src.constants import CategoryNameJAPANESE

ContentType = Literal["text", "image", "table", "chart", "all"]

class BusinessFieldRequest(BaseModel):
    field_name: str = Field(
        ...,
        description=(
            "Nội dung thông tin cần trích xuất."
        ),
    )
    content_types: list[ContentType] = Field(
        default_factory=lambda: ["all"],
        description=(
            "Loại nội dung cần kiểm tra/trích xuất cho trường này. Có thể chọn nhiều loại.\n"
            "Với thông tin hỗ trợ mỗi loại như sau, mặc định là 'all':\n"
            "   - text: Trích xuất thông tin, thông số, ngày giờ, nội dung, mục lục, chỉ mục, hướng dẫn...\n"
            "   - image: Hình ảnh, liên qua đến bản như bản vẽ, bản thiết kế, bản hoàn công...\n"
            "   - table: Bảng dữ liệu, số liệu, bản vẽ, bản hoàn công, bản thiết kế...\n"
            "   - chart: Biểu đồ, sơ đồ, đồ thị, hình ảnh...\n"
        ),
    )


class BusinessSearchParams(BaseModel):
    information_to_extract: list[BusinessFieldRequest] = Field(
        default_factory=list,
        description=(
            "Danh sách các trường thông tin cần trích xuất kèm các loại nội dung tương ứng "
            "trong internal."
        ),
    )


class SelectedCategoryInstructionsParams(BaseModel):
    categories: list[CategoryNameJAPANESE] = Field(
        ...,
        min_length=1,
        description=(
            "Danh sách các thành phần trong nhiệm vụ cần lấy hướng dẫn để làm rõ hơn cho nhiệm vụ đó."
        ),
    )