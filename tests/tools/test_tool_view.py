import logging

import pytest
from test_helpers.tool_call_utils import get_tool_event
from test_helpers.utils import skip_if_no_docker

from agent_proving_ground import Task, eval
from agent_proving_ground.approval._apply import apply_tool_approval
from agent_proving_ground.approval._approval import Approval
from agent_proving_ground.dataset import Sample
from agent_proving_ground.model import ModelOutput, get_model
from agent_proving_ground.model._call_tools import tool_call_view
from agent_proving_ground.solver import generate, use_tools
from agent_proving_ground.tool import bash
from agent_proving_ground.tool._tool_call import (
    ToolCall,
    ToolCallContent,
    ToolCallView,
)
from agent_proving_ground.tool._tool_def import ToolDef


@skip_if_no_docker
@pytest.mark.slow
def test_tool_view():
    task = Task(
        dataset=[
            Sample(
                input="Please use the bash tool to list the files in the current directory?"
            )
        ],
        solver=[use_tools(bash()), generate()],
        sandbox="docker",
    )
    log = eval(
        task,
        model=get_model(
            "mockllm/model",
            custom_outputs=[
                ModelOutput.for_tool_call(
                    model="mockllm/model",
                    tool_name="bash",
                    tool_arguments={"code": "ls ."},
                ),
                ModelOutput.from_content(model="mockllm/model", content="All done!."),
            ],
        ),
    )[0]

    event = get_tool_event(log)
    assert event.view is not None


def _make_tool_def(name: str, viewer) -> ToolDef:
    async def execute(thought: str) -> str:
        return ""

    return ToolDef(
        execute,
        name=name,
        description="test",
        parameters={"thought": "a thought"},
        viewer=viewer,
    )


class _ListHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


def _attach(logger_name: str) -> _ListHandler:
    handler = _ListHandler()
    logging.getLogger(logger_name).addHandler(handler)
    return handler


def test_tool_call_view_swallows_viewer_error():
    def raising_viewer(call: ToolCall) -> ToolCallView:
        return ToolCallView(
            call=ToolCallContent(
                format="markdown", content=call.arguments["missing_key"]
            )
        )

    tdef = _make_tool_def("viewer_keyerror_tool", raising_viewer)
    call = ToolCall(id="1", function="viewer_keyerror_tool", arguments={})

    handler = _attach("agent_proving_ground.model._call_tools")
    try:
        result = tool_call_view(call, [tdef])
    finally:
        logging.getLogger("agent_proving_ground.model._call_tools").removeHandler(handler)

    assert result is None
    assert any(
        "viewer_keyerror_tool" in r.getMessage() and "Error in viewer" in r.getMessage()
        for r in handler.records
    )


def test_tool_call_view_returns_view_when_viewer_succeeds():
    def good_viewer(call: ToolCall) -> ToolCallView:
        return ToolCallView(
            call=ToolCallContent(format="markdown", content="rendered ok")
        )

    tdef = _make_tool_def("viewer_ok_tool", good_viewer)
    call = ToolCall(id="1", function="viewer_ok_tool", arguments={})

    result = tool_call_view(call, [tdef])

    assert result is not None
    assert result.content == "rendered ok"


async def test_apply_tool_approval_falls_back_when_viewer_raises() -> None:
    def raising_viewer(call: ToolCall) -> ToolCallView:
        raise TypeError("not a string")

    captured: dict[str, ToolCallView] = {}

    async def capture_approver(message, call, view, history) -> Approval:
        captured["view"] = view
        return Approval(decision="approve", explanation="ok")

    from agent_proving_ground.approval._apply import _tool_approver

    token = _tool_approver.set(capture_approver)
    handler = _attach("agent_proving_ground.approval._apply")
    try:
        approved, _ = await apply_tool_approval(
            "msg",
            ToolCall(id="1", function="viewer_typeerror_tool", arguments={"x": 1}),
            raising_viewer,
            [],
        )
    finally:
        _tool_approver.reset(token)
        logging.getLogger("agent_proving_ground.approval._apply").removeHandler(handler)

    assert approved is True
    view = captured["view"]
    assert view.call is not None
    assert "viewer_typeerror_tool" in view.call.content
    assert any(
        "viewer_typeerror_tool" in r.getMessage()
        and "Error in viewer" in r.getMessage()
        for r in handler.records
    )
