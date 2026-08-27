from typing import Awaitable, Callable, TypeAlias

from agent_proving_ground._util.content import ContentText

SearchProvider: TypeAlias = Callable[
    [str], Awaitable[str | ContentText | list[ContentText] | None]
]
