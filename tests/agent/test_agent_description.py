from test_helpers.utils import skip_if_no_openai

from agent_proving_ground import Task, eval
from agent_proving_ground.agent import Agent, AgentState, agent, handoff
from agent_proving_ground.dataset import Sample
from agent_proving_ground.model import get_model
from agent_proving_ground.solver import generate, use_tools
from agent_proving_ground.tool import Tool


@agent
def searcher() -> Agent:
    async def execute(state: AgentState) -> AgentState:
        """Searcher

        Args:
            state: Input state (conversation)
            max_searches: Maximum number of web searches to conduct

        Returns:
            Ouput state (additions to conversation)
        """
        return state

    return execute


@agent(description="Searcher2")
def searcher2() -> Agent:
    async def execute(state: AgentState) -> AgentState:
        """Searcher

        Args:
            state: Input state (conversation)
            max_searches: Maximum number of web searches to conduct

        Returns:
            Ouput state (additions to conversation)
        """
        return state

    return execute


def check_agent_description(
    description: str | None = None, agent_handoff: Tool | None = None
) -> None:
    agent_handoff = agent_handoff or handoff(searcher(), description=description)
    log = eval(
        Task(dataset=[Sample(input="Please use the searcher.")]),
        solver=[use_tools(agent_handoff), generate()],
        model=get_model("openai/gpt-4o-mini"),
    )[0]
    assert log.samples
    model_event = next(
        (event for event in log.samples[0].events if event.event == "model")
    )
    assert model_event.tools[0].description == (description or "Searcher")


@skip_if_no_openai
def test_agent_description_doc_comment():
    check_agent_description()


@skip_if_no_openai
def test_agent_description_handoff_param():
    check_agent_description("Searcher3")


@skip_if_no_openai
def test_agent_description_handoff_deorator():
    check_agent_description("Searcher2", handoff(searcher2()))
