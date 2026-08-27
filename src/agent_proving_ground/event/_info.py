from typing import Literal

from pydantic import Field, JsonValue

from agent_proving_ground.event._base import BaseEvent


class InfoEvent(BaseEvent):
    """Event with custom info/data."""

    event: Literal["info"] = Field(default="info")
    """Event type."""

    source: str | None = Field(default=None)
    """Optional source for info event."""

    data: JsonValue
    """Data provided with event."""
