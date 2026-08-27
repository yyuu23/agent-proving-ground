from typing import Literal

from pydantic import Field

from agent_proving_ground._util.error import EvalError
from agent_proving_ground.event._base import BaseEvent


class ErrorEvent(BaseEvent):
    """Event with sample error."""

    event: Literal["error"] = Field(default="error")
    """Event type."""

    error: EvalError
    """Sample error"""
