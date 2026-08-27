from agent_proving_ground import Task, task
from agent_proving_ground.dataset import Sample
from agent_proving_ground.scorer import exact
from agent_proving_ground.solver import generate

# This is the simplest possible AgentProvingGround eval, useful for testing your configuration / network / platform etc.


@task
def hello_world():
    return Task(
        dataset=[
            Sample(
                input="Just reply with Hello World",
                target="Hello World",
            )
        ],
        solver=[
            generate(),
        ],
        scorer=exact(),
    )
