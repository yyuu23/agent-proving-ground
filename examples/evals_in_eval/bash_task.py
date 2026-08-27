from agent_proving_ground import Task, task
from agent_proving_ground.dataset import Sample
from agent_proving_ground.scorer import includes
from agent_proving_ground.solver import generate, use_tools
from agent_proving_ground.tool import bash


@task
def bash_task():
    return Task(
        dataset=[
            Sample(
                input="Use the bash tool to print 'hello world'.",
                target="hello world",
            ),
        ],
        solver=[use_tools([bash()]), generate()],
        scorer=includes(),
        sandbox="docker",
    )
