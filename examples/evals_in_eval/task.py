from claude import claude_code

from agent_proving_ground import Task, task
from agent_proving_ground.dataset import MemoryDataset, Sample


@task
def evals_in_eval() -> Task:
    return Task(
        dataset=MemoryDataset(
            [
                Sample(
                    input="Run two evaluations using the inspect CLI:\n1. 'apg eval file_probe.py'\n2. 'apg eval bash_task.py'\n\nAfter running both, report the accuracy scores from each evaluation.",
                    files={
                        "file_probe.py": "file_probe.py",
                        "bash_task.py": "bash_task.py",
                    },
                )
            ]
        ),
        solver=claude_code(),
        sandbox=("docker", "compose.yaml"),
    )
