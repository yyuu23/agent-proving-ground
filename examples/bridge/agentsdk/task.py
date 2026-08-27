from agent import web_research_agent

from agent_proving_ground import Task, task
from agent_proving_ground.dataset import json_dataset
from agent_proving_ground.scorer import model_graded_fact


@task
def research() -> Task:
    return Task(
        dataset=json_dataset("dataset.json"),
        solver=web_research_agent(),
        scorer=model_graded_fact(),
    )
