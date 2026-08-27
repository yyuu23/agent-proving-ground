from logging import getLogger
from typing import Any, Awaitable, Callable

from agent_proving_ground._util.logger import warn_once
from agent_proving_ground.agent._as_solver import as_solver

from ._solver import Solver, solver

logger = getLogger(__name__)


@solver
def bridge(agent: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]) -> Solver:
    """Bridge an external agent into an AgentProvingGround Solver.

    See documentation at <https://inspect.ai-safety-institute.org.uk/agent-bridge.html>

    Args:
      agent: Callable which takes a sample `dict` and returns a result `dict`.

    Returns:
      Standard AgentProvingGround solver.
    """
    from agent_proving_ground.agent._bridge.bridge import bridge as agent_bridge

    warn_once(
        logger,
        "The bridge solver is deprecated. Please use the bridge agent from the agents module instead.",
    )

    return as_solver(agent_bridge(agent))
