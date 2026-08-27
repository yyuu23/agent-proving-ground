from typing import Generator

from test_helpers.tool_call_utils import get_tool_calls, get_tool_response

from agent_proving_ground import Task, eval
from agent_proving_ground.dataset import Sample
from agent_proving_ground.model import ModelOutput, get_model
from agent_proving_ground.scorer import includes, match
from agent_proving_ground.solver import Generate, TaskState, generate, solver, use_tools
from agent_proving_ground.tool import tool
from agent_proving_ground.util._store import store


def test_sample_store():
    @solver
    def store_solver():
        async def solve(state: TaskState, generate: Generate):
            state.store.set("data", state.sample_id)
            return state

        return solve

    task = Task(
        dataset=[
            Sample(input="Say Hello", target="Hello"),
            Sample(input="Say Goodbye", target="Goodbye"),
        ],
        solver=[store_solver(), generate()],
        scorer=match(),
    )

    log = eval(task, model="mockllm/model")[0]
    assert log.samples[0].store["data"] == 1
    assert log.samples[1].store["data"] == 2


def test_tool_store():
    @tool
    def get_cookie():
        async def exec():
            """
            Tool for getting the cookie.

            If you are asked to get a cookie, call the get_cookie function.

            Returns: The cookie.
            """
            return store().get("cookie", 0)

        return exec

    @solver
    def store_solver():
        async def solve(state: TaskState, generate: Generate):
            state.store.set("cookie", 42)
            return state

        return solve

    task = Task(
        dataset=[
            Sample(input="Get the cookie using the available tools.", target="ignored"),
        ],
        solver=[use_tools(get_cookie()), store_solver(), generate()],
        scorer=includes(),
    )

    def custom_outputs() -> Generator[ModelOutput, None, None]:
        yield ModelOutput.for_tool_call(
            model="mockllm/model",
            tool_name="get_cookie",
            tool_arguments={},
        )
        while True:
            yield ModelOutput.from_content(
                model="mockllm/model",
                content="finished",
            )

    log = eval(
        task,
        get_model(
            "mockllm/model",
            custom_outputs=custom_outputs(),
        ),
        message_limit=5,
    )[0]
    assert (
        get_tool_response(
            log.samples[0].messages,
            get_tool_calls(log.samples[0].messages, "get_cookie")[0],
        ).text
        == "42"
    )


def test_store_create():
    @solver
    def store_solver():
        async def solve(state: TaskState, generate: Generate):
            COLORS = ["red", "green", "blue"]
            colors = state.store.get("colors", COLORS.copy())
            colors.append("orange")
            assert state.store.get("colors") == (COLORS + ["orange"])
            return state

        return solve

    task = Task(solver=[store_solver()])

    log = eval(task, model="mockllm/model")[0]
    assert log.status == "success"
