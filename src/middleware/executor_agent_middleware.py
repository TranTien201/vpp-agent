import logging
from collections.abc import Callable

from langchain.agents.middleware import ModelRequest, ModelResponse
from ._base import BaseMiddleware
from src.model import AgentContext
from src.tools import EXECUTOR_TOOLS, TOOL_REGISTRY, tools_for_executor_turn

_log = logging.getLogger(__name__)

_ALLOWED_TOOL_NAMES = set(TOOL_REGISTRY) | {t.name for t in EXECUTOR_TOOLS}


class ExecutorAgentMiddleware(BaseMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def wrap_model_call(
        self,
        request: ModelRequest[AgentContext],
        handler: Callable[[ModelRequest[AgentContext]], ModelResponse],
    ) -> ModelResponse:
        runtime = request.runtime
        
        if runtime is None or runtime.context is None:
            _log.debug("executor tool middleware: no runtime context, skipping tool override")
            return handler(request)

        tool_name_enabled = runtime.context.current_tool_enabled

        for name in tool_name_enabled:
            if name not in _ALLOWED_TOOL_NAMES:
                _log.warning(
                    "executor tools: name %r not in TOOL_REGISTRY / EXECUTOR_TOOLS, ignored",
                    name,
                )

        tools = tools_for_executor_turn(tool_name_enabled)
        return handler(request.override(tools=tools))
