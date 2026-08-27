from typing import Literal

from pydantic import Field

from agent_proving_ground._util.json import JsonChange
from agent_proving_ground.event._base import BaseEvent


class StateEvent(BaseEvent):
    """Change to the current `TaskState`"""

    event: Literal["state"] = Field(default="state")
    """Event type."""

    changes: list[JsonChange]
    """List of changes to the `TaskState`"""
