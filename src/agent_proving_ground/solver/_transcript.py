import contextlib
from typing import AsyncIterator

from agent_proving_ground._util.json import json_changes
from agent_proving_ground._util.registry import registry_log_name
from agent_proving_ground.event._state import StateEvent
from agent_proving_ground.util._span import span

from ._solver import Solver
from ._task_state import TaskState, state_jsonable


class SolverTranscript:
    def __init__(self, name: str, before_state: TaskState) -> None:
        self.name = name
        self.before = state_jsonable(before_state)

    def complete(self, after_state: TaskState) -> None:
        from agent_proving_ground.log._transcript import transcript

        after = state_jsonable(after_state)
        changes = json_changes(self.before, after)
        if changes:
            transcript()._event(StateEvent(changes=changes))


@contextlib.asynccontextmanager
async def solver_transcript(
    solver: Solver, state: TaskState, name: str | None = None
) -> AsyncIterator[SolverTranscript]:
    name = registry_log_name(name or solver)
    async with span(name=name, type="solver"):
        yield SolverTranscript(name, state)
