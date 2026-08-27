from __future__ import annotations

from typing import TYPE_CHECKING, Any

from agent_proving_ground.agent._bridge.types import AgentBridge
from agent_proving_ground.model._providers.providers import validate_openai_client
from agent_proving_ground.tool._tools._code_execution import CodeExecutionProviders
from agent_proving_ground.tool._tools._web_search._web_search import WebSearchProviders

if TYPE_CHECKING:
    from openai.types.responses import Response


async def inspect_responses_api_request(
    json_data: dict[str, Any],
    headers: dict[str, str] | None,
    web_search: WebSearchProviders | None,
    code_execution: CodeExecutionProviders | None,
    bridge: AgentBridge,
) -> "Response":
    validate_openai_client("agent bridge")

    from .responses_impl import inspect_responses_api_request_impl

    return await inspect_responses_api_request_impl(
        json_data, headers, web_search, code_execution, bridge
    )
