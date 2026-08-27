from __future__ import annotations

from typing import TYPE_CHECKING, Any

from agent_proving_ground.agent._bridge.types import AgentBridge
from agent_proving_ground.model._providers.providers import validate_anthropic_client
from agent_proving_ground.tool._tools._code_execution import CodeExecutionProviders
from agent_proving_ground.tool._tools._web_search._web_search import WebSearchProviders

if TYPE_CHECKING:
    from anthropic.types import Message
    from anthropic.types.beta import BetaMessage


async def inspect_anthropic_api_request(
    json_data: dict[str, Any],
    headers: dict[str, str] | None,
    web_search: WebSearchProviders | None,
    code_execution: CodeExecutionProviders | None,
    bridge: AgentBridge,
    *,
    beta: bool = False,
) -> "Message | BetaMessage":
    validate_anthropic_client("agent bridge")

    from .anthropic_api_impl import inspect_anthropic_api_request_impl

    return await inspect_anthropic_api_request_impl(
        json_data, headers, web_search, code_execution, bridge, beta=beta
    )
