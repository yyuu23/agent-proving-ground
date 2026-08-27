from agent_proving_ground import Task, task
from agent_proving_ground.dataset import FieldSpec, hf_dataset
from agent_proving_ground.scorer import model_graded_qa
from agent_proving_ground.solver import generate


@task
def simpleqa():
    return Task(
        dataset=hf_dataset(
            "codelion/SimpleQA-Verified",
            split="train",
            sample_fields=FieldSpec(
                input="problem",
                target="answer",
            ),
        ),
        solver=generate(),
        scorer=model_graded_qa(),
    )
