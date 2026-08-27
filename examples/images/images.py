from agent_proving_ground import Task, task
from agent_proving_ground.dataset import json_dataset
from agent_proving_ground.scorer import match
from agent_proving_ground.solver import generate, system_message

SYSTEM_MESSAGE = """
For the following exercise, it is important that you answer with only a single word or numeric value in brackets. For example, [22] or [house]. Do not include any discussion, narrative, or rationale, just a single value in brackets.
"""


@task
def images():
    return Task(
        dataset=json_dataset("images.jsonl"),
        solver=[system_message(SYSTEM_MESSAGE), generate()],
        scorer=match(),
    )
