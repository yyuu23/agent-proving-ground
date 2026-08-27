"""Tests for update_plan tool."""

from test_helpers.tool_call_utils import get_tool_event

from agent_proving_ground import Task, eval
from agent_proving_ground.dataset import Sample
from agent_proving_ground.model import ModelOutput, get_model
from agent_proving_ground.solver import generate, use_tools
from agent_proving_ground.tool import update_plan


async def test_update_plan_basic() -> None:
    """Test basic plan update."""
    tool = update_plan()
    result = await tool(
        plan=[
            {"step": "Step 1", "status": "completed"},
            {"step": "Step 2", "status": "in_progress"},
            {"step": "Step 3", "status": "pending"},
        ],
        explanation="Making progress",
    )
    assert result == "Plan updated"


def test_update_plan_via_mockllm() -> None:
    """Test update_plan through a mocked model evaluation."""
    task = Task(
        dataset=[Sample(input="Create a plan")],
        solver=[use_tools(update_plan()), generate()],
    )

    model = get_model(
        "mockllm/model",
        custom_outputs=[
            ModelOutput.for_tool_call(
                model="mockllm/model",
                tool_name="update_plan",
                tool_arguments={
                    "plan": [
                        {"step": "Analyze", "status": "in_progress"},
                        {"step": "Implement", "status": "pending"},
                    ]
                },
            ),
            ModelOutput.from_content("mockllm/model", "Done"),
        ],
    )

    log = eval(task, model=model)[0]
    assert log.status == "success"

    tool_event = get_tool_event(log)
    assert tool_event is not None
    assert tool_event.function == "update_plan"
    assert isinstance(tool_event.arguments["plan"], list)
    assert len(tool_event.arguments["plan"]) == 2
