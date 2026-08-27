from agent_proving_ground import Task, task
from agent_proving_ground.agent._react import react
from agent_proving_ground.dataset import Sample
from agent_proving_ground.model._generate_config import GenerateConfig
from agent_proving_ground.tool import mcp_server_stdio, mcp_tools


@task
def mcp_git_tools():
    git_server = mcp_server_stdio(
        command="python3", args=["-m", "mcp_server_git", "--repository", "."]
    )

    return Task(
        dataset=[
            Sample(
                "What is the status of the git working tree for the current directory?. Additionally, could you summarise recent commits that have been made to the reposiotry?"
            )
        ],
        solver=react(
            name="git_worker",
            prompt="Please use the git tools to solve the problems.",
            tools=[mcp_tools(git_server, tools=["git_log", "git_status"])],
        ),
        config=GenerateConfig(parallel_tool_calls=False),
    )
