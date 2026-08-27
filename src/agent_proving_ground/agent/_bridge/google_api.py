from __future__ import annotations

from typing import Any

from agent_proving_ground.agent._bridge.types import AgentBridge
from agent_proving_ground.tool._tools._code_execution import CodeExecutionProviders
from agent_proving_ground.tool._tools._web_search._web_search import WebSearchProviders


async def inspect_google_api_request(
    json_data: dict[str, Any],
    web_search: WebSearchProviders | None,
    code_execution: CodeExecutionProviders | None,
    bridge: AgentBridge,
) -> dict[str, Any]:
    from .google_api_impl import inspect_google_api_request_impl

    return await inspect_google_api_request_impl(
        json_data, web_search, code_execution, bridge
    )
