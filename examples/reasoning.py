from agent_proving_ground import Task, task
from agent_proving_ground.agent import react
from agent_proving_ground.dataset import Sample
from agent_proving_ground.model._generate_config import GenerateConfig
from agent_proving_ground.tool import Tool, tool


@tool
def validate() -> Tool:
    async def execute(answer: str) -> bool:
        """Validate the answer to a mathematical question.

        Args:
            answer: Answer to validate
        """
        return True

    return execute


@task
def reasoning() -> Task:
    return Task(
        dataset=[
            Sample(
                input="Solve 3*x^3-5*x=1, then call the validate() tool validate your answer. Then after that, solve x^2 - 5x + 6 = 0 and once again call the validate() tool to validate your answer."
            )
        ],
        solver=react(
            prompt="Note that you must use reasoning before solving each problem presented. Do not attempt to solve a problem without reasoning first.",
            tools=[validate()],
        ),
        config=GenerateConfig(
            reasoning_effort="medium", reasoning_tokens=8192, max_tokens=16384
        ),
    )
