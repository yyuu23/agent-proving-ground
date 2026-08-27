from openai import AsyncOpenAI

from agent_proving_ground import Task, eval, task
from agent_proving_ground.agent import Agent, AgentState, agent, agent_bridge
from agent_proving_ground.dataset import Sample
from agent_proving_ground.model._prompt import user_prompt
from agent_proving_ground.scorer import includes


@agent
def responses_agent() -> Agent:
    async def execute(state: AgentState) -> AgentState:
        async with agent_bridge(state) as bridge:
            client = AsyncOpenAI()

            await client.responses.create(
                model="inspect",
                input=user_prompt(state.messages).text,
            )

            return bridge.state

    return execute


@task
def bridged_task():
    return Task(
        dataset=[
            Sample(
                input="Please print the word 'hello'?",
                target="hello",
            )
        ],
        solver=responses_agent(),
        scorer=includes(),
    )


if __name__ == "__main__":
    eval(
        bridged_task(),
        model="openai/gpt-4o",
        display="plain",
    )
