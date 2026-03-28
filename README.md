# vpp-agent

Dự án **vpp-agent** là ứng dụng Python dùng [LangChain](https://python.langchain.com/) xây dựng các agent (đặc biệt **plan-agent** và **executor-agent**) phục vụ quy trình lập kế hoạch và thực thi nhiệm vụ trên tài liệu trong bối cảnh quản lý hồ sơ hoàn công (竣工図書), ví dụ dự án điện mặt trời tại Nhật Bản.

- **Plan agent** (`src/nodes/_plan_agent.py`): nhận yêu cầu người dùng, sinh kế hoạch có cấu trúc (`PlanAgentResponse`) qua mô hình OpenAI.
- **Workflow** (`src/workflow/plan_workfolw_v1.py`): chuẩn bị bước thực thi đầu tiên (`prepare_execute_step`) và vòng lặp gọi executor (async).
- **Cấu hình** (`src/_settings.py`): đọc biến môi trường qua `pydantic-settings` và file `.env`.

## Yêu cầu hệ thống

- **Python**: `3.11.15` (đúng phiên bản khai báo trong `pyproject.toml`).
- **Poetry**: quản lý dependency và virtualenv (khuyến nghị).

## Cài đặt

### 1. Clone và vào thư mục dự án

```bash
cd /path/to/vpp-agent
```

### 2. Cài dependency (kèm nhóm test)

```bash
poetry install --with test
```

Lệnh này cài các gói chính (LangChain, LangChain OpenAI, Pydantic Settings, python-dotenv, Rich, …) và gói test (`pytest`, `pytest-asyncio`, …).

### 3. Biến môi trường

Tạo file **`.env`** ở thư mục gốc dự án (cùng cấp với `pyproject.toml`) với ít nhất:

```env
OPENAI_API_KEY=sk-...
```

Ứng dụng và test đều dùng khóa này qua `python-dotenv` (`tests/conftest.py` gọi `load_dotenv()` khi pytest khởi động).

### 4. (Tuỳ chọn) Chạy thử nhanh plan agent

```bash
poetry run python -m src.main
```

Script gọi `plan_agent.invoke` với một câu hỏi mẫu và in kết quả bằng Rich.

---

## Hướng dẫn test — `tests/agents/test_plan_agent.py`

Cấu hình pytest nằm trong `pyproject.toml` (`asyncio_mode = "auto"`, …). Test trong file này là **tích hợp thực tế**: gọi API OpenAI qua LangChain, cần **mạng** và **`OPENAI_API_KEY` hợp lệ**.

### Chạy toàn bộ file

```bash
poetry run pytest tests/agents/test_plan_agent.py -v
```

### Chạy một test cụ thể

```bash
poetry run pytest tests/agents/test_plan_agent.py::test_plan_agent -v
poetry run pytest tests/agents/test_plan_agent.py::test_plan_agent_and_prepare_execute_step -v
```

### Xem output in ra (Rich / print)

```bash
poetry run pytest tests/agents/test_plan_agent.py -v -s
```

(`-s` tắt capture stdout để thấy `print` và `pprint`.)

### Nội dung hai test

| Test | Mô tả ngắn |
|------|------------|
| `test_plan_agent` | Gọi `plan_agent.invoke` với `HumanMessage`; kiểm tra `structured_response` khác `None`. |
| `test_plan_agent_and_prepare_execute_step` | Gọi `plan_agent.invoke` với dict dạng `{"messages": [{"role": "user", "content": "..."}]}`; lấy `PlanAgentResponse` và `messages`; gọi `prepare_execute_step` từ `plan_workfolw_v1` để kiểm tra chuỗi tin nhắn và `AgentContext` cho bước thực thi. |

Nếu thiếu API key hoặc lỗi mạng / quota OpenAI, các test sẽ thất bại ở bước gọi model.

---

## Cấu trúc mã nguồn (tóm tắt)

| Đường dẫn | Vai trò |
|-----------|---------|
| `src/main.py` | Entry chạy thử plan agent |
| `src/nodes/` | Định nghĩa `plan_agent`, `executor_agent` |
| `src/workflow/plan_workfolw_v1.py` | Workflow plan → chuẩn bị executor |
| `src/model/` | Pydantic models (plan, request, response, context, …) |
| `src/tools/` | Công cụ plan / business / validate |
| `src/middleware/` | Middleware cho agent |
| `tests/conftest.py` | `load_dotenv()` cho toàn bộ phiên pytest |
| `tests/agents/test_plan_agent.py` | Test plan agent và `prepare_execute_step` |

## Giấy phép

MIT (theo `pyproject.toml`).
