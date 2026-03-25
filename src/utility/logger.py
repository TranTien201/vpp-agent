import functools
import inspect
import logging
import os
from collections.abc import Callable
from typing import Any, cast

import colorama
from agents import RunContextWrapper
from colorama import Fore
from rich.console import Console
from rich.rule import Rule
from rich.style import Style
from rich.text import Text

from multi_agents.model import BranchingPlanStep, PlanStep, VplayContext
from multi_agents.model._log import ToolCallLog, TurnLog

Logger = logging.getLogger(__name__)

LOG_EXPAND_RAW: bool = os.getenv("LOG_EXPAND_RAW", "false").lower() == "true"
console = Console()


class Styles:
    """Style definitions for different log elements."""

    # Headers
    HEADER = Style(color="cyan", bold=True)
    SUBHEADER = Style(color="blue")

    # Status
    SUCCESS = Style(color="green", bold=True)
    ERROR = Style(color="red", bold=True)
    WARNING = Style(color="yellow")
    INFO = Style(color="white")

    # Raw content (very dim for less distraction - like thinking mode)
    RAW_BORDER = Style(color="grey37")
    RAW_CONTENT = Style(color="grey58")
    RAW_HEADER = Style(color="grey50")

    # Plan status
    PENDING = Style(color="grey50", dim=True)
    IN_PROGRESS = Style(color="yellow", bold=True)
    COMPLETED = Style(color="green")
    SKIPPED = Style(color="grey50", dim=True)

    # Tool
    TOOL_NAME = Style(color="magenta", bold=True)
    TOOL_ARG_KEY = Style(color="white", dim=True)
    TOOL_ARG_VALUE = Style(color="yellow")


class ColorFormatter(logging.Formatter):
    # Define colors for each log level
    LOG_COLORS: dict[int, str] = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + colorama.Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        # Get the color based on the log level
        log_color = self.LOG_COLORS.get(record.levelno, Fore.WHITE)
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        record.msg = f"{record.msg}"

        # Add color to the message
        record.msg = f"{log_color}{record.msg}{colorama.Style.RESET_ALL}"
        record.levelname = f"{log_color}{record.levelname}{colorama.Style.RESET_ALL}"
        record.filename = f"{log_color}{record.filename}{colorama.Style.RESET_ALL}"
        record.name = f"{log_color}{record.name}{colorama.Style.RESET_ALL}"

        # Use a custom field for formatted lineno
        formatted_lineno = f"{log_color}{record.lineno}{colorama.Style.RESET_ALL}"

        # Format the log message
        formatted_message = super().format(record)

        # Replace lineno placeholder in the final message
        return formatted_message.replace(f":{record.lineno}", f":{formatted_lineno}")


def logger_setup(log_level: str = "INFO") -> None:
    assert log_level in ["DEBUG", "INFO", "WARNING"], "Invalid log level"
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter("%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s"))
    root_level = log_level

    loggers = [
        "root",
        "openai",
        "urllib3",
        "httpcore",
        "aiokafka",
        "pymongo",
        "tzlocal",
        "apscheduler",
        "googleapiclient",
        "LiteLLM",
        "instructor",
        "httpx",
        "graphviz",
        "opentelemetry",
    ]
    for name in loggers:
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.addHandler(handler)
        if name == "opentelemetry":
            logger.setLevel(logging.CRITICAL)
        else:
            logger.setLevel(root_level if name == "root" else logging.WARNING)
