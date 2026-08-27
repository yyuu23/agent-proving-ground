from agent_proving_ground import Task, eval
from agent_proving_ground.dataset import Sample
from agent_proving_ground.model import ModelOutput, get_model
from agent_proving_ground.scorer import match
from agent_proving_ground.solver import generate, use_tools
from agent_proving_ground.tool import ToolDef
from agent_proving_ground.tool._tool import Tool, ToolSource


def test_tool_source() -> None:
    model = get_model(
        "mockllm/model",
        custom_outputs=[
            ModelOutput.for_tool_call(
                "mockllm/model",
                tool_name="addition",
                tool_arguments={"x": 1, "y": 1},
            ),
            ModelOutput.from_content("mockllm/model", content="2"),
        ],
    )

    async def addition(x: int, y: int):
        return x + y

    class GetTools(ToolSource):
        async def tools(self) -> list[Tool]:
            addition_tool = ToolDef(
                tool=addition,
                name="addition2",
                description="Add two numbers",
                parameters={"x": "Integer", "y": "Integer"},
            )
            return [addition_tool.as_tool()]

    task = Task(
        dataset=[Sample(input="What is 1 + 1?", target="2")],
        solver=[use_tools(GetTools()), generate()],
        scorer=match(numeric=True),
    )

    log = eval(task, model=model)[0]
    assert log.status == "success"


if __name__ == "__main__":
    test_tool_source()
