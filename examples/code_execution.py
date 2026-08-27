from agent_proving_ground import Task, task
from agent_proving_ground.dataset import Sample
from agent_proving_ground.solver import generate, use_tools
from agent_proving_ground.tool import code_execution


@task
def code_execution_task():
    return Task(
        dataset=[
            Sample(
                "Please use your available tools to execute Python code that adds 435678 + 23457 and then prints the result."
            )
        ],
        solver=[use_tools(code_execution()), generate()],
        sandbox="docker",
    )
