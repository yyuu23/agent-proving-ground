from pydantic import BaseModel

from agent_proving_ground.event._event import Event


class SampleEvent(BaseModel):
    id: str | int
    epoch: int
    event: Event
