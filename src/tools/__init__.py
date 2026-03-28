from __future__ import annotations

from collections.abc import Sequence

from langchain_core.tools import BaseTool

from .plan_tool import update_plan, replan
from .business_tool import search_internal_knowledge_tool, fetch_rag_documents_tool, extraction_information_tool
from .validate_tool import validate_step_tool


EXECUTOR_TOOLS: list[BaseTool] = [update_plan, replan]

TOOL_REGISTRY: dict[str, BaseTool] = {
    search_internal_knowledge_tool.name: search_internal_knowledge_tool,
    fetch_rag_documents_tool.name: fetch_rag_documents_tool,
    extraction_information_tool.name: extraction_information_tool,
    validate_step_tool.name: validate_step_tool,
}

ALL_EXECUTOR_TOOLS = [*EXECUTOR_TOOLS, *TOOL_REGISTRY.values()]


def tools_for_executor_turn(tool_name_enabled: Sequence[str]) -> list[BaseTool]:
    return [
        *EXECUTOR_TOOLS,
        *[TOOL_REGISTRY[n] for n in tool_name_enabled if n in TOOL_REGISTRY],
    ]


__all__ = [
    "ALL_EXECUTOR_TOOLS",
    "EXECUTOR_TOOLS",
    "TOOL_REGISTRY",
    "tools_for_executor_turn",
    "update_plan",
    "replan",
    "search_internal_knowledge_tool",
    "fetch_rag_documents_tool",
    "extraction_information_tool",
    "validate_step_tool",
]