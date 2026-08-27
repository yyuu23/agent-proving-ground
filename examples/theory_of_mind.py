from agent_proving_ground import Task, eval, task
from agent_proving_ground.dataset import example_dataset
from agent_proving_ground.scorer import model_graded_fact
from agent_proving_ground.solver import chain_of_thought, generate, self_critique


@task
def theory_of_mind(critique=False):
    # use self_critique if requested
    solver = [chain_of_thought(), generate()]
    if critique:
        solver.append(self_critique())

    return Task(
        dataset=example_dataset("theory_of_mind"),
        solver=solver,
        scorer=model_graded_fact(),
    )


if __name__ == "__main__":
    eval(theory_of_mind(critique=True), model="openai/gpt-4o")
