from agent_proving_ground import Task, task
from agent_proving_ground.dataset import Sample
from agent_proving_ground.scorer import match


@task
def example_task() -> Task:
    task = Task(
        dataset=[Sample(input="Say Hello", target="Hello")],
        scorer=match(),
        metadata={"meaning_of_life": 42},
    )
    return task
