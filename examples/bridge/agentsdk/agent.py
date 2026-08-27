from agents import Agent as OpenAIAgent
from agents import RunConfig, Runner, WebSearchTool

from agent_proving_ground.agent import Agent, AgentState, agent, agent_bridge
from agent_proving_ground.model import messages_to_openai_responses


@agent
def web_research_agent() -> Agent:
    """OpenAI Agents SDK search agent."""

    async def execute(state: AgentState) -> AgentState:
        # Use bridge to map OpenAI Responses API to AgentProvingGround Model API
        async with agent_bridge(state) as bridge:
            agent = OpenAIAgent(
                name="SearchAssistant",
                instructions="You help users find information by searching the web.",
                tools=[WebSearchTool()],
            )

            await Runner.run(
                starting_agent=agent,
                input=await messages_to_openai_responses(state.messages),
                run_config=RunConfig(model="inspect"),
            )

            return bridge.state

    return execute
