from typing import Literal

from agent_proving_ground import Task, task
from agent_proving_ground.agent._human.agent import human_cli


@task
def human(user: Literal["root", "nonroot"] | None = None) -> Task:
    return Task(
        solver=human_cli(user=user),
        sandbox=("docker", "compose.yaml"),
    )
