import logging
import time
from collections.abc import Callable

from langchain.agents.middleware import AgentMiddleware
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langgraph.types import Command


class BaseMiddleware(AgentMiddleware):
    def __init__(
        self,
        *,
        max_retries: int = 3,
        retry_delay_seconds: float = 1.0,
        logger: logging.Logger | None = None,
    ) -> None:
        super().__init__()
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds
        self._log = logger or logging.getLogger(__name__)
        if max_retries < 1:
            raise ValueError("max_retries must be >= 1")

    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        name = request.tool_call["name"]
        tool_call_id = request.tool_call["id"]
        args = request.tool_call.get("args", {})

        self._log.info(
            "[tool] start name=%r id=%r args=%r",
            name,
            tool_call_id,
            args,
        )

        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                result = handler(request)
                self._log.info(
                    "[tool] success name=%r attempt=%s/%s",
                    name,
                    attempt,
                    self.max_retries,
                )
                return result
            except Exception as exc:
                last_error = exc
                self._log.warning(
                    "[tool] error name=%r attempt=%s/%s: %s",
                    name,
                    attempt,
                    self.max_retries,
                    exc,
                    exc_info=self._log.isEnabledFor(logging.DEBUG),
                )
                if attempt < self.max_retries:
                    self._log.info(
                        "[tool] retry after %.2fs name=%r",
                        self.retry_delay_seconds,
                        name,
                    )
                    time.sleep(self.retry_delay_seconds)

        self._log.error(
            "[tool] giving up name=%r after %s attempts",
            name,
            self.max_retries,
        )
        err = last_error or RuntimeError("unknown tool error")
        return ToolMessage(
            content=(
                f"Tool {name!r} failed after {self.max_retries} attempt(s): {err!s}"
            ),
            tool_call_id=tool_call_id,
        )
